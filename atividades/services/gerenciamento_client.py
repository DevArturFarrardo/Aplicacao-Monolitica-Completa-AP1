import os
import requests

GERENCIAMENTO_URL = os.getenv("GERENCIAMENTO_URL", "http://gerenciamento:5000")
TIMEOUT = 3

def verificar_turma(turma_id):
    try:
        r = requests.get(f"{GERENCIAMENTO_URL}/turmas/{turma_id}", timeout=TIMEOUT)
        return r.status_code == 200
    except requests.RequestException:
        return False

def verificar_professor(professor_id):
    try:
        r = requests.get(f"{GERENCIAMENTO_URL}/professores/{professor_id}", timeout=TIMEOUT)
        return r.status_code == 200
    except requests.RequestException:
        return False

def verificar_aluno(aluno_id):
    try:
        r = requests.get(f"{GERENCIAMENTO_URL}/alunos/{aluno_id}", timeout=TIMEOUT)
        return r.status_code == 200
    except requests.RequestException:
        return False