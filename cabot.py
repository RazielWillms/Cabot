#Cabot- robô acadêmico para puxar notas no SIGA- Faculdade Uníntese- Raziel Haas Willms
import pyautogui
import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)
time.sleep(20)
open('cursos.txt','a') 
open('turmas.txt','a') 
open('disciplinas.txt','a') 


#devem retornar os ID´s que ainda não foram utilizados, estudar selenium para tentar gerar o arquivo a partir do formulário exibido no SIGA
def ler_cursos():
    form = driver.find_element_by_xpath("//form[@action='" + formName + "']")
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
