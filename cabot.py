# Cabot- robô acadêmico para puxar notas no SIGA- Faculdade Uníntese- Raziel Haas Willms
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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
contadorc = 2

for x in cursoid:
    time.sleep(1)
    navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
    time.sleep(1)
    navegador.find_element('xpath', '//*[@id="curso_chosen"]/div/div/input').send_keys(cursoid[contadorc])
    time.sleep(2)
    # extração do texto do elemento turmas
    navegador.find_element('xpath', '//*[@id="turma_chosen"]/a').click()
    time.sleep(1)
    elementoturma = navegador.find_element('xpath', '//*[@id="turma_chosen"]/div/ul').get_attribute("innerText")
    b = open('turmas.txt', 'w')
    b.write(elementoturma)
    b.close()
    time.sleep(1)
    turma = open('turmas.txt', 'r')
    turmaid = turma.readlines()
    # inserir lógica para remoção das sentenças que denominam se a turma é ativa ou não
    contadort = 1
    if contadorc <= len(cursoid):
        contadorc = contadorc + 1
    else:
        break
    for y in turmaid:
        time.sleep(1)
        navegador.find_element('xpath', '//*[@id="turma_chosen"]/a').click()
        time.sleep(1)
        navegador.find_element('xpath', '//*[@id="turma_chosen"]/div/div/input').send_keys(turmaid[contadort])
        # extração do texto do elemento disciplinas
        navegador.find_element('xpath', '//*[@id="disciplina_chosen"]').click()
        time.sleep(1)
        elementodisciplina = navegador.find_element('xpath', '//*[@id="disciplina_chosen"]/div/ul'). \
            get_attribute("innerText")
        c = open('disciplinas.txt', 'w')
        c.write(elementodisciplina)
        c.close()
        time.sleep(1)
        disc = open('disciplinas.txt', 'r')
        discid = disc.readlines()
        contadord = 0
        if contadort <= len(turmaid):
            contadort = contadort + 1
        else:
            break
        for z in discid:
            print(len(discid))
            time.sleep(1)
            navegador.find_element('xpath', '//*[@id="disciplina_chosen"]').click()
            time.sleep(1)
            navegador.find_element('xpath', '//*[@id="disciplina_chosen"]/div/div/input').\
                send_keys(discid[contadord])
            time.sleep(1)
            navegador.find_element('xpath', '//*[@id="carregarNotas"]').click()
            time.sleep(5)
            navegador.find_element('xpath', '/html/body/div[6]/div/div/a').click()
            time.sleep(1)
            if contadord <= len(discid):
                contadord = contadord + 1
            else:
                break
time.sleep(5)
