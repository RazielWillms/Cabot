# Cabot- robô acadêmico para puxar notas no SIGA- Faculdade Uníntese- Raziel Haas Willms
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# automatiza a atualização do webdriver, do contrário seria necessário instalação manual a cada atualização do chrome
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)

# xpaths para chegarmos na área de lançamento de notas
navegador.maximize_window()
navegador.get('https://unintese.sistemasiga.net/login')
navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[1]/div/div/input').send_keys('Login')
navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[2]/div/div/input').send_keys('Senha')
navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[3]/div/div/select').send_keys('Administração')
navegador.find_element('xpath', '//*[@id="login-btn"]/i').click()
navegador.find_element('xpath', '//*[@id="noprint"]/li[20]/a').click()
wait = WebDriverWait(navegador, 300)
mediasfinais = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="noprint"]/li[20]/ul/li[2]/a')))
mediasfinais.click()

# extração do texto do elemento Cursos
navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
time.sleep(1)
elementocurso = navegador.find_element('class name', 'chosen-results').get_attribute("innerText")
a = open('cursos.txt', 'w')
a.write(elementocurso)
a.close()

# Lógica de 'puxada de nota'
curso = open('cursos.txt', 'r')
cursoid = curso.readlines()
contadorc = 2


for x in cursoid:
    selecaocurso = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="curso_chosen"]/a')))
    selecaocurso.click()
    time.sleep(1)
    navegador.find_element('xpath', '//*[@id="curso_chosen"]/div/div/input').send_keys(cursoid[contadorc])
    time.sleep(1)
    # extração do texto do elemento turmas
    turmas = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="turma_chosen"]/a')))
    turmas.click()
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
        selecaoturma = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="turma_chosen"]/a')))
        selecaoturma.click()
        time.sleep(1)
        navegador.find_element('xpath', '//*[@id="turma_chosen"]/div/div/input').send_keys(turmaid[contadort])
        # extração do texto do elemento disciplinas
        disciplinas = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="disciplina_chosen"]')))
        disciplinas.click()
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
            selecaodisciplina = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="disciplina_chosen"]')))
            selecaodisciplina.click()
            time.sleep(1)
            navegador.find_element('xpath', '//*[@id="disciplina_chosen"]/div/div/input').\
                send_keys(discid[contadord])
            # botão carregar nota
            carregarnota = wait.until(ec.element_to_be_clickable(navegador.find_element('xpath', '//*[''@id'
                                                                                                 '="carregarNotas"]')))
            carregarnota.click()
            # botão importar notas
            wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div/a')))
            navegador.switch_to.frame(0)
            importar = wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/fieldset/a')))
            importar.click()
            # pop-up ok
            wait.until(ec.alert_is_present(), 'O alerta não apareceu')
            alert = navegador.switch_to.alert
            alert.accept()
            # uncheck de checkbox to recalculate
            recalcular = wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/fieldset'
                                                                          '/input')))
            recalcular.click()
            time.sleep(20)
            # wait to checkbox reverse be clickable
            pass
            # save btn
            pass
            # confirm save btn
            pass
            # botão fechar janela para voltar ao loop
            navegador.switch_to.default_content()
            fechar = wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div/a')))
            fechar.click()
            time.sleep(1)
            if contadord <= len(discid):
                contadord = contadord + 1
            else:
                break

time.sleep(5)
