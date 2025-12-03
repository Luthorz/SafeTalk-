import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk   # xarregar logo
import os
import platform
import subprocess
import ttkbootstrap as tb  #  ttkbootstrap só para estilo
from datetime import datetime  # manipulação de datas

# janela - tamanho médio
root = tk.Tk()
root.title("SafeTalk")
root.geometry("360x640")
root.configure(bg="#f6f6f6")


# tema selecionado (minty)
style = tb.Style(theme="minty")



# cores (paleta 1 - pastel)
COR_FUNDO = "#f6f6f6"
COR_ROSA = "#ff8aae"
COR_AZUL = "#8ec5fc"
COR_VERDE = "#9ee7c5"
COR_CARTAO = "#f78d8d"
COR_TEXTO = "#2b2b2b"


# variaveis de datas e historico
ultimo_login = None
ultimo_quiz = None
historico_acertos = []  # guarda pontuacoes anteriores


# abrir video no sistema
def abrir_video(caminho):
   sistema = platform.system()
   try:
       if sistema == "Windows":
           os.startfile(caminho)
       elif sistema == "Darwin":
           subprocess.call(["open", caminho])
       else:
           subprocess.call(["xdg-open", caminho])
   except Exception:
       try:
           os.system(f'xdg-open "{caminho}" &')
       except Exception:
           print("Não foi possível abrir o vídeo:", caminho)


# limpar toda tela anterior
def limpar_tela():
   for widget in root.winfo_children():
       widget.destroy()


#  provisória de cadastro
def tela_cadastro():
   limpar_tela()
   # tela de cadastro provisória
   Label(root, text="Tela de cadastro (provisória)",
         font=("Arial", 18, "bold"), bg=COR_FUNDO).pack(pady=50)


# tela de login (card + inputs)
def tela_login():
   limpar_tela()

   # carregar logo
   try:
       img = Image.open("D.png")
       img = img.resize((200, 200), Image.LANCZOS)
       img = ImageTk.PhotoImage(img)
       logo_label = Label(root, image=img, bg=COR_FUNDO)
       logo_label.image = img
       logo_label.pack(pady=10)
   except Exception as e:
       print("erro", e)

   # titulo
   titulo = Label(root, text="SafeTalk",
                  bg=COR_FUNDO, fg=COR_TEXTO,
                  font=("Arial", 32, "bold"))
   titulo.pack(pady=(8, 4))

   # subtitulo
   subtitulo = Label(root, text="Educação sexual positiva",
                     bg=COR_FUNDO, fg=COR_ROSA,
                     font=("Arial", 13))
   subtitulo.pack(pady=(0, 12))

   # cartão central
   card = Frame(root, bg=COR_CARTAO, bd=0)
   card.pack(padx=28, pady=8, ipady=14, fill="x")
   card.configure(highlightthickness=1, highlightbackground="#eee")

   # campo email
   email = tb.Entry(card, width=30, bootstyle="light")
   email.insert(0, "Email")
   email.pack(pady=10, padx=12, ipady=6)

   # campo senha
   senha = tb.Entry(card, width=30, bootstyle="light", show="*")
   senha.insert(0, "Senha")
   senha.pack(pady=6, padx=12, ipady=6)

   # registrar login e abrir menu
   def registrar_login():
       global ultimo_login
       ultimo_login = datetime.now()
       tela_menu()

   # botão entrar
   btn_entrar = tb.Button(root, text="Entrar",
                         bootstyle="primary", width=28,
                         command=registrar_login)
   btn_entrar.pack(pady=18)

   # link cadastro
   btn_cadastro = tb.Button(root, text="Não tem conta? Cadastre-se",
                            bootstyle="link", width=28,
                            command=tela_cadastro)
   btn_cadastro.pack(pady=6)


