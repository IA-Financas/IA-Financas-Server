#import openai

#chave_api = "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"
#openai.api_key = chave_api

#def enviar_mensagem(mensagem, lista_mensagens=[]):
 #   lista_mensagens.append(
     #   {"role": "user", "content": mensagem}
   #    )

   # resposta = openai.ChatCompletion.create(
     #   model = "gpt-3.5-turbo",
     #   messages = lista_mensagens,
   # )

   # return resposta["choices"][0]["message"]

#lista_mensagens = []
#while True:
  #  texto = input("Escreva aqui sua mensagem:")

 #   if texto == "sair":
    #    break
   # else:
     #   resposta = enviar_mensagem(texto, lista_mensagens)
       # lista_mensagens.append(resposta)
       # print("Chatbot:", resposta["content"])
