# ☁️ AWS Secure Phishing Infrastructure (IaC with Python CDK)

## 📋 Project Overview
Un'infrastruttura **Cloud-Native su AWS** completamente automatizzata tramite codice **(IaC)** utilizzando **AWS CDK (Python)**, progettata per simulazioni di campagne di Phishing etico.

Questo progetto non si limita a lanciare un attacco, ma costruisce un ambiente isolato seguendo le **Best Practices di sicurezza AWS** e della **Defense in Depth**: crittografia, segmentazione di rete e monitoraggio attivo.

---

## 📐 Architettura
L'infrastruttura è progettata seguendo il **AWS Well-Architected Framework**:

<img width="1073" height="745" alt="Architecture_Diagram" src="https://github.com/user-attachments/assets/5af9c44a-12e6-4403-8ffa-07a4321d74b0" />

**Caratteristiche di Sicurezza Implementate**

**Ingress Sicuro:** Traffico gestito da un Application Load Balancer (ALB) protetto da AWS WAF (Web Application Firewall) per bloccare bot e scanner.

**Isolamento:** L'istanza EC2 di attacco risiede in una Private Subnet. Nessun accesso diretto da Internet.

**Gestione Stealth:** Nessuna porta SSH (22) aperta. L'amministrazione avviene via AWS Systems Manager (Session Manager) tramite tunnel crittografato.

**Sicurezza Dati:** Volumi EBS crittografati con chiavi KMS gestite dal cliente.

**Monitoraggio:** Amazon GuardDuty attivo per rilevare minacce e intrusioni in tempo reale.






> **⚠️ DISCLAIMER:** Questo progetto è stato sviluppato esclusivamente a scopo educativo e di ricerca etica (Red Teaming / Awareness Training). L'autore non si assume alcuna responsabilità per l'uso improprio del codice. L'obiettivo è dimostrare come blindare un'infrastruttura offensiva utilizzando AWS CDK e Best Practices di sicurezza.
