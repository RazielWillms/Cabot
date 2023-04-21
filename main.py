# Cabot- robô acadêmico para puxar notas no SIGA- Faculdade Uníntese- Raziel Haas Willms
import os
from selenium.webdriver import ChromeOptions
import time
import tkinter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from tkinter import *
from cryptography.fernet import Fernet
from threading import Thread

# automatiza a atualização do webdriver, do contrário seria necessário instalação manual a cada atualização
# do chrome
servico = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=servico)
chrome_options = ChromeOptions()
chrome_options.add_argument('--disable-infobars')
aguardar = WebDriverWait(navegador, 300)  # define o tempo máximo que o sistema aguardará

# Cores utilizadas
cor0 = "#976daf"  # roxo
cor1 = "#feffff"  # branco
cor2 = "#56856f"  # verde
cor3 = "#953e44"  # vermelho
cor4 = "#403d3d"  # cinza escuro
cor5 = "#D3D3D3"  # cinza claro


def criptografar():
    # Gera uma chave de criptografia
    chave = Fernet.generate_key()

    # Salva a chave em um arquivo
    with open('chave.chave', 'wb') as arquivo_senha:
        arquivo_senha.write(chave)

    # Carrega a chave do arquivo
    with open('chave.chave', 'rb') as arquivo_senha:
        chave = arquivo_senha.read()

    # Cria um objeto Fernet com a chave
    fernet = Fernet(chave)

    # Criptografa o arquivo
    with open('lembrar.txt', 'rb') as file:
        original = file.read()
    encrypted = fernet.encrypt(original)

    # Salva o arquivo criptografado
    with open('lembrar_criptografado.txt', 'wb') as file:
        file.write(encrypted)

    # apaga o arquivo desprotegido temporário
    os.remove("lembrar.txt")


# compara o que foi escrito na turma e remove 'turmas ativas', 'turmas encerradas' e 'turmas não iniciadas'
def alterar_txt_turma():
    textos_a_serem_excluidos = ["Turmas ativas", "Turmas encerradas", "Turmas não inciadas"]

    with open('turmas.txt', 'r+') as arquivo:
        linhas = arquivo.readlines()
        arquivo.seek(0)
        novas_linhas = []
        for linha in linhas:
            if not any(texto in linha for texto in textos_a_serem_excluidos):
                novas_linhas.append(linha)
        arquivo.writelines(novas_linhas)
        arquivo.truncate()


