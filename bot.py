# Import for the Web Bot
import requests
import pandas as pd
from datetime import datetime
from botcity.web import WebBot, Browser, By
import tkinter as tk
from tkinter import simpledialog, messagebox

# Import for integration with BotCity Maestro SDK
from botcity.maestro import *

# Disable errors if we are not connected to Maestro
BotMaestroSDK.RAISE_NOT_CONNECTED = False

from webdriver_manager.chrome import ChromeDriverManager

class Bot(WebBot):

    def __init__(self):
        super().__init__()  
        self.dados = None  

    def config(self):
        self.headless = False

        # Uncomment to change the default Browser to Firefox
        self.browser = Browser.CHROME

        # Uncomment to set the WebDriver path
        self.driver_path = ChromeDriverManager().install()

    def url_site(self, url="https://sistemas1.sefaz.ma.gov.br/download-nfe/"):
        try:
            self.browse(url)
        except Exception as ex:
            print('Erro ao acessar a url da classe:', ex)
            self.save_screenshot('error.png')

    def verificar_site(self, url):
        try:
            response = requests.get(url, verify=False) 
            if response.status_code == 200:
                print("O site está operando.")
                return True
            else:
                print(f"O site retornou status {response.status_code}. Não está operando.")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Ocorreu um erro ao verificar o site: {e}")
            return False   

    def preencher_formulario(self):
        self.planilha = r"resources\Dados_Empresas.xlsx"
        df = pd.read_excel(self.planilha)

        for index, row in df.iterrows():
            ie_empresa = str(row["IE Empresa"])
            cpf_socio = str(row["CPF Sócio"])
            protocolo_dief = str(row["Último Protocolo DIEF"])
            data_inicial = str(row["Data Inicial"]) 
            data_final = str(row["Data Final"])      
               
            while len(self.find_elements('//*[@id="form1:j_id6_body"]/table[1]/tbody/tr[1]/td[2]/input', By.XPATH)) < 1:
                self.wait(1000)
                print('Carregando...')            

            
            self.preencher_campos(ie_empresa, cpf_socio, protocolo_dief, data_inicial, data_final)

            
            captcha_text = self.entrada_captcha()
            print(f"O usuário digitou o CAPTCHA: {captcha_text}")

            
            captcha_xpath = '//*[@id="form1:cap"]/tbody/tr[2]/td/div/input'
            elemento_captcha = self.find_element(captcha_xpath, By.XPATH)
            elemento_captcha.click()
            self.paste(captcha_text)
            self.wait(1000) 
            
            
            botao_baixar_xpath = '//*[@id="form1:j_id6_body"]/table[4]/tbody/tr/td[2]/input' 
            botao_baixar = self.find_element(botao_baixar_xpath, By.XPATH)
            botao_baixar.click()
            self.wait(1000) 

            botao_limpar_xpath = '//*[@id="form1:j_id6_body"]/table[4]/tbody/tr/td[1]/input'  
            botao_limpar = self.find_element(botao_limpar_xpath, By.XPATH)
            botao_limpar.click()
            self.wait(1000) 
            
        messagebox.showinfo("Processo Concluído", "O processo foi finalizado com sucesso!")

    def preencher_campos(self, ie_empresa, cpf_socio, protocolo_dief, data_inicial, data_final):
        elemento_ie = self.find_element('//*[@id="form1:j_id6_body"]/table[1]/tbody/tr[1]/td[2]/input', By.XPATH)
        elemento_ie.click()
        self.paste(ie_empresa)
        self.wait(1000)

        elemento_cpf = self.find_element('//*[@id="form1:j_id6_body"]/table[1]/tbody/tr[2]/td[2]/input', By.XPATH)
        elemento_cpf.click()
        self.paste(cpf_socio)
        self.wait(1000)

        elemento_protocolo = self.find_element('//*[@id="form1:j_id6_body"]/table[1]/tbody/tr[3]/td[2]/input', By.XPATH)
        elemento_protocolo.click()
        self.paste(protocolo_dief)
        self.wait(1000)

        self.execute_javascript(f"""
            var campo = document.evaluate('//*[@id="form1:dtIniInputDate"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            campo.value = '{data_inicial}';
            campo.dispatchEvent(new Event('input'));
            campo.dispatchEvent(new Event('change'));
        """)
        self.wait(2000)
        
        # Preencher a Data Final
        self.execute_javascript(f"""
            var campo = document.evaluate('//*[@id="form1:dtFinInputDate"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            campo.value = '{data_final}';
            campo.dispatchEvent(new Event('input'));
            campo.dispatchEvent(new Event('change'));
        """)
        self.wait(2000)  

    def entrada_captcha(self):
        
        root = tk.Tk()
        root.withdraw()  
        
        captcha = simpledialog.askstring("CAPTCHA", "Digite o CAPTCHA que aparece na tela:", parent=root)
        return captcha if captcha is not None else ""

    def entrando_iframes(self):
        self.wait(1000)
        
        iframe = self.find_element(selector='/html/frameset1', by=By.XPATH)
        
        self.enter_iframe(iframe)

        self.wait(1000)

        iframe2 = self.find_element('/html/frameset/frame', By.XPATH)
        self.enter_iframe(iframe2)

    def action(self, execution=None):
        maestro = BotMaestroSDK.from_sys_args()
        execution = maestro.get_execution()

        maestro.alert(
            task_id=execution.task_id,
            title="Alerta!",
            message="Bot Desafio 6 - LG: Iniciado!",
            alert_type=AlertType.INFO
        )

        finishion_status = AutomationTaskFinishStatus.SUCCESS
        finishi_message = 'Tarefa Finalizada'
        
        print(f"Task ID is: {execution.task_id}")
        print(f"Task Parameters are: {execution.parameters}")
        
        url = 'https://sistemas1.sefaz.ma.gov.br/download-nfe'
        if not self.verificar_site(url):
            print("Finalizando o bot devido à indisponibilidade do site.")
            return  

        try:
            self.config()
            self.url_site(url)
            self.entrando_iframes()
            self.preencher_formulario()

        except Exception as ex:
            print('Erro', ex)

            finishion_status = AutomationTaskFinishStatus.FAILED
            finishi_message = 'Tarefa Finalizada com erro!'

            self.save_screenshot('erro.png')
        finally:
            self.wait(2000)
            self.stop_browser()

        maestro.finish_task(
            task_id=execution.task_id,
            status= finishion_status,
            message= finishi_message
        
    )

    def not_found(self, label):
        print(f"Element not found: {label}")

if __name__ == '__main__':
    Bot.main()