# tela principal (menu com cards)
def tela_menu():
   limpar_tela()

   # cabeçalho
   titulo = Label(root, text="SafeTalk",
                  bg=COR_FUNDO, fg=COR_TEXTO,
                  font=("Arial", 26, "bold"))
   titulo.pack(pady=(12, 6))

   # descriçao curta
   descricao = Label(root, text="Escolha um tema ou recurso",
                     bg=COR_FUNDO, fg="#777777",
                     font=("Arial", 11))
   descricao.pack(pady=(0, 8))

   # mostrar ultimo acesso se houver
   if ultimo_login:
       lbl_ult = Label(root, text=f"Último acesso: {ultimo_login.strftime('%d/%m/%Y %H:%M')}",
                       bg=COR_FUNDO, fg="#777777", font=("Arial", 10))
       lbl_ult.pack(pady=(0,8))

   # frame para cards informativos
   frame_info = Frame(root, bg=COR_FUNDO)
   frame_info.pack(pady=8, padx=16, fill="x")

   # criar card utilitário
   def criar_card(parent, emoji, titulo_card, cor):
       card = Frame(parent, bg=cor, bd=0)
       card.pack(side="left", expand=True, fill="both", padx=8)
       card.configure(highlightthickness=0)
       lbl_emoji = Label(card, text=emoji, bg=cor, font=("Arial", 20))
       lbl_emoji.pack(pady=(10, 0))
       lbl_txt = Label(card, text=titulo_card, bg=cor, fg="white", font=("Arial", 11, "bold"))
       lbl_txt.pack(pady=(6, 12))
       return card

   # cards informativos
   criar_card(frame_info, "❓", "Dúvidas\ncomuns", COR_ROSA)
   criar_card(frame_info, "🪪", "Mitos e\nverdades", COR_AZUL)
   criar_card(frame_info, "📍", "Onde\nprocurar ajuda", COR_VERDE)

   # seção temas
   Label(root, text="Temas",
         bg=COR_FUNDO, fg=COR_TEXTO,
         font=("Arial", 14, "bold")).pack(pady=(14, 6))

   frame_temas = Frame(root, bg=COR_FUNDO)
   frame_temas.pack(pady=6, padx=16, fill="x")

   #  botões-tema
   def criar_tema_button(parent, texto, comando=None):
       btn_frame = Frame(parent, bg=COR_CARTAO)
       btn_frame.pack(side="left", expand=True, padx=8)
       btn_frame.configure(highlightthickness=1, highlightbackground="#eee")
       label_btn = tb.Button(btn_frame, text=texto, bootstyle="light", width=16, command=comando)
       label_btn.pack(padx=8, pady=10)
       return label_btn

   # temas
   criar_tema_button(frame_temas, "Diversidade e\nrespeito", comando=tela_tema)
   criar_tema_button(frame_temas, "Saúde\nsexual")
   criar_tema_button(frame_temas, "Prevenção")
   criar_tema_button(frame_temas, "Relacionamentos")

   # quizzes
   Label(root, text="Quizzes",
         bg=COR_FUNDO, fg=COR_TEXTO,
         font=("Arial", 14, "bold")).pack(pady=(14, 6))

   frame_quiz = Frame(root, bg=COR_FUNDO)
   frame_quiz.pack(pady=6, padx=16, fill="x")

   def criar_quiz_card(parent, texto):
       qf = Frame(parent, bg="#fff0f5")
       qf.pack(side="left", expand=True, padx=8)
       qf.configure(highlightthickness=1, highlightbackground="#eee")
       tb.Button(qf, text=texto, bootstyle="secondary", width=14, command=None).pack(padx=8, pady=10)

   criar_quiz_card(frame_quiz, "Teste seu\nconhecimento")
   criar_quiz_card(frame_quiz, "Desafio e\nmitos")
   criar_quiz_card(frame_quiz, "Quiz\ngeral")


