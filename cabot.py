# Cabot- robô acadêmico para puxar notas no SIGA- Faculdade Uníntese- Raziel Haas Willms
import pyautogui
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

#automatiza a atualização do webdriver, do contrário seria necessário instalação manual a cada atualização do chrome
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

#extração do texto do elemento Cursos
navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
z = navegador.find_element('class name', 'chosen-results').get_attribute("innerText")
a = open('cursos.txt', 'a')
a.write(z)
a.close()

#criação de arquivos base para vetorização dos cursos, turmas e disciplinas
#a = open('cursos.txt', 'a')
#a = open('turmas.txt','a')
#a = open('disciplinas.txt','a')
#a.close()

# Devem retornar vetores com todas as possibilidades de curso, turma e disciplina
def ler_cursos(cursoid=None):
    #a = open('cursos.txt', 'r+')
    #with open("cursos.txt", "r") as f:
    #    string = f.read()
    #a.write(string)
    #cursoid = a.readlines()
    #cursoid = [x.strip('\n') for x in cursoid]
    #for linha in cursoid:
    #    print(linha)
    #    print('próximo valor na lista')
    #a.close()
    #with open(a) as f:
    #    for x, linha in enumerate(f):
    #        if x == 3:
    #            print('numero')
    #            print(enumerate)
    #            print('linha')
    #            print(linha)
    #            print('x')
    #            print(x)
    #            print('f')
    #            print(f)
    return cursoid


#def ler_turmas(turmaid=None):
#    a = open('turmas.txt', 'r+')
#    return turmaid


#def ler_disciplinas(disciplinaid=None):
#    a = open('disciplinas.txt', 'r+')
#    return disciplinaid


#ler_cursos()

# trocar coordenadas por identificação do campo a ser selecionado/preebchido
#pyautogui.click(1291, 288)
#pyautogui.write(x)
#time.sleep(1)
#pyautogui.press('enter')

time.sleep(50)
