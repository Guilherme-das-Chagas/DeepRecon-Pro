import os
import sys
import subprocess
import json
import platform
import time

class DeepReconPro:
    """
    Framework de Reconhecimento de Segurança.
    Desenvolvido para automação de coleta de informações (OSINT & Infra).
    """
    
    def __init__(self):
        self.os_type = platform.system()
        self.target = ""
        self.api_keys = {"vt": "", "shodan": ""}
        self.report_data = {
            "target": "",
            "os": self.os_type,
            "timestamp": "",
            "scans_performed": [],
            "results": {}
        }
        # Cores para interface CLI
        self.colors = {
            "cyan": "\033[96m", "green": "\033[92m", "yellow": "\033[93m",
            "red": "\033[91m", "reset": "\033[0m", "bold": "\033[1m"
        }

    def clear_screen(self):
        os.system('cls' if self.os_type == 'Windows' else 'clear')

    def print_banner(self):
        self.clear_screen()
        print(f"{self.colors['cyan']}{self.colors['bold']}")
        print("="*55)
        print("      🛡️  DEEPHAT RECON PRO - SECURITY FRAMEWORK")
        print("="*55)
        print(f"{self.colors['reset']} Sistema: {self.os_type} | Alvo: {self.target if self.target else 'Nenhum'}")
        print(f"{self.colors['reset']} Status: {'[+] Operacional' if self.target else '[!] Aguardando Configuração'}")
        print("="*55 + "\n")

    def check_dependencies(self):
        """Verifica se ferramentas críticas estão instaladas no sistema."""
        print(f"{self.colors['yellow']}[*] Verificando dependências essenciais...{self.colors['reset']}")
        deps = ["nmap", "whois", "subfinder"]
        missing = []
        
        for tool in deps:
            try:
                # Tenta rodar o comando para checar se existe no PATH
                subprocess.run(f"{tool} --version", shell=True, capture_output=True, timeout=3)
                print(f" [OK] {tool}")
            except:
                missing.append(tool)
                print(f" [!] {tool} NÃO ENCONTRADO")
        
        if missing:
            print(f"\n{self.colors['red']}⚠️  AVISO: Algumas ferramentas estão faltando: {', '.join(missing)}")
            print(f"DICA: Instale-as ou adicione ao seu PATH para melhor performance.{self.colors['reset']}")
            input("\nPressione Enter para continuar...")
        else:
            print(f"{self.colors['green']}[+] Dependências verificadas com sucesso!{self.colors['reset']}")

    def setup_config(self):
        """Configuração inicial do alvo e chaves."""
        self.print_banner()
        print(f"{self.colors['bold']}--- CONFIGURAÇÃO INICIAL ---{self.colors['reset']}")
        self.target = input(f"{self.colors['cyan']}Digite o domínio ou IP alvo: {self.colors['reset']}").strip()
        
        if not self.target:
            print(f"{self.colors['red']}Erro: Alvo obrigatório.{self.colors['reset']}")
            return False

        self.api_keys['vt'] = input(f"{self.colors['cyan']}VirusTotal API Key (Enter para pular): {self.colors['reset']}\n")
        self.api_keys['shodan'] = input(f"{self.colors['cyan']}Shodan API Key (Enter para pular): {self.colors['reset']}\n")
        
        self.report_data["target"] = self.target
        self.report_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        return True

    # --- MÓDULOS DE SCAN ---

    def run_geo_lookup(self):
        """Módulo de Geolocalização de IP."""
        ip = input(f"{self.colors['yellow']}Digite o IP para geolocalização: {self.colors['reset']}")
        if not ip: return
        
        print(f"{self.colors['cyan']}[*] Consultando localização para {ip}...{self.colors['reset']}")
        import requests # Import local para não travar se não houver internet
        url = f"http://ip-api.com/json/{ip}"
        
        try:
            res = requests.get(url, timeout=10).json()
            if res.get('status') == 'success':
                geo_info = {
                    "country": res.get("country"),
                    "region": res.get("regionName"),
                    "city": res.get("city"),
                    "isp": res.get("isp"),
                    "lat": res.get("lat"),
                    "lon": res.get("lon")
                }
                print(f"{self.colors['green']}[+] Localização: {geo_info['city']}, {geo_info['country']} (ISP: {geo_info['isp']}){self.colors['reset']}")
                self.report_data["results"]["geolocation"] = geo_info
            else:
                print(f"{self.colors['red']}Erro: {res.get('message')}{self.colors['reset']}")
        except Exception as e:
            print(f"{self.colors['red']}Erro na conexão: {str(e)}{self.colors['reset']}")
        
        input(f"\n{self.colors['cyan']}Pressione Enter para voltar...{self.colors['reset']}")

    def run_nmap_scan(self):
        """Scan de portas e serviços."""
        print(f"\n{self.colors['cyan']}[*] Iniciando Scan de Rede (Nmap)...{self.colors['reset']}")
        print("Isso pode levar alguns minutos dependendo do alvo...")
        
        # Comando Nmap: -F (rápido), -sV (versão de serviço), -T4 (velocidade)
        cmd = f"nmap -F -sV -T4 {self.target}"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        self.report_data["results"]["nmap"] = result.stdout
        self.report_data["scans_performed"].append("Network Scanning (Nmap)")
        print(result.stdout if result.stdout else "Nenhum dado retornado.")
        input(f"\n{self.colors['cyan']}Pressione Enter para voltar...{self.colors['reset']}")

    def run_subdomain_scan(self):
        """Busca de subdomínios via Subfinder."""
        print(f"\n{self.colors['cyan']}[*] Iniciando busca de subdomínios...{self.colors['reset']}")
        cmd = f"subfinder -d {self.target} -silent"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        subdomains = result.stdout.strip().split('\n')
        self.report_data["results"]["subdomains"] = [s for s in subdomains if s]
        self.report_data["scans_performed"].append("Subdomain Enumeration")
        
        print(f"[+] Subdomínios encontrados: {len(self.report_data['results']['subdomains'])}")
        print(result.stdout if result.stdout else "Nenhum subdomínio detectado.")
        input(f"\n{self.colors['cyan']}Pressione Enter para voltar...{self.colors['reset']}")

    def save_report(self):
        """Gera o arquivo de relatório final em JSON."""
        if not self.report_data["target"]:
            print(f"{self.colors['red']}Erro: Configure um alvo primeiro!{self.colors['reset']}")
            return

        filename = f"report_{self.target.replace('.', '_')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.report_data, f, indent=4, ensure_ascii=False)
        print(f"\n{self.colors['green']}[!] RELATÓRIO GERADO COM SUCESSO!{self.colors['reset']}")
        print(f"[+] Arquivo: {filename}")
        input(f"\nPressione Enter para voltar...{self.colors['reset']}")

    # --- MENU E FLUXO PRINCIPAL ---

    def start(self):
        self.clear_screen()
        print(f"{self.colors['bold']}1. Iniciar Nova Investigação")
        print("2. Ver Documentação")
        print("3. Sair")
        
        choice = input(f"\n{self.colors['yellow']}Escolha: {self.colors['reset']}")

        if choice == '1':
            if self.setup_config():
                self.check_dependencies()
                self.main_menu()
        elif choice == '2':
            self.show_docs()
        else:
            sys.exit()

    def main_menu(self):
        while True:
            self.print_banner()
            print(f"{self.colors['bold']}MENU DE OPERAÇÕES:{self.colors['reset']}")
            print(f"1. [🔍] Recon Passivo (Whois/APIs)")
            print(f"2. [🌐] Subdomínios (Subfinder)")
            print(f"3. [🛡️] Scan de Rede (Nmap)")
            print(f"4. [📍] Geolocalização (IP)")
            print(f"5. [📄] Gerar Relatório Final")
            print(f"0. [❌] Sair")
            print("-" * 30)
            
            choice = input(f"\n{self.colors['yellow']}Selecione uma opção: {self.colors['reset']}")

            if choice == '1':
                print(f"{self.colors['cyan']}[*] Módulo de Recon Passivo selecionado.{self.colors['reset']}")
                # Aqui você integraria o Whois/VT que discutimos
                input("\nPressione Enter para voltar...")
            elif choice == '2':
                self.run_subdomain_scan()
            elif choice == '3':
                self.run_nmap_scan()
            elif choice == '4':
                self.run_geo_lookup()
            elif choice == '5':
                self.save_report()
            elif choice == '0':
                break
            else:
                print(f"{self.colors['red']}Opção inválida!{self.colors['reset']}")
                time.sleep(1)

    def show_docs(self):
        self.clear_screen()
        print(f"{self.colors['cyan']}{self.colors['bold']}=====================================================")
        print("           DOCUMENTAÇÃO - DEEPHAT RECON PRO")
        print(f"====================================================={self.colors['reset']}")
        print(f"""
        {self.colors['bold']}SOBRE:{self.colors['reset']}
        Ferramenta de automação para coleta de informações em Cybersecurity.

        {self.colors['bold']}COMO USAR:{self.colors['reset']}
        1. Configure seu alvo (Domínio ou IP).
        2. Escolha um módulo no menu principal.
        3. Aguarde o processamento e veja os resultados no terminal.
        4. Gere o relatório JSON para análise posterior.

        {self.colors['bold']}REQUISITOS:{self.colors['reset']}
        - Python 3.8+
        - Nmap, Subfinder instalados no sistema.
        - Conexão com a Internet para APIs e Scans.

        {self.colors['bold']}MODULOS DISPONÍVEIS:{self.colors['reset']}
        - Recon Passivo: Coleta dados sem interagir com o alvo.
        - Subdomínios: Mapeia a superfície de ataque.
        - Scan de Rede: Identifica portas e serviços abertos.
        - Geolocalização: Localiza IPs geograficamente.
        """)
        input(f"\nPressione Enter para voltar...")

if __name__ == "__main__":
    app = DeepReconPro()
    app.start()
