import os
import requests

GERENCIAMENTO_URL = os.getenv("GERENCIAMENTO_URL", "http://gerenciamento:5000")
TIMEOUT = 3

def verificar_turma(turma_id):
    try:
        r = requests.get(f"{GERENCIAMENTO_URL}/turmas/{turma_id}", timeout=TIMEOUT)
        if r.status_code == 200:
            return True, r.json()
        return False, None
    except requests.RequestException:
        return False, None