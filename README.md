# ☁️AWS Secure Phishing Infrastructure (IaC with Python CDK)

## 📋 Overview
Un'infrastruttura **Cloud-Native su AWS** completamente automatizzata tramite il codice **(IaC)** utilizzando **AWS CDK (Python)**, progettata per simulazioni di campagne di Phishing etico utilizzando **GoPhish**. 
Questo progetto non si limita a lanciare un attacco, ma costruisce un ambiente isolato seguendo le **Best Practices di sicurezza AWS** e della **Defense in Depth**: crittografia, segmentazione di rete e monitoraggio attivo.

## 📐 Architettura
L'infrastruttura è progettata seguendo il **AWS Well-Architected Framework**:

<img width="1073" height="745" alt="Architecture Diagram" src="https://github.com/user-attachments/assets/d7824cb0-3335-450b-a853-5e3abac90718" />

1.  **Ingress Sicuro:** Traffico gestito da un **Application Load Balancer (ALB)** protetto da **AWS WAF**.
2.  **Isolamento:** L'istanza EC2 di attacco risiede in una **Private Subnet**. Nessun accesso diretto da Internet.
3.  **Gestione Stealth:** Nessuna porta SSH (22) aperta. L'amministrazione avviene via **AWS Systems Manager (Session Manager)** tramite tunnel crittografato.
4.  **Sicurezza Dati:** Volumi EBS crittografati con chiavi **KMS** gestite dal cliente.
5.  **Monitoraggio:** **Amazon GuardDuty** e **AWS Inspector** attivi per rilevare minacce e vulnerabilità in tempo reale.

## 🛠️ Stack Tecnologico
* **IaC:** AWS CDK Python 3.11
* **Software:** GoPhish (Campaign Management) & Custom Flask Payload
* **Containerization:** Docker (running GoPhish)
* **AWS Services:** VPC, EC2, IAM, KMS, ALB, WAF, Systems Manager.

## 🚀 Guida Rapida

### Prerequisiti
* AWS CLI configurata
* Node.js & AWS CDK installati
* Python 3.11 & Docker

