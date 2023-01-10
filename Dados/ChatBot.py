import telebot, csv
from decouple import config
import time
from datetime import datetime
from telebot.types import LabeledPrice #preenchimento de tabela de preço

#Conectando ao bot criado no Telegram
token = config("TOKEN_BOT") 

bot = telebot.TeleBot(token)

#Token de conexão com o provedor de pagamentos
token_provedor = config("TOKEN_PROVEDOR")

#Criar o preço do meu produto
preco = [
    LabeledPrice(label='E-book Engenharia de Requisitos para Projetos de BI', amount=1000)
]

#Salvando dados da conversa do chatbot em arq csv
def salvar (arquivo, conversa: list):
    with open(arquivo,'a') as chat:
        e = csv.writer(chat)
        e.writerow(conversa)

#Iniciar a conversa com o BOT
@bot.message_handler(commands=["start","iniciar"])
def start (message):
    bot.send_message(message.chat.id, "Seja bem vindo(a) ao DestinySeat, tudo bem?",timeout=120)

#Função de compra
@bot.message_handler(commands=["comprar"])
def compra (message):
    bot.send_invoice(
        message.from_user.id,
        title='Teste1',
        description='Teste2',
        provider_token=token_provedor,
        currency='BRL',
        photo_url=config('PROD1'),
        photo_height=512,
        photo_size=512,
        photo_width=512,
        is_flexible=False,
        prices=preco,
        invoice_payload="PAYLOAD"
    )

#Função pré-checkout. Verificar dados do cartão.
@bot.pre_checkout_query_handler(func=lambda	query:True)
def verify_paycard(pre_checkout_query):
    bot.answer_pre_checkout_query(
        pre_checkout_query.id, ok=True, error_message="Houve uma falha na confirmação do pagamento do seu cartão. Verifique com a operadora do seu cartão!"
    )

#Função para validação de pagamento
@bot.message_handler(content_types=['successful payment'])
def pgto_confirmado (message):
    salvar('c_efetuada.csv',[message.chat.id, message.from_user.username, message.text, datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    doc = open("Dados\\teste.jpg","rb")
    bot.send_message(message.chat.id, "Show! Pagamento confirmado, arquivo liberado, jájá vai receber o seu arquivo aqui no chat!! :D")
    bot.send_document(message.chat.id, doc, timeout=180)
    time.sleep(2)
    bot.send_message(message.chat.id, "Obrigado pela compra, até a próxima!!\n\nSe quiser reiniciar a nossa conversa, digite iniciar.")

@bot.message_handler(regexp='iniciar')
def iniciar (message):
    print(message) #vai vir tudo que acontece no chat
    salvar('iniciar.csv',[message.chat.id, message.from_user.username, message.text, datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    bot.send_message(message.chat.id, "Seja bem vindo(a) ao DestinySeat, tudo bem?",timeout=120)

@bot.message_handler(regexp=r'tudo|td|sim')
def pergunta (message):
    salvar('saudacao.csv',[message.chat.id, message.from_user.username, message.text, datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    time.sleep(5)
    bot.send_message(message.chat.id, "Que bom! Agora, vamos realizar a compra do Sticker?\n \nAo comprar o sticker, ela se torna sua, assim como NFTS. Se interessou? Então, clique em /comprar para efetuar o pagamento e receber o seu produto, o valor é R$10,00.\n \nNão perca essa chance!!\n \nDo contrário, digite DEPOIS para uma próxima oportunidade.",timeout=120)

#Download ou Playlist
'''@bot.message_handler(regexp='bora')
def download(message):
    salvar('c_efetuada.csv',[message.chat.id, message.from_user.username, message.text, datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    doc = open("Dados\\teste.jpg","rb")
    bot.send_message(message.chat.id, 'Opa. Hora de fazer o download rs', timeout=120)
    time.sleep(2)
    bot.send_document(message.chat.id, doc, timeout=120)
    time.sleep(2)
    bot.send_document(message.chat.id, "Obrigada pelo download! Para reiniciar a conversa, digite iniciar.", timeout=120)
'''

@bot.message_handler(regexp='depois')
def convence (message): 
    time.sleep(2)
    bot.send_message(message.chat.id, "Tem certeza que não deseja realizar a compra?\n \nVou te dar mais uma chance para /comprar o sticker, você não vai se arrepender, acredita em mim rs", timeout=120)
    time.sleep(4)
    bot.send_message(message.chat.id, "De novo, clica em /comprar aí, vai ser a melhor coleção que já presenciou na vida. Ou digite tchau para pensar um pouco mais sobre a compra..",timeout=120)

@bot.message_handler(regexp='tchau')
def tchau(message):
    salvar('c_naoefetuada.csv',[message.chat.id, message.from_user.username, message.text, datetime.now().strftime('%d/%m/%Y %H:%M:%S')])
    time.sleep(2)
    bot.send_message(message.chat.id, "Bom, caso mude de ideia, sabe o que tem que fazer rs.\n \nEspero que consigamos conquistar o seu lado de colecionador na próxima vez.. Obrigada pelo interesse!!",timeout=120)

#Sondagem/Verificar se há mensagens
bot.polling(non_stop=True, interval=0) 

