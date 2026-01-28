# ☁️ AWS Secure Phishing Infrastructure (IaC with Python CDK)

## 📋 Project Overview
Un'infrastruttura **Cloud-Native su AWS** completamente automatizzata tramite codice **(IaC)** utilizzando **AWS CDK (Python)**, progettata per simulazioni di campagne di Phishing etico.

Questo progetto non si limita a lanciare un attacco, ma costruisce un ambiente isolato seguendo le **Best Practices di sicurezza AWS** e della **Defense in Depth**: crittografia, segmentazione di rete e monitoraggio attivo.

---

## 📐 Architettura
L'infrastruttura è progettata seguendo il **AWS Well-Architected Framework**:

<img width="1073" height="745" alt="Architecture_Diagram" src="https://github.com/user-attachments/assets/5af9c44a-12e6-4403-8ffa-07a4321d74b0" />

## Caratteristiche di Sicurezza Implementate

**Ingress Sicuro:** Traffico gestito da un **Application Load Balancer (ALB)** protetto da **AWS WAF** (Web Application Firewall) per bloccare bot e scanner.

**Isolamento:** L'istanza EC2 di attacco risiede in una **Private Subnet**. Nessun accesso diretto da Internet.

**Gestione Stealth:** Nessuna porta SSH (22) aperta. L'amministrazione avviene via **AWS Systems Manager (Session Manager)** tramite tunnel crittografato.

**Sicurezza Dati:** Volumi EBS crittografati con chiavi **KMS** gestite dal cliente.

**Monitoraggio:** **Amazon GuardDuty** attivo per rilevare minacce e intrusioni in tempo reale.

## 🛠️ Stack Tecnologico

**IaC:** AWS CDK (Python 3.11)

**Networking (VPC Segmentata):**

- Public Subnet: Solo per il Load Balancer (ALB).
- Private Subnet: L'istanza di attacco (Server) è isolata da Internet.

**Software:** Python Flask (Payload simulato) & Docker.

**AWS Services:** VPC, EC2, IAM, KMS, ALB, WAF, Systems Manager, GuardDuty.

## A. Definizione Infrastruttura (CDK)
Il codice definisce l'intera architettura. Sintesi del template CloudFormation (~400 righe) generato automaticamente.

<img width="1909" height="1030" alt="infra_cdk_synth png" src="https://github.com/user-attachments/assets/31fb9f4f-fed2-4f3f-a24f-c5e7424734ab" />

## B. La Trappola (Phishing Page PoC)
Simulazione del payload lato vittima: una pagina di login clone (Google Workspace) pixel-perfect ospitata localmente.

<img width="1909" height="882" alt="poc_phishing_page png" src="https://github.com/user-attachments/assets/c68e6541-d5c6-4a29-9b35-137891aebb21" />

## C. L'Attacco (Credential Harvesting)
Dimostrazione del backend: le credenziali inserite dalla vittima vengono intercettate, salvate e la vittima viene reindirizzata al sito reale.

<img width="1910" height="750" alt="attack_result_loot png" src="https://github.com/user-attachments/assets/5202fcbb-940c-44f1-bcf8-3c0752926442" />

## 🚀 Guida Rapida

**Prerequisiti**
- AWS CLI configurata
- Node.js & AWS CDK installati
- Python 3.11 & Docker

## 1. Deploy Infrastruttura

                  # Attivazione ambiente virtuale (Windows)
                  .venv\Scripts\Activate.ps1 

                  # Installazione dipendenze
                  pip install -r requirements.txt

                  # Sintesi del template (Test)
                  cdk synth1 
## 2. Esecuzione Simulazione (Locale)
                  # Avvio del server di phishing simulato
                   python demo_attack.py
                   
> **⚠️ DISCLAIMER:** Questo progetto è stato sviluppato esclusivamente a scopo educativo e di ricerca etica (Red Teaming / Awareness Training). L'autore non si assume alcuna responsabilità per l'uso improprio del codice. L'obiettivo è dimostrare come blindare un'infrastruttura offensiva utilizzando AWS CDK e Best Practices di sicurezza.
