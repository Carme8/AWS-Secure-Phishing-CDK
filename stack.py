import os
from aws_cdk import (
    App,
    Stack,
    CfnOutput,
    Duration,
    Environment,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as targets,
    aws_kms as kms,
    aws_wafv2 as wafv2,
    aws_guardduty as guardduty,

)
from constructs import Construct

class SecurePhishingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # =================================================================================
        # 1. MONITORAGGIO & SICUREZZA (GuardDuty)
        # =================================================================================
        cfn_detector = guardduty.CfnDetector(self, "PhishingGuardDuty",
            enable=True,
            finding_publishing_frequency="FIFTEEN_MINUTES"
        )

        # =================================================================================
        # 2. RETE (VPC)
        # =================================================================================
        vpc = ec2.Vpc(self, "PhishingVPC",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(name="Public", subnet_type=ec2.SubnetType.PUBLIC),
                ec2.SubnetConfiguration(name="Private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS)
            ]
        )

        # =================================================================================
        # 3. SECURITY GROUPS
        # =================================================================================
        alb_sg = ec2.SecurityGroup(self, "AlbSG", vpc=vpc, description="Public HTTP access")
        # Modificato a porta 80 (HTTP) per test senza certificato
        alb_sg.add_ingress_rule(ec2.Peer.any_ipv4(), ec2.Port.tcp(80), "Allow HTTP")

        ec2_sg = ec2.SecurityGroup(self, "GoPhishSG", vpc=vpc, description="Private access from ALB only")
        ec2_sg.add_ingress_rule(alb_sg, ec2.Port.tcp(80), "Allow HTTP from ALB")

        # =================================================================================
        # 4. IAM & INSPECTOR
        # =================================================================================
        role = iam.Role(self, "GoPhishRole", assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSSMManagedInstanceCore"))
        role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonInspector2ManagedCisPolicy"))

        # =================================================================================
        # 5. EC2 & ENCRYPTION
        # =================================================================================
        disk_key = kms.Key(self, "DiskEncKey", enable_key_rotation=True)

        user_data = ec2.UserData.for_linux()
        user_data.add_commands(
            "yum update -y",
            "yum install -y docker",
            "service docker start",
            "usermod -a -G docker ssm-user",
            # GoPhish sulla porta 80
            "docker run -d --name gophish --restart always -p 80:80 -p 3333:3333 gophish/gophish"
        )

        instance = ec2.Instance(self, "GoPhishInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            security_group=ec2_sg,
            role=role,
            user_data=user_data,
            block_devices=[ec2.BlockDevice(
                device_name="/dev/xvda",
                volume=ec2.BlockDeviceVolume.ebs(30, encrypted=True, kms_key=disk_key)
            )]
        )

        # =================================================================================
        # 6. LOAD BALANCER (Versione HTTP senza Dominio)
        # =================================================================================
    
        
        alb = elbv2.ApplicationLoadBalancer(self, "PhishingALB",
            vpc=vpc,
            internet_facing=True,
            security_group=alb_sg
        )

        # Listener HTTP semplice sulla porta 80 (invece che HTTPS 443)
        listener = alb.add_listener("PublicListener", port=80)
        
        listener.add_targets("GoPhishTarget",
            port=80,
            targets=[targets.InstanceTarget(instance)],
            health_check=elbv2.HealthCheck(path="/", interval=Duration.seconds(60))
        )

        # =================================================================================
        # 7. WAF (Firewall Applicativo)
        # =================================================================================
        waf_rules = [
            wafv2.CfnWebACL.RuleProperty(
                name="AWS-AWSManagedRulesCommonRuleSet",
                priority=1,
                override_action=wafv2.CfnWebACL.OverrideActionProperty(none={}),
                statement=wafv2.CfnWebACL.StatementProperty(
                    managed_rule_group_statement=wafv2.CfnWebACL.ManagedRuleGroupStatementProperty(
                        name="AWSManagedRulesCommonRuleSet", vendor_name="AWS"
                    )
                ),
                visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                    cloud_watch_metrics_enabled=True, metric_name="CommonRules", sampled_requests_enabled=True
                )
            )
        ]

        web_acl = wafv2.CfnWebACL(self, "PhishingWebACL",
            default_action=wafv2.CfnWebACL.DefaultActionProperty(allow={}),
            scope="REGIONAL",
            visibility_config=wafv2.CfnWebACL.VisibilityConfigProperty(
                cloud_watch_metrics_enabled=True, metric_name="PhishingWebACL", sampled_requests_enabled=True
            ),
            rules=waf_rules
        )

        wafv2.CfnWebACLAssociation(self, "WafAssociation",
            resource_arn=alb.load_balancer_arn,
            web_acl_arn=web_acl.attr_arn
        )

        # =================================================================================
        # 8. OUTPUT OPERATIVI
        # =================================================================================
        
        # 1. URL pubblico (del Load Balancer, non del dominio)
        CfnOutput(self, "1_PhishingURL", value=f"http://{alb.load_balancer_dns_name}")

        # 2. Comando per Admin Tunnel
        CfnOutput(self, "2_CommandConnectAdmin", 
            value=f"aws ssm start-session --target {instance.instance_id} --document-name AWS-StartPortForwardingSession --parameters '{{\"portNumber\":[\"3333\"],\"localPortNumber\":[\"3333\"]}}'"
        )

        # 3. Comando Password
        cmd_get_pass = f"aws ssm start-session --target {instance.instance_id} --document-name AWS-RunShellScript --parameters 'commands=[\"docker logs gophish 2>&1 | grep Password\"]'"
        CfnOutput(self, "3_CommandGetPassword", value=cmd_get_pass)

# =================================================================================
# ESECUZIONE DELL'APP
# =================================================================================
app = App()

# Usiamo l'ambiente corrente (CDK_DEFAULT_ACCOUNT)
env = Environment(
    account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    region=os.environ.get("CDK_DEFAULT_REGION")
)

SecurePhishingStack(app, "SecurePhishingStack", env=env)

app.synth()