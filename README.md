🛡️ DeepRecon Pro: Automated Information Gathering Framework
Python VersionLicense: MITPlatform: Windows/Linux

📝 Overview
DeepRecon Pro é uma ferramenta de orquestração de reconhecimento (Recon) desenvolvida para automatizar o mapeamento de superfícies de ataque. Ela integra ferramentas de inteligência de ameaças, escaneamento de rede e descoberta de subdomínios em um único framework modular e intuitivo.

O objetivo principal é reduzir o tempo de coleta de dados iniciais (Information Gathering), permitindo que profissionais de segurança foquem na análise de vulnerabilidades.

✨ Key Features
Multi-Platform Support: Totalmente compatível com Windows e Linux.
Modular Architecture: Sistema de módulos para expansão fácil (Subdomain Enumeration, Port Scanning, Vulnerability Detection).
Dependency Checker: Sistema inteligente que detecta se as ferramentas essenciais (nmap, subfinder, etc.) estão instaladas e configuradas no PATH.
Interactive CLI: Interface de menu amigável para usuários iniciantes e avançados.
Automated Reporting: Gera relatórios detalhados em formato JSON para integração com outras ferramentas de segurança.
🚀 Getting Started
Prerequisites
Certifique-se de ter instalado:

Python 3.8+
Nmap
Go (para ferramentas como subfinder e nuclei)
Installation
Clone o repositório:
bash
Download
Copy code
git clone https://github.com/seu-usuario/deeprecon-pro.git
cd deeprecon-pro
Instale as dependências do Python:
bash
Download
Copy code
pip install -r requirements.txt
🛠️ Usage
Execute o script principal e siga as instruções no menu interativo:

bash
Download
Copy code
python deeprecon_pro.py
⚠️ Disclaimer
Esta ferramenta deve ser utilizada apenas para fins educacionais ou em ambientes onde você possui autorização explícita para realizar testes de segurança. O uso indevido pode ser ilegal.
