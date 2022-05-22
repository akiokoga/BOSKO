# Biblioteca da cãmera
import numpy as np
import face_recognition as fr
import cv2
import keyboard

# Biblioteca de comando de voz
import speech_recognition as sr
import playsound
from gtts import gTTS, tts
import random
import webbrowser
import wikipedia
import pyttsx3
import time
import os

"""
Qual o objetivo do cadastro facial:
Manter o controle da autenticação da professora e dos alunos que irão utilizar a plataforma
Sendo o objetivo central ter uma plataforma com o intuito educacional
Precisamos manter uma forma de autenticação seja do professor ou do aluno que irá 
utilizar o aplicativo criado.
"""

def encontrar_rostos(url):
    # Carrega uma imagem no face recognition
    foto = fr.load_image_file(url)
    # Carrega os rostos encontrados nas fotos
    rostos = fr.face_encodings(foto)
    # Se for encontrado mais de um rosto
    if len(rostos) > 0:
        return True, rostos
    else:
        return False, []

rostos_cadastrados = []
email_cadastrado = []
nome_cadastrado = []

email_input = input("Preencha o seu e-mail: ")
"""
# Vamos simular um cadastro de alguém com a função encontrar rostos
guilherme = encontrar_rostos("./fotos/endrigo.guilherme@hotmail.com/guilherme1.jpg")
if guilherme[0] == True:
    # A função cadastrada acima retorna o rosto da imagem da url passada na função
    rostos_cadastrados.append(guilherme[1][0])
    # Vamos adicionar o e-mail que será cadastrado
    email_cadastrado.append("endrigo.guilherme@hotmail.com")
"""
henrrique = encontrar_rostos("./fotos/akiokoga@hotmail.com/henrrique1.png")
if henrrique[0] == True:
    # A função cadastrada acima retorna o rosto da imagem da url passada na função
    rostos_cadastrados.append(henrrique[1][0])
    # Vamos adicionar o e-mail que será cadastrado
    email_cadastrado.append("akiokoga@hotmail.com")
    # Vamos adicionar o nome para identificar o usuário
    # Parâmetro que será utilizado na nossa IA de voz para reconhecer o usuário
    nome_cadastrado.append("Henrique")

