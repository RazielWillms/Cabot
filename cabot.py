#Cabot- automação acadêmica para puxar notas no SIGA- Faculdade Uníntese- Raziel Haas Willms
import pyautogui
import time
import os

#devem retornar os ID´s que ainda não foram utilizados
def ler_cursos():
    z = open('cursos.txt','r+')
    cursoid=z.read(3)
    z.close()
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
