# ☁️ AWS Secure Phishing Infrastructure (IaC with Python CDK)

## 📋 Project Overview
Un'infrastruttura **Cloud-Native su AWS** completamente automatizzata tramite codice **(IaC)** utilizzando **AWS CDK (Python)**, progettata per simulazioni di campagne di Phishing etico.

Questo progetto non si limita a lanciare un attacco, ma costruisce un ambiente isolato seguendo le **Best Practices di sicurezza AWS** e della **Defense in Depth**: crittografia, segmentazione di rete e monitoraggio attivo.

---

## 📐 Architettura
L'infrastruttura è progettata seguendo il **AWS Well-Architected Framework**:

<img width="1073" height="745" alt="Architecture_Diagram" src="https://github.com/user-attachments/assets/ca18dbf9-e4cb-40ba-8d45-e744ff861ef1" />

## 🛡️ Caratteristiche di Sicurezza

* **WAF & ALB:** Filtraggio traffico Web per bloccare bot e scanner automatizzati.
* **Private Networking:** Server isolato in subnet privata (Invisibile da Internet).
* **Zero SSH:** Porta 22 chiusa. Accesso amministrativo sicuro tramite AWS Systems Manager.
* **Encryption:** Dischi cifrati a riposo con chiavi KMS gestite dal cliente.
* **Monitoraggio:** **Amazon GuardDuty** (Intrusion Detection) e **AWS Inspector** (Vulnerability Scanning) attivi per la massima visibilità.

---

## 🛠️ Stack Tecnologico

* **IaC:** AWS CDK (Python 3.11)
* **Networking (VPC Segmentata):**
    * *Public Subnet:* Solo per il Load Balancer (ALB).
    * *Private Subnet:* L'istanza di attacco (Server) è isolata da Internet.
* **Software & Tooling:** * **Python Flask:** Utilizzato per lo sviluppo del PoC e i test di simulazione locale.
    * **Docker:** Implementato nello stack IaC per il deploy containerizzato di GoPhish su istanza EC2.
* **AWS Services:** VPC, EC2, IAM, KMS, ALB, WAF, Systems Manager, GuardDuty, Inspector.

---

### A. Definizione Infrastruttura (CDK)
Il codice definisce l'intera architettura. Sintesi del template CloudFormation (~400 righe) generato automaticamente.

<img width="1909" height="1030" alt="infra_cdk_synth png" src="https://github.com/user-attachments/assets/1130033a-37ce-47df-9221-280be88a1e92" />

### B. La Trappola (Phishing Page PoC)
Simulazione del payload lato vittima: una pagina di login clone (Google Workspace) pixel-perfect ospitata localmente, all'indirizzo: http://127.0.0.1:5000.

<img width="1909" height="882" alt="poc_phishing_page png" src="https://github.com/user-attachments/assets/abf83fbb-9715-462c-ab00-b0477ee049b2" />

### C. L'Attacco (Credential Harvesting)
Dimostrazione del backend: le credenziali inserite dalla vittima vengono intercettate, salvate e la vittima viene reindirizzata al sito reale.

<img width="1910" height="750" alt="attack_result_loot png" src="https://github.com/user-attachments/assets/e10da12f-5857-4a22-8811-291eb802c3a7" />

---

## 🚀 Guida Rapida

### Prerequisiti
* AWS CLI configurata
* Node.js & AWS CDK installati
* Python 3.11 + Docker

### 1. Deploy Infrastruttura
```bash
# Attivazione ambiente virtuale (Windows)
.venv\Scripts\Activate.ps1 

# Installazione dipendenze
pip install -r requirements.txt

# Sintesi del template (Test)
cdk synth
```
### 2. Esecuzione Simulazione (Locale)

                  # Avvio del server di phishing simulato
                   python demo_attack.py
                   
> **⚠️ DISCLAIMER:** Questo progetto è stato sviluppato esclusivamente a scopo educativo e di ricerca etica (Red Teaming / Awareness Training). L'autore non si assume alcuna responsabilità per l'uso improprio del codice. L'obiettivo è dimostrare come blindare un'infrastruttura offensiva utilizzando AWS CDK e Best Practices di sicurezza.