# tela do tema
def tela_tema():
   limpar_tela()

   titulo = Label(root, text="Diversidade e respeito",
                  bg=COR_FUNDO, fg=COR_TEXTO,
                  font=("Arial", 20, "bold"))
   titulo.pack(pady=18)

   content_card = Frame(root, bg=COR_CARTAO)
   content_card.pack(padx=20, pady=6, fill="both")
   content_card.configure(highlightthickness=1, highlightbackground="#eee")

   texto = (
       "Diversidade e respeito envolvem \nreconhecer que cada pessoa\n"
       "tem sua própria identidade, \nexpressão de gênero, orientação\n"
       "afetiva, corpo e história. \nRespeitar a diversidade significa\n"
       "acolher as diferenças sem \njulgamento, promovendo ambientes\n"
       "mais seguros e inclusivos para todos."
   )

   label_texto = Label(content_card, text=texto,
                       bg=COR_CARTAO, fg=COR_TEXTO,
                       font=("Arial", 12), justify="center", wraplength=360)
   label_texto.pack(padx=12, pady=12)

   botoes_frame = Frame(root, bg=COR_FUNDO)
   botoes_frame.pack(pady=14)

   botao_video = tb.Button(botoes_frame, text="▶ Assistir vídeo",
                        bootstyle="info", width=22,
                        command=lambda: abrir_video("Diversidade.mp4"))
   botao_video.pack(pady=(0, 10))

   botao_quiz = tb.Button(botoes_frame, text="Ir para o quiz",
                       bootstyle="warning", width=22,
                       command=tela_quiz)
   botao_quiz.pack(pady=(0, 8))

   botao_voltar = tb.Button(root, text="Voltar ao menu",
                            bootstyle="light", width=20,
                            command=tela_menu)
   botao_voltar.pack(pady=8)


# banco de perguntas
perguntas_quiz = [
   {
       "pergunta": "Segundo o vídeo,\n o que é diversidade?",
       "opcoes": [
           "São todas as diferenças que existem entre as \npessoas, como de corpo, cor, identidade de gênero, \norientação sexual e cultura.",
           "É quando todo mundo é \nigual e pensa da mesma forma.",
           "É apenas sobre orientação sexual."
       ],
       "correta": 0
   },
   {
       "pergunta": "A diversidade e o fato de não \nsermos todos iguais \né um defeito ou \numa característica humana?",
       "opcoes": [
           "É um defeito que deve ser corrigido.",
           "É apenas uma opinião pessoal.",
           "É uma característica da nossa \nhumanidade, não um defeito."
       ],
       "correta": 2
   },
   {
       "pergunta": "Qual direito fundamental\n de cada \npessoa o respeito \nbusca garantir?",
       "opcoes": [
           "O direito de existir sem ser diminuída,\n humilhada ou xingada por ser quem é.",
           "O direito de escolher a roupa \nque os outros devem usar.",
           "O direito de obrigar outras \npessoas a pensar igual."
       ],
       "correta": 0
   }
]


# variaveis globais do quiz
indice = 0
pontuacao = 0


# tela do quiz
def tela_quiz():
   limpar_tela()
   global indice, pontuacao

   quiz = perguntas_quiz[indice]

   titulo = Label(root, text=f"Pergunta {indice+1}/3",
                  bg=COR_FUNDO, fg=COR_TEXTO,
                  font=("Arial", 22, "bold"))
   titulo.pack(pady=16)

   pergunta_card = Frame(root, bg=COR_CARTAO)
   pergunta_card.pack(padx=18, pady=6, fill="both")
   pergunta_card.configure(highlightthickness=1, highlightbackground="#eee")

   pergunta_label = Label(pergunta_card,
                          text=quiz["pergunta"],
                          bg=COR_CARTAO,
                          fg="#333333",
                          font=("Arial", 16),
                          wraplength=380,
                          justify="center")
   pergunta_label.pack(pady=12, padx=8)

   Frame(root, height=6, bg=COR_FUNDO).pack()

   def verificar(op_idx):
       global indice, pontuacao
       if op_idx == quiz["correta"]:
           pontuacao += 1
       indice += 1
       if indice < len(perguntas_quiz):
           tela_quiz()
       else:
           mostrar_resultado()

   for i, opcao in enumerate(quiz["opcoes"]):
       opt_frame = Frame(root, bg=COR_CARTAO)
       opt_frame.pack(padx=18, pady=8, fill="x")
       opt_frame.configure(highlightthickness=1, highlightbackground="#eee")
       tb.Button(opt_frame, text=opcao, bootstyle="secondary", width=60, command=lambda i=i: verificar(i)).pack(padx=8, pady=8)


