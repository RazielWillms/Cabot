#Cabot- robô acadêmico para puxar notas no SIGA- Faculdade Uníntese- Raziel Haas Willms
import pyautogui
import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

navegador.get('https://unintese.sistemasiga.net/login')

#xpaths para chegarmos na área de lançamento de notas
navegador.find_element('xpath','/html/body/div[2]/form[1]/div[1]/div/div/input').send_keys('Login')
navegador.find_element('xpath','/html/body/div[2]/form[1]/div[2]/div/div/input').send_keys('Senha')
navegador.find_element('xpath','/html/body/div[2]/form[1]/div[3]/div/div/select').send_keys('Administração')
navegador.find_element('xpath','//*[@id="login-btn"]/i').click()
navegador.find_element('xpath','//*[@id="noprint"]/li[20]/a').click()
time.sleep(2)
navegador.find_element('xpath','//*[@id="noprint"]/li[20]/ul/li[2]/a').click()




a=open('cursos.txt','a') 
#a=open('turmas.txt','a') 
#a=open('disciplinas.txt','a') 
navegador.find_element('xpath','//*[@id="curso_chosen"]/a/span').click()
z= navegador.find_element('xpath','/html/body/div[3]/div[2]/div/form/fieldset/div[1]/div/div/div/ul')
print(z)
a.close()

#devem retornar os ID´s que ainda não foram utilizados, estudar selenium para tentar gerar o arquivo a partir do formulário exibido no SIGA
def ler_cursos():
    z = open('cursos.txt','r+')
    cursoid=z.readlines()
    print(cursoid)
    cursoid=[x.strip('\n') for x in cursoid]
    print(cursoid)
    z.close()
    for linha in cursoid:
        print(linha)
    return cursoid

def ler_turmas():
    z = open('turmas.txt','r+')
    return turmaid

def ler_disciplinas():
    z = open('disciplinas.txt','r+')
    return disciplinaid


x=ler_cursos()

#trocar coordenadas por identificação do campo a ser selecionado/preebchido
pyautogui.click(1291, 288)
pyautogui.write(x)
time.sleep(1)
pyautogui.press('enter')

time.sleep(50)