class App:
    def __init__(self):
        super().__init__()
        # criando uma thread
        self.painel_login = Tk()

        # INÍNCIO PAINEL DE LOGIN --------------------------------------------------
        # recebe os dados de acesso do usuário e utiliza no caminho inicial
        self.painel_login.title("Login Siga")

        # config do painel
        self.painel_login.resizable(False, False)
        self.painel_login.config(bg=cor5, bd=1, padx=5, pady=5)
        self.painel_login.iconbitmap("./recursos/icone.ico")

        # início disposição dos elementos
        # txt info´s
        self.info_txt = Label(self.painel_login, text="Informe os dados de acesso no SIGA:",
                              font="Helvetica 9 bold", bg=cor5)
        self.info_txt.grid(row=0, column=1)

        # campos de login e senha
        self.login = Label(self.painel_login, text="Login:", height=1, anchor=NW, font='Ivy 10 bold', bg=cor5, fg=cor4)
        self.login.grid(row=1, column=0)
        self.recebe_login = Entry(self.painel_login, width=25, justify='left', font=("", 15), highlightthickness=1,
                                  relief="solid")
        self.recebe_login.grid(row=1, column=1)

        self.senha = Label(self.painel_login, text="Senha:", height=1, anchor=NW, font='Ivy 10 bold', bg=cor5, fg=cor4)
        self.senha.grid(row=2, column=0)
        self.recebe_senha = Entry(self.painel_login, show='*', width=25, justify='left', font=("", 15),
                                  highlightthickness=1, relief="solid")
        self.recebe_senha.grid(row=2, column=1)

        self.conferir_salvo()

        self.marcado_salvar = IntVar()
        self.checkbox_salvar = Checkbutton(self.painel_login, text="Lembrar-me", bg=cor5, font='Ivy 8 bold',
                                           variable=self.marcado_salvar)
        self.checkbox_salvar.grid(row=3, column=1, sticky=W)

        self.botao_confirmar = Button(self.painel_login, command=self.caminho_inicial, text="Entrar", width=39,
                                      height=2, bg=cor2, fg=cor1, font='Ivy 8 bold', relief=RAISED, overrelief=RIDGE)
        self.botao_confirmar.grid(row=4, column=1, pady=2, padx=5)

        self.painel_login.mainloop()
        # FIM PAINEL DE LOGIN --------------------------------------------------

        # INÍCIO PAINEL CABOT --------------------------------------------------
        # extração do texto do elemento Cursos
        navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
        elemento_web_cursos = navegador.find_element('class name', 'chosen-results').get_attribute("innerText")
        a = open('cursos.txt', 'w')
        a.write(elemento_web_cursos)
        a.close()
        lista = open('cursos.txt', 'r')
        self.listbox = lista.readlines()
        lista.close()

        # inicio do painel/configurações
        self.painel = Tk()
        self.painel.title("Painel Cabot")
        self.painel.minsize(500, 300)  # width x height, define o tamanho mínimo da painel, pra facilitar a visualização
        self.painel.resizable(False, False)
        self.painel.config(bg=cor5, bd=1, padx=5, pady=5)

        # inicio disposição dos elementos no grid

        # imagem logo Cabot
        img = PhotoImage(file="./recursos/logo.png")
        logo_img = Label(self.painel, image=img, bd=1)
        logo_img.grid(row=0, column=1)

        self.img_redefinir = PhotoImage(file="./recursos/refresh_icon2.png")

        self.painel.iconbitmap("./recursos/icone.ico")

        # txt info´s
        self.info_txt = Label(self.painel, text="*Selecione os cursos que deseja efetuar o processamento de notas*",
                              font="Helvetica 9 bold", bg=cor5)
        self.info_txt.grid(row=1, column=1)

        # scrollbar config/vinculo com listbox
        self.frame_scrollbar = Frame(self.painel)
        self.scrollbar = Scrollbar(self.frame_scrollbar, orient=VERTICAL)

        # listbox com cursos encontrados no SIGA
        self.selecionados = Listbox(self.frame_scrollbar, font="Helvetica 10", height=20, width=75, bd=0,
                                    selectmode=tkinter.MULTIPLE, cursor="plus", selectbackground=cor0,
                                    activestyle='none', yscrollcommand=self.scrollbar.set)

        # config´s scrollbar
        self.scrollbar.config(command=self.selecionados.yview)
        self.scrollbar.grid(sticky=tkinter.NS, column=2, row=2)
        self.frame_scrollbar.grid(row=2, column=1, padx=5, pady=5)

        for elementos in self.listbox:
            self.selecionados.insert(END, elementos)
        self.selecionados.delete(0, last=None)
        self.selecionados.grid(row=2, column=1, padx=5, pady=5)

        # 1º botão
        self.botao_puxar = Button(self.painel, text="Puxar Selecionado", command=self.alterar_txt, bg=cor2, fg=cor1,
                                  font="Helvetica 9 bold", width=18, relief=RAISED, overrelief=RIDGE)
        self.botao_puxar.grid(column=1, row=5, sticky=W, pady=2, padx=5)

        # 2º botão
        self.botao_todos = Button(self.painel, text="Puxar Todos", command=self.redefinir_txt_puxar, bg="#292625",
                                  fg=cor1, font="Helvetica 9 bold", width=18, relief=RAISED, overrelief=RIDGE)
        self.botao_todos.grid(column=1, row=6, sticky=W, pady=2, padx=5)
        # 3º botão
        self.botao_fechar = Button(self.painel, text="  Fechar Sistema  ", command=self.sair, bg=cor3, fg=cor1,
                                   font="Helvetica 9 bold", width=18, relief=RAISED, overrelief=RIDGE)
        self.botao_fechar.grid(column=1, row=7, sticky=NW, pady=2, padx=5)
        # 4º botão
        self.botao_atualizar = Button(self.painel, text=" Redefinir lista", image=self.img_redefinir,
                                      compound=tkinter.LEFT, command=self.redefinir_txt, bg=cor5, fg="black",
                                      font="Helvetica 9 bold", relief=RAISED, overrelief=RIDGE)
        self.botao_atualizar.grid(column=1, row=5, sticky=E, padx=5)

        # assinatura antiga
        # Label(self.painel, text="Criado por: Raziel e Palf", font="Helvetica 7 bold",
        #     bg="lightgrey").grid(row=7, column=1, sticky=SE)

        # assinatura animada
        img0 = PhotoImage(file="./recursos/rimg0.png")
        b0 = Label(self.painel, text="Criado por: Raziel e Palf", font="Helvetica 7 bold", bg="lightgrey", image=img0)

        b0.grid(row=7, column=1, sticky=SE)

        self.painel.mainloop()  # responsável por manter a painel aberta
        # FIM PAINEL CABOT --------------------------------------------------

    def caminho_inicial(self):
        try:
            login_siga = self.recebe_login.get()
            senha_siga = self.recebe_senha.get()
            # xpaths para chegarmos na área de lançamento de notas
            navegador.maximize_window()
            navegador.get('https://unintese.sistemasiga.net/login')
            navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[1]/div/div/input').send_keys(login_siga)
            navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[2]/div/div/input').send_keys(senha_siga)
            navegador.find_element('xpath', '/html/body/div[2]/form[1]/div[3]/div/div/select').send_keys(
                'Administração')
            navegador.find_element('xpath', '//*[@id="login-btn"]/i').click()
            navegador.find_element('xpath', '//*[@id="noprint"]/li[20]/a').click()
            elemento_lancamento = aguardar.until(
                ec.element_to_be_clickable((By.XPATH, '//*[@id="noprint"]/li[20]/ul/li[2]/a')))
            elemento_lancamento.click()
            self.painel_login.destroy()
            # verifica se pedimos para lembrar do usuário informado e realiza o processo de criptografia da senha
            if self.marcado_salvar.get() == 1:
                # vamos destruir o arquivo caso já exista uma senha salva
                if os.path.exists("lembrar_criptografado.txt"):
                    os.remove("lembrar_criptografado.txt")
                # criação do arquivo temporário de senha
                d = open('lembrar.txt', 'w')
                d.close()
                # abertura para inserção dos dados informados
                with open('lembrar.txt', 'a') as e:
                    e.write(login_siga)
                    e.write("\n")
                    e.write(senha_siga)
                # chamada para criptografarmos o arquivo temporário
                criptografar()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            self.info_txt.config(text="Tente de novo...", font="Helvetica 9 bold", bg="lightgrey", fg="red")
            raise

    def puxar_nota(self):
        try:
            self.botao_fechar.config(text='Aguarde...', relief=SUNKEN, bg="#292625", command='')
            self.botao_todos.config(text='Aguarde...', relief=SUNKEN, bg="#292625", command='')
            self.botao_puxar.config(text='Aguarde...', relief=SUNKEN, bg="#292625", command='')
            self.botao_atualizar.config(text='Aguarde...', relief=SUNKEN, bg="#292625", command='')
            # self.botao_fechar.update()
            # Inicio Lógica de 'puxada de nota'
            curso_txt = open('cursos.txt', 'r')
            curso_lista = curso_txt.readlines()
            curso_txt.close()
            contador_curso = 0  # padrão (0)

            for nome_curso in curso_lista:
                if contador_curso < len(curso_lista):
                    elemento_web = aguardar.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="curso_chosen"]/a')))
                    elemento_web.click()
                    elemento_web = navegador.find_element('xpath', '//*[@id="curso_chosen"]/div/div/input')
                    elemento_web.send_keys(nome_curso)
                    elemento_web.send_keys(Keys.ENTER)
                    time.sleep(1)
                    # extração do texto do elemento turmas
                    elemento_web = aguardar.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="turma_chosen"]/a')))
                    elemento_web.click()
                    elemento_web = navegador.find_element('xpath', '//*[@id="turma_chosen"]/div/ul') \
                        .get_attribute("innerText")
                    b = open('turmas.txt', 'w')
                    b.write(elemento_web)
                    b.close()
                    alterar_txt_turma()
                    turma_txt = open('turmas.txt', 'r')
                    turma_lista = turma_txt.readlines()
                    turma_txt.close()
                    contador_curso = contador_curso + 1
                else:
                    break
                contador_turma = 0  # padrão (0)
                for nome_turma in turma_lista:
                    if contador_turma < len(turma_lista):
                        elemento_web = aguardar.until(ec.element_to_be_clickable((By.XPATH,
                                                                                  '//*[@id="turma_chosen"]/a')))
                        elemento_web.click()
                        elemento_web = navegador.find_element('xpath', '//*[@id="turma_chosen"]/div/div/input')
                        elemento_web.send_keys(nome_turma)
                        elemento_web.send_keys(Keys.ENTER)
                        time.sleep(1)
                        # extração do texto do elemento divisão
                        elemento_web = aguardar.until(ec.element_to_be_clickable
                                                      ((By.XPATH, '//*[@id="divisao_chosen"]/a')))
                        elemento_web.click()
                        elemento_web = navegador.find_element('xpath', '//*[@id="divisao_chosen"]/div/ul'). \
                            get_attribute("innerText")
                        c = open('periodo.txt', 'w')
                        c.write(elemento_web)
                        c.close()
                        periodo_txt = open('periodo.txt', 'r')
                        periodo_lista = periodo_txt.readlines()
                        periodo_txt.close()
                    else:
                        break
                    contador_periodo = 0  # padrão (0)
                    for nome_periodo in periodo_lista:
                        if contador_periodo < len(periodo_lista):
                            elemento_web = aguardar.until(
                                ec.element_to_be_clickable((By.XPATH, '//*[@id="divisao_chosen"]')))
                            elemento_web.click()
                            elemento_web = navegador.find_element('xpath', '//*[@id="divisao_chosen"]/div/div/input')
                            elemento_web.send_keys(nome_periodo)
                            elemento_web.send_keys(Keys.ENTER)
                            time.sleep(1)
                            # extração do texto do elemento disciplinas
                            elemento_web = aguardar.until(ec.element_to_be_clickable
                                                          ((By.XPATH, '//*[@id="disciplina_chosen"]')))
                            elemento_web.click()
                            elemento_web = navegador.find_element('xpath', '//*[@id="disciplina_chosen"]/div/ul'). \
                                get_attribute("innerText")
                            d = open('disciplinas.txt', 'w')
                            d.write(elemento_web)
                            d.close()
                            disciplina_txt = open('disciplinas.txt', 'r')
                            disciplina_lista = disciplina_txt.readlines()
                            disciplina_txt.close()
                            contador_periodo = contador_periodo + 1
                        else:
                            break
                        contador_disciplina = 0  # padrão (0)
                        for nome_disciplina in disciplina_lista:
                            if contador_disciplina < len(disciplina_lista):
                                elemento_web = aguardar.until(ec.element_to_be_clickable
                                                              ((By.XPATH, '//*[@id="disciplina_chosen"]')))
                                elemento_web.click()
                                elemento_web.click()
                                elemento_web = navegador.find_element('xpath',
                                                                      '//*[@id="disciplina_chosen"]/div/div/input')
                                time.sleep(1)
                                elemento_web.send_keys(nome_disciplina)
                                elemento_web.send_keys(Keys.ENTER)
                                # botão carregar médias
                                elemento_web = aguardar.until(ec.element_to_be_clickable
                                                              (navegador.find_element
                                                               ('xpath', '//*[''@id''="carregarNotas"]')))
                                elemento_web.click()
                                # botão importar notas
                                aguardar.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[6]/div/div/a')))
                                navegador.switch_to.frame(0)
                                elemento_web = aguardar.until(ec.element_to_be_clickable
                                                              ((By.XPATH, '/html/body/div[3]/div/div/form/fieldset/a')))
                                elemento_web.click()
                                # dá ok/sim no pop-up
                                aguardar.until(ec.alert_is_present(), 'O alerta não apareceu')
                                elemento_web = navegador.switch_to.alert
                                elemento_web.accept()
                                # desmarca o checkbox para recalcular
                                elemento_web = aguardar.until(
                                    ec.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/form/fieldset'
                                                                          '/input')))
                                elemento_web.click()
                                # aciona a inversão de puxar nota
                                elemento_web = aguardar.until(ec.element_to_be_clickable((By.XPATH,
                                                                                          '//*[@id="btnLancado"]')))
                                elemento_web.click()
                                # confere todas as checkbox para deixá-las marcadas
                                elemento_web = navegador.find_elements(By.CLASS_NAME, 'lancadoAluno')
                                for w in elemento_web:
                                    selecionado = w.is_selected()
                                    if not selecionado:
                                        w.click()
                                # save btn
                                elemento_web = aguardar.until(ec.element_to_be_clickable
                                                              ((By.XPATH, '//*[@id="noprint"]/button')))
                                elemento_web.click()
                                # confirm save btn
                                elemento_web = aguardar.until(ec.element_to_be_clickable
                                                              ((By.XPATH, '/html/body/div[5]/div[2]/a[1]')))
                                elemento_web.click()
                                # botão fechar painel para voltar ao loop
                                navegador.switch_to.default_content()
                                elemento_web = aguardar.until(ec.element_to_be_clickable
                                                              ((By.XPATH, '/html/body/div[6]/div/div/a')))
                                elemento_web.click()
                                contador_disciplina = contador_disciplina + 1
                            else:
                                break
        except OSError as err:
            print("OS error:", err)
            self.info_txt.config(text="Erro, selecione novamente ou reinicie o sistema", font="Helvetica 9 bold",
                                 bg=cor5, fg="red")
            self.botoes()
        except ValueError as err:
            print("ValueError:", err)
            self.info_txt.config(text="Erro, selecione novamente ou reinicie o sistema", font="Helvetica 9 bold",
                                 bg=cor5, fg="red")
            self.botoes()
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            self.info_txt.config(text="Erro, selecione novamente ou reinicie o sistema", font="Helvetica 9 bold",
                                 bg=cor5, fg="red")
            self.botoes()
            raise
        self.info_txt.config(text="Notas puxadas com sucesso!", font="Helvetica 9 bold", bg=cor5, fg=cor2)
        self.botoes()

    # atualiza os botões
    def botoes(self):
        self.botao_fechar.config(text="  Fechar Sistema  ", command=self.sair, bg=cor3, fg=cor1,
                                 font="Helvetica 9 bold", width=18, relief=RAISED, overrelief=RIDGE)
        self.botao_puxar.config(text="Puxar Selecionado", command=self.alterar_txt, bg=cor2, fg=cor1,
                                font="Helvetica 9 bold", width=18, relief=RAISED, overrelief=RIDGE)
        self.botao_todos.config(text="Puxar Todos", command=self.redefinir_txt_puxar, bg="#292625",
                                fg=cor1, font="Helvetica 9 bold", width=18, relief=RAISED, overrelief=RIDGE)
        self.botao_atualizar.config(text=" Redefinir lista", image=self.img_redefinir,
                                    compound=tkinter.LEFT, command=self.redefinir_txt, bg=cor5, fg="black",
                                    font="Helvetica 9 bold", relief=RAISED, overrelief=RIDGE)

    # def responsável por fechar as dependências e encerrar o sistema- obviamente
    def sair(self):
        self.painel.destroy()
        navegador.close()

        exit()

    # def responsável pela alteração do arquivo na pasta raiz do Cabot
    def alterar_txt(self):
        entrada_teclado = self.selecionados.curselection()
        txt_entrada = open('cursos.txt', 'w')
        for entrada in entrada_teclado:
            txt_entrada.write(
                self.listbox[entrada + 1])  # +1 para compensar o item excluído da listbox: Escolha um curso
        txt_entrada.close()
        thread = Thread(target=self.puxar_nota)
        thread.start()

    # def responsável pela restauração do txt
    def redefinir_txt(self):
        # nova extração do texto do elemento Cursos
        navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
        elemento_web_atualizado = navegador.find_element('class name', 'chosen-results').get_attribute("innerText")
        arquivo_atualizado = open('cursos.txt', 'w')
        arquivo_atualizado.write(elemento_web_atualizado)
        arquivo_atualizado.close()
        navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
        # atualização do campo visual
        self.selecionados.destroy()
        lista_atualizada = open('cursos.txt', 'r')
        listbox_atualizado = lista_atualizada.readlines()
        lista_atualizada.close()
        self.selecionados.__init__(self.frame_scrollbar, font="Helvetica 10", height=20, width=75, bd=0,
                                   selectmode=tkinter.MULTIPLE, cursor="plus", selectbackground=cor0,
                                   activestyle='none', yscrollcommand=self.scrollbar.set)
        # config´s scrollbar
        self.scrollbar.config(command=self.selecionados.yview)
        self.scrollbar.grid()
        self.frame_scrollbar.grid()
        for elementos_atualizados in listbox_atualizado:
            self.selecionados.insert(END, elementos_atualizados)
        self.selecionados.delete(0, last=None)
        self.selecionados.grid(row=2, column=1, padx=5, pady=5)
        self.info_txt.config(text='Lista redefinida!', font="Helvetica 9 bold", bg=cor5, fg=cor2)

    # def responsável pela restauração do txt e chamada do puxar nota
    def redefinir_txt_puxar(self):
        # nova extração do texto do elemento Cursos
        navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
        elemento_web_atualizado = navegador.find_element('class name', 'chosen-results').get_attribute("innerText")
        arquivo_atualizado = open('cursos.txt', 'w')
        arquivo_atualizado.write(elemento_web_atualizado)
        arquivo_atualizado.close()
        navegador.find_element('xpath', '//*[@id="curso_chosen"]/a').click()
        # atualização do campo visual
        self.selecionados.destroy()
        lista_atualizada = open('cursos.txt', 'r')
        listbox_atualizado = lista_atualizada.readlines()
        lista_atualizada.close()
        self.selecionados.__init__(self.frame_scrollbar, font="Helvetica 10", height=20, width=75, bd=0,
                                   selectmode=tkinter.MULTIPLE, cursor="plus", selectbackground=cor0,
                                   activestyle='none', yscrollcommand=self.scrollbar.set)
        # config´s scrollbar
        self.scrollbar.grid()
        self.frame_scrollbar.grid()
        for elementos_atualizados in listbox_atualizado:
            self.selecionados.insert(END, elementos_atualizados)
        self.selecionados.delete(0, last=None)
        self.selecionados.grid(row=2, column=1, padx=5, pady=5)
        thread = Thread(target=self.puxar_nota)
        thread.start()

    def conferir_salvo(self):
        if os.path.exists("lembrar_criptografado.txt"):
            # Abre o arquivo criptografado para leitura
            with open('chave.chave', 'rb') as k:
                # Lê a chave de criptografia do arquivo
                chave = k.read()

            # Cria um objeto Fernet com a chave de criptografia
            fernet = Fernet(chave)

            # Abre o arquivo para descriptografar
            with open('lembrar_descriptografado.txt', 'wb') as f:
                # Abre o arquivo criptografado para leitura
                with open('lembrar_criptografado.txt', 'rb') as arquivo_criptografado:
                    # Lê o conteúdo do arquivo criptografado
                    conteudo_criptografado = arquivo_criptografado.read()

                    # Descriptografa o conteúdo
                    conteudo_descriptografado = fernet.decrypt(conteudo_criptografado)

                    # Escreve o conteúdo descriptografado no arquivo de destino
                    f.write(conteudo_descriptografado)

            dados_descriptografados = open('lembrar_descriptografado.txt', 'r')
            lista_dados = dados_descriptografados.readlines()
            self.recebe_login.insert(END, lista_dados[0])
            self.recebe_senha.insert(END, lista_dados[1])
            dados_descriptografados.close()
            os.remove("lembrar_descriptografado.txt")


if __name__ == "__main__":
    app = App()
