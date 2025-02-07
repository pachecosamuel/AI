from transformers import AutoModelForCausalLM, AutoTokenizer

modelo = "mistralai/Mistral-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(modelo)
modelo = AutoModelForCausalLM.from_pretrained(modelo)

entrada = tokenizer("Explique o que é IA.", return_tensors="pt")
saida = modelo.generate(**entrada)
print("\n🤖 Resposta da IA:", tokenizer.decode(saida[0]))
