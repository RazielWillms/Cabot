# Cabot- robô acadêmico para puxar notas no SIGA- Faculdade Uníntese- Raziel Haas Willms
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from tkinter import *

# automatiza a atualização do webdriver, do contrário seria necessário instalação manual a cada atualização do chrome
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)
wait = WebDriverWait(navegador, 300)  # define o tempo máximo que o sistema aguardará


def caminhoinicial():
    # xpaths para chegarmos na área de lançamento de notas
    navegador.maximize_window()
    navegador.get('https://unintese.sistemasiga.net/login')
    navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[1]/div/div/input').send_keys('04853343059')
    navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[2]/div/div/input').send_keys('04853343059')
    navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[3]/div/div/select').send_keys('Administração')
    navegador.find_element('xpath', '//*[@id="login-btn"]/i').click()
    navegador.find_element('xpath', '//*[@id="noprint"]/li[20]/a').click()
    elementolancamento = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="noprint"]/li[20]/ul/li[2]/a')))
    elementolancamento.click()


def puxarnota():
    # Inicio Lógica de 'puxada de nota'
    curso = open('cursos.txt', 'r')
    cursoid = curso.readlines()
    contadorcurso = 0  # padrão (0)

    for x in cursoid:
        if contadorcurso < len(cursoid):
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
            contadorcurso = contadorcurso + 1
        else:
            break
        contadorturma = 0  # padrão (0)
        for y in turmaid:
            if contadorturma < len(turmaid):
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
                discid = disc.readlines()
                contadorturma = contadorturma + 1
            else:
                break
            contadordisciplina = 0  # padrão (0)
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
                    break
    curso.close()


def sair():
    navegador.close()
    exit()


def painel():
    # xpaths para chegarmos na área de lançamento de notas
    caminhoinicial()

    # extração do texto do elemento Cursos
    navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
    time.sleep(1)
    elementocursos = navegador.find_element('class name', 'chosen-results').get_attribute("innerText")
    a = open('cursos.txt', 'w')
    a.write(elementocursos)
    a.close()

    # def responsável pela alteração do arquivo na pasta raiz do Cabot
    def alterartxt():
        entradateclado = selecionados.get("1.0", "end-1c")
        txtentrada = open('cursos.txt', 'w')
        txtentrada.write(entradateclado)
        txtentrada.close()
        puxarnota()

    def atualizartxttodos():
        # nova extração do texto do elemento Cursos
        navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
        elementocursosatualizado = navegador.find_element('class name', 'chosen-results').get_attribute("innerText")
        arquivoatualizado = open('cursos.txt', 'w')
        arquivoatualizado.write(elementocursosatualizado)
        arquivoatualizado.close()
        # atualização do campo visual
        selecionados.destroy()
        selecionados.__init__(font="Helvetica 10", height=20, width=75, bd=3)
        selecionados.insert(END, elementocursosatualizado)
        selecionados.grid(row=2, column=1, padx=5, pady=5)

    def puxartxttodos():
        # nova extração do texto do elemento Cursos
        navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
        elementocursosatualizado = navegador.find_element('class name', 'chosen-results').get_attribute("innerText")
        arquivoatualizado = open('cursos.txt', 'w')
        arquivoatualizado.write(elementocursosatualizado)
        arquivoatualizado.close()
        # atualização do campo visual
        selecionados.destroy()
        selecionados.__init__(font="Helvetica 10", height=20, width=75, bd=3)
        selecionados.insert(END, elementocursosatualizado)
        selecionados.grid(row=2, column=1, padx=5, pady=5)
        puxarnota()

    # inicio da janela/configurações
    janela = Tk()
    janela.title("Painel Cabot")
    janela.minsize(500, 300)  # width x height, define o tamanho mínimo da janela, pra facilitar a visualização
    janela.config(bg="lightgrey")

    # inicio disposição dos elementos no grid
    # imagem logo Cabot
    # Setting it up
    img = PhotoImage(file="resources/logo.png")
    logoimg = Label(janela, image=img)
    logoimg.grid(row=0, column=1, padx=5, pady=5)

    # txt com cursos encontrados no SIGA
    selecionados = Text(janela, font="Helvetica 10", height=20, width=75, bd=3)
    selecionados.insert(END, elementocursos)
    selecionados.grid(row=2, column=1, padx=5, pady=5)

    # 1º botão
    botaopuxar = Button(janela, text="Puxar nota parcial", command=alterartxt, bg="green", fg="white",
                        font="Helvetica 9 bold", width=18)
    botaopuxar.grid(column=1, row=5, sticky=W, padx=5, pady=2)
    # 2º botão
    botaotudo = Button(janela, text="Puxar nota completa", command=puxartxttodos, bg="black", fg="white",
                       font="Helvetica 9 bold", width=18)
    botaotudo.grid(column=1, row=6, sticky=W, padx=5, pady=2)
    # 3º botão
    botaofechar = Button(janela, text="  Fechar Sistema  ", command=sair, bg="red",
                         fg="white", font="Helvetica 9 bold", width=18)
    botaofechar.grid(column=1, row=7, sticky=W, padx=5, pady=2)
    # 4º botão
    botaoatualizar = Button(janela, text="Atualizar lista", command=atualizartxttodos,
                            bg="lightgrey", fg="black", font="Helvetica 9 bold", width=15)
    botaoatualizar.grid(column=1, row=5, sticky=E, padx=5, pady=2)

    # assinatura
    Label(janela, text="Criado por: Raziel Haas Willms", font="Helvetica 6 bold",
          bg="lightgrey").grid(row=7, column=1, padx=5, pady=5, sticky=E)

    janela.mainloop()  # responsável por manter a janela aberta


painel()