# Com o cv2 criamos uma variável que chama a ferramenta para absorver os vídeos rodados
# Vem do openCv, pegamos a primeira camera
video_cam = cv2.VideoCapture(0)
# Obriga a entrada no fluxo seguinte
while True:
    # Retorna doi parâmetros a função read do opencv, o primeiro um booleano, o segundo retorna o frame
    bool, frame = video_cam.read()
    # Vamos colocar um input do frame criando uma variável para armazenar um RGB(cores)
    rgb = frame[:, :, ::-1]
    # Vamos verificar portanto a localização da face(face_location) e vamos passar pra função face_encoding
    # Para cada imagem retornada temos um face_encoding, que verifica pra cada face 128 pontos de dimensões da face
    # criamos portanto a variável chamada face
    localizacao_rostos = fr.face_locations(rgb)
    localizacao_pontos_rostos = fr.face_encodings(rgb, localizacao_rostos)

    for (top, right, bottom, left), rosto in zip(localizacao_rostos, localizacao_pontos_rostos):
        # Imaginando que ocorreu um cadastro com fotos do rosto, vamos verificar com uma autenticação a comparação dos rostos cadastrados
        # Dessa forma conseguimos autenticar os rostos comparando com todos os rostos que aparecem na webcam
        resultados = fr.compare_faces(rostos_cadastrados, rosto)
        # Verificar o quão distante está do rosto mais similar na nossa base de dados
        dissimiliaridade = fr.face_distance(rostos_cadastrados, rosto)
        # Pegar o rosto que possui o menor valor
        vl_min = np.argmin(dissimiliaridade)
        # verificar se existe algum valor minimo aderente ao rosto que está autenticando no app
        if resultados[vl_min] == True:
            email = email_cadastrado[vl_min]
            nome = nome_cadastrado[vl_min]
        else:
            email = "NEGADO"

        # Criar caixa ao redor do rosto
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Embaixo: Criando uma faixa vermelha de visualização do email
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_SIMPLEX

        # Texto: ONDE O TEXTO DEVE APARECER, logicamente esta tela não irá existir
        # Iremos apenas mostrar o funcionamento do reconhecimento do e-mail para
        # realizar a autenticação do usuário
        cv2.putText(frame, email, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        cv2.imshow('AUTENTICACAO', frame)

        # Vamos criar uma tecla de encerramento para finalizar o nosso programa
        # Para isso escolhemos uma tecla qualquer com o valor z, que irá passar o valor
        # Para o 0xFF, ou seja, o que irá finalizar o processo
        # Ele apenas irá finalizar se reconhecer o usuário
        if email == email_input:
            time.sleep(5)
            keyboard.press('z')
        else:
            print("Não autenticado")

    if cv2.waitKey(1) & 0xFF == ord('z'):
        break
# Vamos encerrar a câmera
video_cam.release()
cv2.destroyAllWindows()

print("Tudo certo, você está autenticado!!!")

# Iremos criar uma classe BOSKO
# Que irá controlar os comandos de voz

class BOSKO():
    def __init__(self, nome, pessoa):
        self.pessoa = pessoa
        self.nome = nome

        # Iremos instanciar a chamada da fala
        self.fala = pyttsx3.init()
        self.fala.setProperty('rate', 300)
        # Assim como o recgonizer para reconhecer o nosso áudio
        self.rec = sr.Recognizer()
        # os dados de voz é declarado apenas para armazenar a info que está sendo comunicada
        # De forma textual
        self.dados_de_voz = ''

    # A função falar recebe um texto para o BOSKO se comunicar
    def falar(self, texto):
        """
        fala da Assistente virtual
        """
        texto = str(texto)
        self.fala.say(texto)
        self.fala.runAndWait()

    # Essa função serve para gravar um audio, portanto o parâmetro de dados de voz é limpado
    # Recebe um áudio
    def gravar_audio(self):

        with sr.Microphone() as source:

            self.dados_de_voz = ""

            audio = self.rec.listen(source, None, 8)
            print('BOSKO: ...')

            # Como primeiro passo ele irá tentar converter o áudio com o recgonize_google
            # Pacote que conseguimos construir o entendimento para o português
            try:
                self.dados_de_voz = self.rec.recognize_google(audio, language="pt-BR")

            # Caso o valor seja uma comando inválido, ele é colocado na exceção, ou seja
            # o BOSKO irá se desculpar por não ter compreendido
            except sr.UnknownValueError:
                # self.falar(f"Desculpa {self.pessoa}, Eu não entendi o que você disse, pode repetir?")
                if self.dados_de_voz != "":
                    self.falar("Desculpa não entendi")
                self.dados_de_voz = ''

            # Caso a falha seja de requisição da chamada do google recgonize
            # O nosso aplicativo irá dizer que não está funcionando o servidor
            except sr.RequestError:
                self.falar("Desculpa meu servidor não está funcionando")

            if self.dados_de_voz != "":
                print("   Eu: >>", self.dados_de_voz.lower())
                self.dados_de_voz = self.dados_de_voz.lower()

                return self.dados_de_voz.lower()
    # Comandos de fala, configurações de vocabulário português para a fala
    # conversão do audio em texto com o gTTs
    def falar(self, audio):
        audio = str(audio)
        tts = gTTS(text=audio, lang='pt')
        r = random.randint(1, 20000)
        arquivo = 'audio' + str(r) + '.mp3'
        tts.save(arquivo)
        playsound.playsound(arquivo)
        print(self.nome + ': >>', audio)
        os.remove(arquivo)

    # Caso o termo exista em uma lista de valores
    # Ele irá compreender o valor do comando e irá executar o que lhe é solicitado
    def existe_termo(self, termos):
        """
        Função para identificar se o termo existe no aúdio
        """
        # Portanto ele percorre todos os elementos de uma lista
        for term in termos:
            if term in self.dados_de_voz:
                return True

# Com a classe declarada precisamos agora instanciar a variável
# Vamos portanto passar o nome do usuário logado
# para o nosso BOSKO
assistente = BOSKO("BOSKO", nome)

# Forçamos portanto um looping infinito
# Ele entra no looping e executa os comandos de voz do BOSKO
while True:

    dados_de_voz = assistente.gravar_audio()
    # Aqui criamos a função de acionamento do BOSKO
    if assistente.existe_termo(['bosko', 'bosco', 'busco']):
        assistente.falar(f'Olá {nome}, como eu poderia te ajudar?')
        # Se o looping se exceder a quantidade de valores de loopings(8 rodadas) após o acionamento do bosko
        # Ele irá se despedir, por isso foi implementado um contador
        contador_looping = 0
        while True:
            dados_de_voz = assistente.gravar_audio()
            # Colocamos um dicionário dentro do BOSKO para caso o usuário sinta a necessidade
            # de procurar o significado de alguma palavra, com uma requisição da wikipedia
            # Sendo o nosso app um aplicativo de leitura, será uma ferramenta muito útil para auxiliar os usuários
            if assistente.existe_termo(['pesquise por', 'procure por']):
                search_term = dados_de_voz.split("por")[-1]
                wikipedia.set_lang('pt')
                procurar = wikipedia.summary(search_term, 2)
                assistente.falar(procurar)
                dados_de_voz = ""
                break

            # Sendo o nosso aplicativo utilizado também para controle de turmas escolares, temos que
            # implementar uma forma de realizar a inclusão de tarefas de leituras obrigatórias
            # Deve receber como parâmetro um livro, uma página e uma data limite para a realização da tarefa pendente
            elif assistente.existe_termo(
                    ['cadastrar leitura obrigatória', 'cadastrar obrigatória', 'leitura obrigatória']):
                livro = ""
                livro_confirma = ""
                pg = ""
                pagina_confirma = ""
                dia = ""
                dia_confirma = ""
                resp = ""
                while livro == "" or livro == None:
                    assistente.falar("Ok, qual livro devo cadastrar?")
                    livro = assistente.gravar_audio()
                while pg == "" or pg == None:
                    assistente.falar("Ok, qual página devo cadastrar?")
                    pg = assistente.gravar_audio()
                while dia == "" or dia == None:
                    assistente.falar("Qual data limite?")
                    dia = assistente.gravar_audio()
                cadastro = "livro " + livro + ", página " + pg + ", para o dia " + dia
                while resp not in ('sim', 'não'):
                    assistente.falar(cadastro + ', gostaria de confirmar?')
                    resp = assistente.gravar_audio()
                if resp == "sim":
                    with open('tarefas.txt', 'a') as arq:
                        arq.write(str(cadastro) + '\n')
                    assistente.falar("Leitura obrigatória cadastrada")
                elif resp == "não":
                    assistente.falar('Leitura não cadastrada')
                dados_de_voz = ""
                break

            # Assim como o/a professor(a), os alunos, também poderão acessar a verificação de tarefas criadas pelo professor(a)
            elif assistente.existe_termo(['verificar tarefas', 'tarefas', 'minhas tarefas']):
                with open('tarefas.txt') as event:
                    content = event.readlines()
                content = [x.strip('\n') for x in content]
                for line in content:
                    assistente.falar(line)
                dados_de_voz = ""
                break

            # Funções de biblioteca, são funções que permitem navegar pelo aplicativo verificando livros da plataforma,
            # verificando autores, categoria do livro, e número de páginas
            elif assistente.existe_termo(['temos o livro ']):
                # Estante ficticia
                livros = ['harry potter', 'a arte da guerra', 'orgulho e preconceito']
                autores = ["J. K. Rowling", 'Sun Tzu', "Jane Austen"]

                livro_procurado = dados_de_voz.split("livro ")[-1]
                if livro_procurado in livros:
                    assistente.falar("Temos sim o livro " + livro_procurado + " na nossa estante virtual")
                else:
                    assistente.falar("infelizmente ainda não temos o livro " + livro_procurado)
                break

            elif assistente.existe_termo(['quem é o autor de', 'o autor de', 'autor de', 'ator de']):
                # Estante ficticia
                livros = ['harry potter', 'a arte da guerra', 'orgulho e preconceito']
                autores = ["J. K. Rowling", 'Sun Tzu', "Jane Austen"]

                livro_procurado = dados_de_voz.split("de ")[-1]
                if livro_procurado in livros:
                    for i in range(len(livros)):
                        if livros[i] == livro_procurado:
                            valor = i
                            assistente.falar("O autor de " + livros[i] + " é " + autores[i])
                else:
                    assistente.falar("Não encontrei nada referente a " + livro_procurado)
                    assistente.falar("Irei te direcionar para o google com o livro procurado")
                    url = "https://www.google.com.br/search?q=" + livro_procurado
                    webbrowser.get().open(url)
                break

            elif assistente.existe_termo(['número de páginas de', 'páginas de']):
                # Estante ficticia
                livros = ['harry potter', 'a arte da guerra', 'orgulho e preconceito']
                autores = ["J. K. Rowling", 'Sun Tzu', "Jane Austen"]
                paginas = [450, 300, 460]

                livro_procurado = dados_de_voz.split("páginas de ")[-1]
                if livro_procurado in livros:
                    for i in range(len(livros)):
                        if livros[i] == livro_procurado:
                            valor = i
                            assistente.falar("O livro " + livros[i] + " tem " + str(paginas[i]) + " páginas")
                else:
                    assistente.falar("Não encontrei nada referente a " + livro_procurado)
                    assistente.falar("Irei te direcionar para o google com o livro procurado")
                    url = "https://www.google.com.br/search?q=" + livro_procurado
                    webbrowser.get().open(url)
                break

            elif assistente.existe_termo(['categoria do livro ']):
                # Estante ficticia
                livros = ['harry potter', 'a arte da guerra', 'orgulho e preconceito']
                autores = ["J. K. Rowling", 'Sun Tzu', "Jane Austen"]
                paginas = [450, 300, 460]
                categoria = ['aventura', 'não ficção', 'drama']

                livro_procurado = dados_de_voz.split("livro ")[-1]
                if livro_procurado in livros:
                    for i in range(len(livros)):
                        if livros[i] == livro_procurado:
                            valor = i
                            assistente.falar("O livro " + livros[i] + " é da categoria " + str(categoria[i]))
                else:
                    assistente.falar("Não encontrei nada referente a " + livro_procurado)
                    assistente.falar("Irei te direcionar para o google com o livro procurado")
                    url = "https://www.google.com.br/search?q=" + livro_procurado
                    webbrowser.get().open(url)
                break

            elif dados_de_voz != "" and dados_de_voz != None:
                contador_looping += 1
                assistente.falar("Desculpa não entendi")
                if contador_looping == 8:
                    assistente.falar("Qualquer coisa pode me chamar! Estou a disposição! Até logo")
                    dados_de_voz = ""
                    break

            else:
                contador_looping += 1
                if contador_looping == 8:
                    assistente.falar("Qualquer coisa pode me chamar! Estou a disposição! Até logo")
                    dados_de_voz = ""
                    break
















