# https://huggingface.co/docs/api-inference/getting-started
from hg_face import HEADERS
import requests


# Modelo GENERATIVO para Sumarização
def summarize_text(text):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    payload = {"inputs": text}
    response = requests.post(API_URL, headers=HEADERS, json=payload)

    # Check if the response was successful
    if response.status_code == 200:
        # Check if the response is a list and contains the expected structure
        try:
            return response.json()[0]["summary_text"]
        except (KeyError, IndexError, TypeError):
            print(f"Formato de resposta inesperado: {response.json()}")
            return None  # or raise an exception
    else:
        print(f"Erro: {response.status_code} - {response.text}")  # Print the error message
        return None  # or raise an exception
    
texto = "A inteligência artificial é um campo da ciência que se concentra na criação de computadores e máquinas que podem raciocinar, aprender e atuar de maneira que normalmente exigiria inteligência \
        humana ou que envolve dados com escala maior do que as pessoas podem analisar. A IA é um campo amplo que abrange muitas disciplinas diferentes, como ciência da computação, estatísticas e análises \
        de dados, engenharia de hardware e software, linguística, neurociência e até mesmo filosofia e psicologia. Em um nível operacional para uso comercial, a IA é um conjunto de tecnologias baseadas \
        principalmente em machine learning e aprendizado profundo, usada para análise de dados, previsões e previsão, categorização de objetos, processamento de linguagem natural, recomendações, \
        recuperação inteligente de dados e muito mais. \
        Embora as especificidades variem de acordo com as técnicas de IA, o princípio básico gira em torno dos dados. Os sistemas de IA aprendem e melhoram por meio da exposição a grandes quantidades \
        de dados, identificando padrões e relações que os humanos podem não perceber. Esse processo de aprendizado geralmente envolve algoritmos, que são conjuntos de regras ou instruções que orientam\
        a análise e a tomada de decisões da IA. Em machine learning, um subconjunto conhecido da IA, algoritmos são treinados em dados rotulados ou não rotulados para fazer previsões ou categorizar informações. \
        O aprendizado profundo, uma especialização adicional, utiliza redes neurais artificiais com várias camadas para processar informações, imitando a estrutura e a função do cérebro humano. Com o aprendizado \
        e a adaptação contínuos, os sistemas de IA se tornam cada vez mais competentes para realizar tarefas específicas, como reconhecer imagens, traduzir idiomas e muito mais." 


resumo = summarize_text(text=texto)
print(resumo)

# Exemplo de uso
if __name__ == "__main__":
    resumo = summarize_text(text=texto)

    if resumo:
        print("\nResumo do texto:")
        print(resumo)

        # Salvando em arquivo
        nome_arquivo = "resumo.txt"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(resumo)

        print(f"\nResumo salvo com sucesso em '{nome_arquivo}'.")