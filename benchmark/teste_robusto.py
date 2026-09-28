import time
import requests
import json
import threading
import psutil
import os

URL = "http://localhost:11434/api/generate"

# Monitoramento de RAM do sistema em background
ram_picos = []
monitorando = True

def monitorar_ram():
    processo = psutil.Process(os.getpid())
    while monitorando:
        ram_sistema = psutil.virtual_memory().percent
        ram_processo_mb = processo.memory_info().rss / (1024 * 1024)
        ram_picos.append((ram_sistema, ram_processo_mb))
        time.sleep(0.1)

# Cenário pedagógico mais complexo: Verificação de Palíndromo
prompt_robusto = """Você é um tutor pedagógico rigoroso de Algoritmos e Estruturas de Dados.
Compare a solução do aluno com o gabarito oficial.
Identifique:
1. Erros lógicos ou de sintaxe.
2. Casos de borda não tratados (ex: pontuação, espaços, maiúsculas).
3. Dica pedagógica reflexiva sem jamais fornecer código pronto.

[Enunciado]
Crie uma função `eh_palindromo(frase)` que retorne True se a frase for palíndromo e False caso contrário. Desconsidere espaços, acentos e maiúsculas. Exemplo: "A sacada da casa" -> True.

[Gabarito Oficial]
def eh_palindromo(frase):
    limpa = ''.join(c.lower() for c in frase if c.isalnum())
    return limpa == limpa[::-1]

[Código Submetido pelo Aluno]
def eh_palindromo(frase):
    tamanho = len(frase)
    for i in range(tamanho):
        if frase[i] != frase[tamanho - i]:
            return False
    return True

Responda ESTRITAMENTE em formato JSON com o seguinte schema:
{
  "status": "incorreto",
  "erros_detectados": [
    "string descrevendo erro 1",
    "string descrevendo erro 2"
  ],
  "casos_de_borda_ignorados": [
    "string descrevendo caso 1"
  ],
  "dica_pedagogica": "orientação socrática"
}
"""

payload = {
    "model": "qwen2.5-coder:7b",
    "prompt": prompt_robusto,
    "format": "json",
    "stream": False,
    "options": {
        "temperature": 0.0,
        "seed": 42
    }
}

# Medição de RAM antes do início
ram_inicial_sistema = psutil.virtual_memory().percent
ram_inicial_usada_gb = (psutil.virtual_memory().total - psutil.virtual_memory().available) / (1024**3)

t_thread = threading.Thread(target=monitorar_ram)
t_thread.start()

print("Disparando inferência com prompt analítico robusto...")
t_inicio = time.time()
resposta_raw = requests.post(URL, json=payload)
t_total = time.time() - t_inicio

monitorando = False
t_thread.join()

res = resposta_raw.json()

# Processamento da RAM
pico_sistema = max(r[0] for r in ram_picos) if ram_picos else ram_inicial_sistema
ram_final_usada_gb = (psutil.virtual_memory().total - psutil.virtual_memory().available) / (1024**3)

print("\n================== RETORNO ESTRUTURADO DA IA ==================")
try:
    dados_json = json.loads(res["response"])
    print(json.dumps(dados_json, indent=2, ensure_ascii=False))
except Exception as e:
    print("Erro no parsing:", e)
    print(res.get("response"))

print("\n================== TELEMETRIA COMPUTACIONAL ==================")
print(f"Tempo de Execução Total : {t_total:.2f} s")
print(f"Tokens de Entrada (Prompt) : {res.get('prompt_eval_count')}")
print(f"Tokens de Saída (Geração) : {res.get('eval_count')}")
if res.get('eval_duration'):
    velocidade = res.get('eval_count') / (res.get('eval_duration') / 1e9)
    print(f"Throughput de Geração   : {velocidade:.2f} tokens/s")

print("\n================== CONSUMO DE MEMÓRIA RAM ==================")
print(f"RAM Sistema (Antes)     : {ram_inicial_usada_gb:.2f} GB ({ram_inicial_sistema}%)")
print(f"RAM Sistema (Pico)      : {pico_sistema}%")
print(f"RAM Sistema (Depois)    : {ram_final_usada_gb:.2f} GB")
