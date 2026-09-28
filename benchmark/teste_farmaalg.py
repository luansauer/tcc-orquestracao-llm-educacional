import json
import time
import requests

URL = "http://localhost:11434/api/generate"

# 1. Parâmetros fornecidos pelo Farma-alg / Professor
questao_professor = """
Enunciado:
Implemente uma função em Python chamada `conta_vogais(texto)` que receba uma string
e retorne um dicionário contendo a contagem individual de cada vogal ('a', 'e', 'i', 'o', 'u').
A contagem deve ser insensível a maiúsculas/minúsculas. Vogais acentuadas não precisam ser tratadas.
Se uma vogal não aparecer no texto, sua contagem no dicionário deve ser 0.

Exemplo de entrada:
conta_vogais("Ola Mundo")
Exemplo de retorno esperado:
{'a': 1, 'e': 0, 'i': 0, 'o': 2, 'u': 1}
"""

gabarito_professor = """
def conta_vogais(texto):
    vogais = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
    for char in texto.lower():
        if char in vogais:
            vogais[char] += 1
    return vogais
"""

# 2. Código submetido pelo aluno (com erros conceituais típicos)
resposta_aluno = """
def conta_vogais(texto):
    resultado = {}
    for c in texto:
        if c in "aeiou":
            resultado[c] = resultado.get(c, 0) + 1
    return resultado
"""

# 3. Prompt de ancoragem pedagógica
prompt_pedagogico = f"""Você é o tutor pedagógico automatizado do sistema Farma-alg.
Sua função é realizar a mediação pedagógica entre o que o professor pediu, o gabarito oficial e o código submetido pelo aluno.

Regras estritas:
1. Jamais entregue a resposta correta nem trechos de código corrigidos.
2. Foque em perguntas reflexivas ou dicas pontuais sobre os desvios lógicos.
3. Compare o código do aluno tanto contra o gabarito quanto contra as regras do enunciado.

[QUESTÃO DO PROFESSOR]
{questao_professor.strip()}

[GABARITO DO PROFESSOR]
{gabarito_professor.strip()}

[RESPOSTA SUBMETIDA PELO ALUNO]
{resposta_aluno.strip()}

Responda exclusivamente em formato JSON seguindo a estrutura:
{{
  "atende_requisitos": false,
  "erros_detectados": [
    "descrição do desvio em relação ao gabarito/enunciado"
  ],
  "dica_reflexiva": "orientação sem dar código",
  "avaliacao_geral": "análise técnica sucinta"
}}
"""

payload = {
    "model": "qwen2.5-coder:7b",
    "prompt": prompt_pedagogico,
    "format": "json",
    "stream": False,
    "options": {
        "temperature": 0.0,
        "seed": 42
    }
}

print("Enviando avaliação Farma-alg para o Ollama...")
t0 = time.time()
res = requests.post(URL, json=payload).json()
total_tempo = time.time() - t0

print("\n--- RETORNO DO FARMA-ALG ---")
print(json.dumps(json.loads(res["response"]), indent=2, ensure_ascii=False))

print("\n--- PERFORMANCE ---")
print(f"Tempo total: {total_tempo:.2f} s")
print(f"Tokens processados (Entrada): {res.get('prompt_eval_count')}")
print(f"Tokens gerados (Saída): {res.get('eval_count')}")
if res.get("eval_duration"):
    print(f"Throughput: {res.get('eval_count') / (res.get('eval_duration') / 1e9):.2f} tokens/s")