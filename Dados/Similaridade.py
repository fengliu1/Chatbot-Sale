import spacy

nlp = spacy.load("pt_core_news_sm")

#Exemplo 1 - Tokenização = divisão de tudo que está sendo falado
texto = nlp(u'Eu estou aprendendo a utilizar chatbots')

for token in texto:
    print(token.text, token.pos_) #pos = part of speach = ponto de fala
    
#Exemplo 2 - Mais alguns atributos do token
texto2 = nlp(u'O canal do Youtube do "Prof. Claudio Bonel" está chegando a 11.000 inscritos.')

for token in texto2:
    print('Texto:',token.text,
            "Forma raiz:", token.lemma_, #lematização -> dá lema a palavra
            "Tipo:",token.pos_,
            "É letra:",token.is_alpha) #verifica se é letra alfabética
    

#Exemplo 3 - Buscando semelhanças = Faz com que o bot tenha a noção de buscar
#  semelhanças em digitação das palavras
# Frase testada: Quero aprendizado e conhecimento
texto3 = input('Como posso te ajudar no dia de hoje? ')
texto3 = nlp(texto3) #texto sendo carregado para a biblioteca ptbr

for token1 in texto3:
    for token2 in texto3:
        similaridade = round((token1.similarity(token2) *100),2) #comparação do token1 e token2
        print("A palavra {} é {}% similar a palavra {}".format(token1.text, similaridade, token2.text))

#Exemplo 4 - Buscando semelhanças e comparando com as regras do chatbot
texto4 = input('Como posso te ajudar no dia de hoje? ')
texto4 = nlp(texto4) 
texto_comp = nlp('conhecimento')

def conhecimento():
        print('Fico feliz em saber que está em busca de conhecimento!! Acesse https://www.youtube.com/premium_benefits para mais informações!')


for token in texto4:
    similaridade = round((token.similarity(texto_comp) *100),2)
    if similaridade == 100:
        #print("A palavra {} é {}% similar a palavra conhecimento".format(token.text, similaridade))
        conhecimento()
    elif similaridade >= 39 and similaridade < 100:
        pergunta_similaridade = input('Você está em busca de conhecimento? [S/N] ')
        if pergunta_similaridade.upper() == "S":
            print("A palavra {} é {}% similar a palavra conhecimento".format(token.text, similaridade))
            conhecimento()
        else:
            print("Refaça sua solicitação, por favor.")
    else:
        print("Não encontrei sua solicitação. Por favor, refaça.",similaridade)