# mostrar resultado final
def mostrar_resultado():
   limpar_tela()
   global pontuacao, indice, ultimo_quiz

   ultimo_quiz = datetime.now()
   historico_acertos.append(pontuacao)

   Label(root, text="Resultado",
         bg=COR_FUNDO, fg=COR_TEXTO,
         font=("Arial", 26, "bold")).pack(pady=30)

   Label(root,
         text=f"Você acertou {pontuacao} de 3 perguntas!",
         bg=COR_FUNDO, fg="#444444",
         font=("Arial", 18)).pack(pady=12)

   total_tentativas = len(historico_acertos)
   media = sum(historico_acertos) / total_tentativas if total_tentativas > 0 else 0
   melhor = max(historico_acertos) if total_tentativas > 0 else 0
   pior = min(historico_acertos) if total_tentativas > 0 else 0

   resumo_txt = f"Tentativas: {total_tentativas}  |  Média: {media:.2f}  |  Melhor: {melhor}  |  Pior: {pior}"
   Label(root, text=resumo_txt, bg=COR_FUNDO, fg="#666666", font=("Arial", 11)).pack(pady=(6,12))

   barras_acertos = "*" * pontuacao
   barras_erros = "*" * (3 - pontuacao)
   Label(root, text="Progresso (acertos x erros):", bg=COR_FUNDO, fg="#666666", font=("Arial", 11)).pack()
   Label(root, text=f"Acertos: {barras_acertos}", bg=COR_FUNDO, fg=COR_ROSA, font=("Arial", 12)).pack()
   Label(root, text=f"Erros:   {barras_erros}", bg=COR_FUNDO, fg="#777777", font=("Arial", 12)).pack(pady=(0,12))

   botoes_frame = Frame(root, bg=COR_FUNDO)
   botoes_frame.pack(pady=12)

   tb.Button(botoes_frame, text="Voltar ao menu", bootstyle="secondary", width=18, command=tela_menu).pack(side="left", padx=8)
   tb.Button(botoes_frame, text="Ver análise completa", bootstyle="light", width=18, command=abrir_analise_popup).pack(side="left", padx=8)

   pontuacao = 0
   indice = 0


# popup análise completa
def abrir_analise_popup():
   popup = Toplevel(root)
   popup.title("Análise")
   popup.geometry("420x520")
   popup.configure(bg=COR_FUNDO)

   Label(popup, text="Análise completa", bg=COR_FUNDO, fg=COR_TEXTO, font=("Arial", 18, "bold")).pack(pady=(12,6))

   total = len(historico_acertos)
   media = sum(historico_acertos) / total if total > 0 else 0
   melhor = max(historico_acertos) if total > 0 else 0
   pior = min(historico_acertos) if total > 0 else 0

   Label(popup, text=f"Tentativas: {total}", bg=COR_FUNDO, fg="#666666", font=("Arial", 11)).pack()
   Label(popup, text=f"Média: {media:.2f}", bg=COR_FUNDO, fg="#666666", font=("Arial", 11)).pack()
   Label(popup, text=f"Melhor: {melhor}", bg=COR_FUNDO, fg="#666666", font=("Arial", 11)).pack()
   Label(popup, text=f"Pior: {pior}", bg=COR_FUNDO, fg="#666666", font=("Arial", 11)).pack(pady=(0,10))

   frame_hist = Frame(popup, bg=COR_FUNDO)
   frame_hist.pack(padx=12, pady=8, fill="both", expand=True)

   if total == 0:
       Label(frame_hist, text="Nenhuma tentativa registrada ainda.", bg=COR_FUNDO, fg="#777777").pack(pady=20)
   else:
       for idx, val in enumerate(historico_acertos, start=1):
           barras = "*" * val
           Label(frame_hist, text=f"Tentativa {idx}: {barras} ({val}/3)", bg=COR_FUNDO, fg="#333333", anchor="w", justify="left").pack(fill="x", padx=6, pady=4)

   Label(popup, text=" ", bg=COR_FUNDO).pack()
   if ultimo_login:
       Label(popup, text=f"Último login: {ultimo_login.strftime('%d/%m/%Y %H:%M')}", bg=COR_FUNDO, fg="#666666").pack()
   if ultimo_quiz:
       Label(popup, text=f"Último quiz: {ultimo_quiz.strftime('%d/%m/%Y %H:%M')}", bg=COR_FUNDO, fg="#666666").pack()

   tb.Button(popup, text="Fechar", bootstyle="secondary", command=popup.destroy).pack(pady=12)


# iniciar app
tela_login()
root.mainloop()
