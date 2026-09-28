import time
import requests
import json

URL = "http://localhost:11434/api/generate"

prompt_completo = """Você é um tutor pedagógico de programação.
Compare o código do aluno estritamente com o gabarito.
Responda exclusivamente no formato JSON com as chaves:
- "status": "correto" ou "incorreto"
- "erro_identificado": descrição concisa do erro
- "dica_pedagogica": orientação sem entregar a resposta pronta

[Gabarito]
def soma(a, b):
    return a + b

[Código do Aluno]
def soma(a, b):
    print(a + b)
"""

payload = {
    "model": "qwen2.5-coder:7b",
    "prompt": prompt_completo,
    "format": "json",  # Força decodificação estruturada nativa no Ollama
    "stream": False,
    "options": {
        "temperature": 0.0,
        "seed": 42
    }
}

print("Enviando requisição com restrição JSON...")
t_inicio = time.time()
res = requests.post(URL, json=payload).json()
t_total = time.time() - t_inicio

print("\n--- RETORNO PARSEADO (JSON) ---")
dados_retorno = json.loads(res["response"])
print(json.dumps(dados_retorno, indent=2, ensure_ascii=False))

print("\n--- MÉTRICAS COMPUTACIONAIS ---")
print(f"Tempo total: {t_total:.2f} s")
print(f"Tokens gerados: {res.get('eval_count')}")
if res.get('eval_duration'):
    velocidade = res.get('eval_count') / (res.get('eval_duration') / 1e9)
    print(f"Velocidade: {velocidade:.2f} tokens/s")