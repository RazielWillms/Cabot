# Cabot- robô acadêmico para puxar notas no SIGA- Faculdade Uníntese- Raziel Haas Willms
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys

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
elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="noprint"]/li[20]/ul/li[2]/a')))
elemento.click()

# extração do texto do elemento Cursos
navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
time.sleep(1)
elemento = navegador.find_element('class name', 'chosen-results').get_attribute("innerText")
a = open('cursos.txt', 'w')
a.write(elemento)
a.close()

# Lógica de 'puxada de nota'
curso = open('cursos.txt', 'r')
cursoId = curso.readlines()
contadorCurso = 0  # padrão (0)
contadorTurma = 0  # padrão (0)
contadorDisciplina = 0  # padrão (0)

# verificar bkp e setar contadores posição de onde parou ou pular
pass

for x in cursoId:
    if contadorCurso < len(cursoId):
        contadorCurso = contadorCurso + 1
        elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="curso_chosen"]/a')))
        elemento.click()
        time.sleep(1)
        elemento = navegador.find_element('xpath', '//*[@id="curso_chosen"]/div/div/input')
        elemento.send_keys(x)
        time.sleep(1)
        elemento.send_keys(Keys.ENTER)
        time.sleep(1)
        # extração do texto do elemento turmas
        elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="turma_chosen"]/a')))
        elemento.click()
        time.sleep(1)
        elemento = navegador.find_element('xpath', '//*[@id="turma_chosen"]/div/ul').get_attribute("innerText")
        b = open('turmas.txt', 'w')
        b.write(elemento)
        b.close()
        time.sleep(1)
        turma = open('turmas.txt', 'r')
        turmaId = turma.readlines()
    else:
        break
    for y in turmaId:
        if contadorTurma < len(turmaId):
            contadorTurma = contadorTurma + 1
            elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="turma_chosen"]/a')))
            elemento.click()
            time.sleep(1)
            elemento = navegador.find_element('xpath', '//*[@id="turma_chosen"]/div/div/input')
            elemento.send_keys(y)
            time.sleep(1)
            elemento.send_keys(Keys.ENTER)
            time.sleep(1)
            # extração do texto do elemento disciplinas
            elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="disciplina_chosen"]')))
            elemento.click()
            time.sleep(1)
            elemento = navegador.find_element('xpath', '//*[@id="disciplina_chosen"]/div/ul'). \
                get_attribute("innerText")
            c = open('disciplinas.txt', 'w')
            c.write(elemento)
            c.close()
            time.sleep(1)
            disc = open('disciplinas.txt', 'r')
            discId = disc.readlines()
        else:
            contadorTurma = 0
            break
        for z in discId:
            if contadorDisciplina < len(discId):
                elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="disciplina_chosen"]')))
                elemento.click()
                time.sleep(1)
                elemento.click()
                time.sleep(1)
                elemento = navegador.find_element('xpath', '//*[@id="disciplina_chosen"]/div/div/input')
                elemento.send_keys(z)
                time.sleep(1)
                elemento.send_keys(Keys.ENTER)
                time.sleep(1)
                # botão carregar médias
                elemento = wait.until(ec.element_to_be_clickable(navegador.
                                                                 find_element('xpath', '//*[''@id''="carregarNotas"]')))
                elemento.click()
                # botão importar notas
                wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div/a')))
                navegador.switch_to.frame(0)
                elemento = wait.until(ec.element_to_be_clickable((By.XPATH,
                                                                  '/html/body/div[3]/div/div/form/fieldset/a')))
                elemento.click()
                # pop-up ok
                wait.until(ec.alert_is_present(), 'O alerta não apareceu')
                elemento = navegador.switch_to.alert
                elemento.accept()
                # uncheck de checkbox to recalculate
                elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/fieldset'
                                                                            '/input')))
                elemento.click()
                # wait to checkbox reverse be clickable
                elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="btnLancado"]')))
                elemento.click()
                # conferir todas as checkbox para deixá-las marcadas, usar navegador.find_element().is_selected()
                pass
                # save btn
                elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="noprint"]/button')))
                elemento.click()
                # confirm save btn
                elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[2]/a[1]')))
                elemento.click()
                # botão fechar janela para voltar ao loop
                navegador.switch_to.default_content()
                elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div/a')))
                elemento.click()
                time.sleep(1)
                contadorDisciplina = contadorDisciplina + 1
            else:
                contadorDisciplina = 0
                break

time.sleep(5)
