# Cabot- robô acadêmico para puxar notas no SIGA- Faculdade Uníntese- Raziel Haas Willms
import os
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
elementoLancamento = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="noprint"]/li[20]/ul/li[2]/a')))
elementoLancamento.click()

# Criação do arquivo de Backup
bkp = open('bkpCurso.txt', 'w')
bkp.close()


def puxarnota():
    # extração do texto do elemento Cursos
    navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
    time.sleep(1)
    elemento = navegador.find_element('class name', 'chosen-results').get_attribute("innerText")
    a = open('cursos.txt', 'w')
    a.write(elemento)
    a.close()
    # Lógica de 'puxada de nota'
    curso = open('cursos.txt', 'r')
    cursoid = curso.readlines()
    contadorcurso = 0  # padrão (0)
    contadorturma = 0  # padrão (0)
    contadordisciplina = 0  # padrão (0)

    # verificar arquivo bkp e setar x na posição de onde parou ou pular, a ideia é registrar quais cursos já foram
    # puxados e continuar de onde parou em caso de erro. Vou fazer apenas com o Curso já que é o laço maior, se for
    # fácil de implementar posso adicionar nos demais também.

    print("arquivo criado")
    os.remove('bkpCurso.txt')
    print("arquivo removido")
    time.sleep(10)

    for x in cursoid:
        d = open('bkpCurso.txt', 'w')
        d.write(x)
        d.close()
        if contadorcurso < len(cursoid):
            contadorcurso = contadorcurso + 1
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
            turmaid = turma.readlines()
        else:
            break
        for y in turmaid:
            if contadorturma < len(turmaid):
                contadorturma = contadorturma + 1
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
                elemento = navegador.find_element('xpath', '//*[@id="disciplina_chosen"]/div/ul').\
                    get_attribute("innerText")
                c = open('disciplinas.txt', 'w')
                c.write(elemento)
                c.close()
                time.sleep(1)
                disc = open('disciplinas.txt', 'r')
                discid = disc.readlines()
            else:
                contadorturma = 0
                break
            for z in discid:
                if contadordisciplina < len(discid):
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
                    elemento = wait.until(ec.element_to_be_clickable
                                          (navegador.find_element('xpath', '//*[''@id''="carregarNotas"]')))
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
                    elemento = wait.until(
                        ec.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/fieldset'
                                                              '/input')))
                    elemento.click()
                    # wait to checkbox reverse be clickable
                    elemento = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="btnLancado"]')))
                    elemento.click()
                    # conferir todas as checkbox para deixá-las marcadas, usar navegador.find_element().is_selected()
                    # para conferir antes de clicar
                    elemento = navegador.find_elements(By.CLASS_NAME, 'lancadoAluno')
                    for w in elemento:
                        selecionado = w.is_selected()
                        if not selecionado:
                            w.click()
                            time.sleep(1)
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
                    contadordisciplina = contadordisciplina + 1
                else:
                    contadordisciplina = 0
                    break


# inicio do programa
puxarnota()
# setar bkp como vazio ou excluí-lo
os.remove('bkpCurso.txt')
# Criar encerramento da rotina, questionando se o usuário deseja realizar novamente.
recomecar = input("O programa concluiu com êxito o lançamento de notas no sistema SIGA, deseja fazer a importação e "
                  "lançamento de notas novamente? (1-sim) (2-não)")
if recomecar == 1 or "sim":
    puxarnota()
else:
    print("Certo, até mais!")
    time.sleep(5)
    exit()
