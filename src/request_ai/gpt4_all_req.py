from gpt4all import GPT4All

model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")  # Baixa o modelo automaticamente
resposta = model.generate("Explique a Lei da Oferta e da Demanda.")
print(resposta)
