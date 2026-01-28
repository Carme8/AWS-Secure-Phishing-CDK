import aws_cdk as cdk
from stack import SecurePhishingStack

app = cdk.App()
SecurePhishingStack(app, "SecurePhishingStack")

app.synth()