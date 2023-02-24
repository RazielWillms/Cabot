# Cabot- robô acadêmico para puxar notas no SIGA- Faculdade Uníntese- Raziel Haas Willms
import pyautogui
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# automatiza a atualização do webdriver, do contrário seria necessário instalação manual a cada atualização do chrome
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

navegador.get('https://unintese.sistemasiga.net/login')

# xpaths para chegarmos na área de lançamento de notas
navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[1]/div/div/input').send_keys('04853343059')
navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[2]/div/div/input').send_keys('04853343059')
navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[3]/div/div/select').send_keys('Administração')
navegador.find_element('xpath', '//*[@id="login-btn"]/i').click()
navegador.find_element('xpath', '//*[@id="noprint"]/li[20]/a').click()
time.sleep(2)
navegador.find_element('xpath', '//*[@id="noprint"]/li[20]/ul/li[2]/a').click()

# extração do texto do elemento Cursos
navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
elementocurso = navegador.find_element('class name', 'chosen-results').get_attribute("innerText")
a = open('cursos.txt', 'w')
a.write(elementocurso)
a.close()

# Lógica de 'puxada de nota'
curso = open('cursos.txt', 'r')
cursoid = curso.readlines()
contadorc = 0
contadort = 0
contadord = 0

for x in cursoid:
    contadorc = contadorc+1
    navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
    #navegador.find_element('xpath','//*[@id="curso_chosen"]/div/div/input').send_keys(cursoid[contadorc])
    pyautogui.write(cursoid[contadorc])
    time.sleep(2)
    pyautogui.press('enter')
    time.sleep(5)

    # extração do texto do elemento turmas
    navegador.find_element('xpath', '//*[@id="turma_chosen"]/a').click()
    elementoturma = navegador.find_element('xpath', '//*[@id="turma_chosen"]/div/ul').get_attribute("innerText")
    b = open('turmas.txt', 'w')
    b.write(elementoturma)
    b.close()
    time.sleep(1)
    turma = open('turmas.txt', 'r')
    turmaid = turma.readlines()
    # inserir lógica para remoção das sentenças que denominam se a turma é ativa ou não
    for y in turmaid:
        time.sleep(1)
        contadort = contadort+1
        navegador.find_element('xpath', '//*[@id="turma_chosen"]/a').click()
        #navegador.find_element('xpath', '//*[@id="turma_chosen"]/div/div/input').send_keys(turmaid[contadort])
        pyautogui.write(turmaid[contadort])
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(500)
else:
    print('nenhum curso cadastrado')
    time.sleep(500)
