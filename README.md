# 🏫 Sistema de Gerenciamento Escolar - Arquitetura de Microsserviços

## 📘 Visão Geral

Este projeto implementa um **sistema de gerenciamento escolar** utilizando arquitetura de **microsserviços** com Flask, containerizados via Docker Compose. O sistema é composto por três serviços independentes que se comunicam de forma síncrona através de APIs REST.

### Serviços do Ecossistema

1.  **Gerenciamento** - Serviço central que gerencia professores, alunos e turmas.
2.  **Reservas** - Gerencia reservas de salas e laboratórios.
3.  **Atividades** - Gerencia atividades avaliativas e notas dos alunos.

---

## 🏗️ Arquitetura do Sistema

### Visão Geral da Arquitetura

O sistema utiliza uma **arquitetura de microsserviços** onde cada serviço:
- Possui seu próprio banco de dados (SQLite).
- Expõe uma API REST independente.
- Comunica-se com outros serviços via HTTP.
- Roda em um container Docker isolado.
- Possui documentação Swagger própria.

### Diagrama de Comunicação

```text
┌─────────────────┐
│   Reservas      │
│   (Port 5001)   │
│                 │
│  ┌──────────┐   │         HTTP GET
│  │ reservas │───┼────────────────────┐
│  │   .db    │   │                    │
│  └──────────┘   │                    ▼
└─────────────────┘              ┌─────────────────┐
                                 │  Gerenciamento  │
┌─────────────────┐              │   (Port 5000)   │
│  Atividades     │              │                 │
│   (Port 5002)   │              │  ┌──────────┐   │
│                 │   HTTP GET   │  │ escola   │   │
│  ┌──────────┐   │──────────────┤  │   .db    │   │
│  │atividades│   │              │  └──────────┘   │
│  │   .db    │   │              │                 │
│  └──────────┘   │              └─────────────────┘
Tabela de Arquitetura
Serviço	Porta	Framework	Documentação	Banco de Dados	Responsabilidade
gerenciamento	5000	Flask + Flasgger	/apidocs	escola.db	CRUD de alunos, professores e turmas
reservas	5001	Flask + Flask-RESTX	/docs	reservas.db	CRUD de reservas de salas/labs
atividades	5002	Flask + Flask-RESTX	/docs	atividades.db	CRUD de atividades e notas
🔗 Integração entre Microsserviços
Comunicação Síncrona com Requests
O sistema implementa comunicação síncrona entre microsserviços utilizando a biblioteca requests do Python. Os serviços Reservas e Atividades validam dados consultando o serviço Gerenciamento antes de realizar operações.

Fluxo de Integração
1. Serviço Reservas → Gerenciamento
Arquivo: reservas/services/gerenciamento_client.py

Quando uma reserva é criada, o serviço valida se a turma existe:

python
Copy
import requests

def validar_turma(turma_id):
    """
    Valida se uma turma existe no serviço de Gerenciamento
    """
    try:
        response = requests.get(f'http://gerenciamento:5000/turmas/{turma_id}')
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
Fluxo:

Cliente faz POST para /reservas com turma_id.
Serviço Reservas chama validar_turma(turma_id).
Requisição HTTP GET para http://gerenciamento:5000/turmas/{turma_id}.
Se a turma existe (200 OK), a reserva é criada.
Se não existe (404), retorna erro ao cliente.
2. Serviço Atividades → Gerenciamento
Arquivo: atividades/services/gerenciamento_client.py

O serviço Atividades valida três entidades diferentes:

python
Copy
import requests

BASE_URL = 'http://gerenciamento:5000'

def validar_turma(turma_id):
    """Valida se uma turma existe"""
    try:
        response = requests.get(f'{BASE_URL}/turmas/{turma_id}')
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def validar_professor(professor_id):
    """Valida se um professor existe"""
    try:
        response = requests.get(f'{BASE_URL}/professores/{professor_id}')
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def validar_aluno(aluno_id):
    """Valida se um aluno existe"""
    try:
        response = requests.get(f'{BASE_URL}/alunos/{aluno_id}')
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
Fluxo para criação de Atividade:

Cliente faz POST para /atividades com turma_id e professor_id.
Serviço valida a turma via validar_turma().
Serviço valida o professor via validar_professor().
Se ambos existem, a atividade é criada.
Caso contrário, retorna erro 400.
Fluxo para criação de Nota:

Cliente faz POST para /atividades/notas com aluno_id e atividade_id.
Serviço valida o aluno via validar_aluno().
Serviço valida se a atividade existe localmente.
Se ambos existem, a nota é criada.
Caso contrário, retorna erro 400.
Características da Comunicação
Característica	Descrição
Tipo	Síncrona (bloqueante)
Protocolo	HTTP/REST
Biblioteca	requests (Python)
Método	GET para validações
Timeout	Padrão do requests
Tratamento de Erro	Try/except com fallback para False
⚙️ Estrutura do Projeto
Aplicacao-Monolitica-Completa/
│
├── gerenciamento/                    # Microsserviço de Gerenciamento
│   ├── app.py                        # Aplicação Flask principal
│   ├── routes.py                     # Definição das rotas/endpoints
│   ├── models.py                     # Modelos SQLAlchemy (Aluno, Professor, Turma)
│   ├── requirements.txt              # Dependências Python
│   └── Dockerfile                    # Container do serviço
│
├── reservas/                         # Microsserviço de Reservas
│   ├── app.py                        # Aplicação Flask principal
│   ├── routes.py                     # Definição das rotas/endpoints
│   ├── models.py                     # Modelo SQLAlchemy (Reserva)
│   ├── extensions.py                 # Extensões Flask (db, api)
│   ├── services/
│   │   └── gerenciamento_client.py   # Cliente HTTP para Gerenciamento
│   ├── requirements.txt              # Dependências Python
│   └── Dockerfile                    # Container do serviço
│
├── atividades/                       # Microsserviço de Atividades
│   ├── app.py                        # Aplicação Flask principal
│   ├── routes.py                     # Definição das rotas/endpoints
│   ├── models.py                     # Modelos SQLAlchemy (Atividade, Nota)
│   ├── extensions.py                 # Extensões Flask (db, api)
│   ├── services/
│   │   └── gerenciamento_client.py   # Cliente HTTP para Gerenciamento
│   ├── requirements.txt              # Dependências Python
│   └── Dockerfile                    # Container do serviço
│
├── docker-compose.yml                # Orquestração dos containers
└── README.md                         # Este arquivo
🚀 Instruções de Execução
Pré-requisitos
Certifique-se de ter instalado:

Docker (versão 20.10 ou superior)
Docker Compose (versão 1.29 ou superior)
Para verificar as versões instaladas:

bash
Copy
docker --version
docker-compose --version
Passo 1: Clonar o Repositório
bash
Copy
git clone https://github.com/seuusuario/Aplicacao-Monolitica-Completa.git
cd Aplicacao-Monolitica-Completa
Passo 2: Construir e Iniciar os Containers
Execute o comando para construir as imagens e iniciar todos os serviços:

bash
Copy
docker-compose up --build
O que acontece:

Docker Compose lê o arquivo docker-compose.yml.
Constrói as imagens Docker de cada serviço.
Cria os containers e configura a rede interna para comunicação.
Expõe as portas 5000, 5001 e 5002 no host.
Inicia os três serviços simultaneamente.
Saída esperada:

Creating network "aplicacao-monolitica-completa_default" with the default driver
Building gerenciamento
Building reservas
Building atividades
Creating gerenciamento ... done
Creating reservas      ... done
Creating atividades    ... done
Attaching to gerenciamento, reservas, atividades
Passo 3: Verificar se os Serviços Estão Rodando
Abra outro terminal e execute:

bash
Copy
docker-compose ps
Saída esperada:

       Name                     Command               State           Ports
-----------------------------------------------------------------------------------
gerenciamento         python app.py                    Up      0.0.0.0:5000->5000/tcp
reservas              python app.py                    Up      0.0.0.0:5001->5001/tcp
atividades            python app.py                    Up      0.0.0.0:5002->5002/tcp
Passo 4: Acessar os Serviços
Serviço	URL Base	Documentação Swagger
Gerenciamento	http://localhost:5000/	http://localhost:5000/apidocs
Reservas	http://localhost:5001/	http://localhost:5001/docs
Atividades	http://localhost:5002/	http://localhost:5002/docs
Comandos Úteis
Parar os serviços:

bash
Copy
docker-compose down
Ver logs de um serviço específico:

bash
Copy
docker-compose logs -f gerenciamento
docker-compose logs -f reservas
docker-compose logs -f atividades
Reiniciar um serviço específico:

bash
Copy
docker-compose restart reservas
Reconstruir após mudanças no código:

bash
Copy
docker-compose up --build
Executar em background (modo detached):

bash
Copy
docker-compose up -d
📚 Descrição da API
1️⃣ Microsserviço: Gerenciamento
Responsabilidade: Gerenciar o cadastro de alunos, professores e turmas.
Base URL: http://localhost:5000
Documentação Swagger: http://localhost:5000/apidocs

Endpoints - Alunos
Método	Endpoint	Descrição	Body (JSON)
GET	/alunos	Lista todos os alunos	-
GET	/alunos/{id}	Busca aluno por ID	-
POST	/alunos	Cria novo aluno	{"nome": "João Silva", "matricula": "2024001"}
PUT	/alunos/{id}	Atualiza aluno	{"nome": "João Silva Jr."}
DELETE	/alunos/{id}	Remove aluno	-
Exemplo de Resposta (GET /alunos):

json
Copy
[
  {
    "id": 1,
    "nome": "João Silva",
    "matricula": "2024001"
  },
  {
    "id": 2,
    "nome": "Maria Santos",
    "matricula": "2024002"
  }
]
Endpoints - Professores
Método	Endpoint	Descrição	Body (JSON)
GET	/professores	Lista todos os professores	-
GET	/professores/{id}	Busca professor por ID	-
POST	/professores	Cria novo professor	{"nome": "Dr. Carlos", "disciplina": "Matemática"}
PUT	/professores/{id}	Atualiza professor	{"disciplina": "Física"}
DELETE	/professores/{id}	Remove professor	-
Endpoints - Turmas
Método	Endpoint	Descrição	Body (JSON)
GET	/turmas	Lista todas as turmas	-
GET	/turmas/{id}	Busca turma por ID	-
POST	/turmas	Cria nova turma	{"nome": "3º Ano A", "ano": 2025}
PUT	/turmas/{id}	Atualiza turma	{"nome": "3º Ano B"}
DELETE	/turmas/{id}	Remove turma	-
2️⃣ Microsserviço: Reservas
Responsabilidade: Gerenciar reservas de salas e laboratórios.
Base URL: http://localhost:5001
Documentação Swagger: http://localhost:5001/docs
Integração: Valida turma_id com o serviço Gerenciamento antes de criar a reserva.

Endpoints - Reservas
Método	Endpoint	Descrição	Body (JSON)
GET	/reservas	Lista todas as reservas	-
GET	/reservas/{id}	Busca reserva por ID	-
POST	/reservas	Cria nova reserva	Ver exemplo abaixo
PUT	/reservas/{id}	Atualiza reserva	Ver exemplo abaixo
DELETE	/reservas/{id}	Remove reserva	-
Exemplo de Criação (POST /reservas):

json
Copy
{
  "num_sala": "Lab A",
  "lab": "Computação",
  "data": "2025-11-15",
  "turma_id": 1
}
Validação:

O sistema verifica se turma_id=1 existe no serviço Gerenciamento.
Se não existir, retorna erro 400: {"error": "Turma não encontrada"}.
Exemplo de Resposta (GET /reservas):

json
Copy
[
  {
    "id": 1,
    "num_sala": "Lab A",
    "lab": "Computação",
    "data": "2025-11-15",
    "turma_id": 1
  }
]
3️⃣ Microsserviço: Atividades
Responsabilidade: Gerenciar atividades avaliativas e notas dos alunos.
Base URL: http://localhost:5002
Documentação Swagger: http://localhost:5002/docs
Integração: Valida turma_id, professor_id e aluno_id com o serviço Gerenciamento.

Endpoints - Atividades
Método	Endpoint	Descrição	Body (JSON)
GET	/atividades	Lista todas as atividades	-
GET	/atividades/{id}	Busca atividade por ID	-
POST	/atividades	Cria nova atividade	Ver exemplo abaixo
PUT	/atividades/{id}	Atualiza atividade	Ver exemplo abaixo
DELETE	/atividades/{id}	Remove atividade	-
Exemplo de Criação (POST /atividades):

json
Copy
{
  "nome_atividade": "Prova 1 - Flask",
  "descricao": "Avaliação sobre desenvolvimento web com Flask",
  "peso_porcento": 30,
  "data_entrega": "2025-11-20",
  "turma_id": 1,
  "professor_id": 2
}
Validações:

Verifica se turma_id=1 existe no Gerenciamento.
Verifica se professor_id=2 existe no Gerenciamento.
Se algum não existir, retorna erro 400.
Endpoints - Notas
Método	Endpoint	Descrição	Body (JSON)
GET	/atividades/notas	Lista todas as notas	-
GET	/atividades/notas/{id}	Busca nota por ID	-
POST	/atividades/notas	Cria nova nota	Ver exemplo abaixo
PUT	/atividades/notas/{id}	Atualiza nota	{"nota": 9.5}
DELETE	/atividades/notas/{id}	Remove nota	-
Exemplo de Criação (POST /atividades/notas):

json
Copy
{
  "nota": 8.5,
  "aluno_id": 1,
  "atividade_id": 1
}
Validações:

Verifica se aluno_id=1 existe no Gerenciamento.
Verifica se atividade_id=1 existe localmente.
Se algum não existir, retorna erro 400.
Exemplo de Resposta (GET /atividades/notas):

json
Copy
[
  {
    "id": 1,
    "nota": 8.5,
    "aluno_id": 1,
    "atividade_id": 1
  }
]
🧪 Testando a API
Usando cURL
1. Criar um aluno:

bash
Copy
curl -X POST http://localhost:5000/alunos \
  -H "Content-Type: application/json" \
  -d '{"nome":"João Silva","matricula":"2024001"}'
2. Criar uma turma:

bash
Copy
curl -X POST http://localhost:5000/turmas \
  -H "Content-Type: application/json" \
  -d '{"nome":"3º Ano A","ano":2025}'
3. Criar uma reserva (com validação):

bash
Copy
curl -X POST http://localhost:5001/reservas \
  -H "Content-Type: application/json" \
  -d '{"num_sala":"Lab A","lab":"Computação","data":"2025-11-15","turma_id":1}'
4. Listar atividades:

bash
Copy
curl http://localhost:5002/atividades
Usando Swagger UI
Cada serviço possui uma interface Swagger interativa:

Gerenciamento: Acesse http://localhost:5000/apidocs
Reservas: Acesse http://localhost:5001/docs
Atividades: Acesse http://localhost:5002/docs
Na interface Swagger você pode:

Ver todos os endpoints disponíveis.
Testar requisições diretamente no navegador.
Ver exemplos de request/response.
Validar schemas JSON.
🔐 Configuração do Banco de Dados
Padrão: SQLite
Por padrão, cada serviço usa SQLite com bancos separados:

gerenciamento/escola.db
reservas/reservas.db
atividades/atividades.db
Os bancos são criados automaticamente na primeira execução via db.create_all().

Migração para PostgreSQL
Para usar PostgreSQL em produção, altere a configuração em cada app.py:

python
Copy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:senha@db:5432/escola'
E adicione o serviço PostgreSQL no docker-compose.yml:

yaml
Copy
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: usuario
      POSTGRES_PASSWORD: senha
      POSTGRES_DB: escola
    ports:
      - "5432:5432"
🛠 Desenvolvimento Local
Executar um serviço individualmente (sem Docker)
bash
Copy
cd reservas
pip install -r requirements.txt
flask run --host=0.0.0.0 --port=5001
Nota: Para a comunicação entre serviços funcionar localmente, altere as URLs de http://gerenciamento:5000 para http://localhost:5000 nos arquivos gerenciamento_client.py.

🧩 Tecnologias Utilizadas
Tecnologia	Versão	Uso
Python	3.9+	Linguagem principal
Flask	2.x	Framework web
Flask-RESTX	1.x	API REST + Swagger
Flasgger	0.9.x	Documentação Swagger (Gerenciamento)
SQLAlchemy	1.4+	ORM para banco de dados
Requests	2.x	Cliente HTTP para comunicação entre serviços
Docker	20.10+	Containerização
Docker Compose	1.29+	Orquestração de containers
📊 Padrões e Boas Práticas Implementadas
✅ Separação de responsabilidades - Cada serviço tem uma função específica.
✅ Comunicação via API REST - Protocolo HTTP padrão da indústria.
✅ Validação de dados - Verificação de integridade referencial entre serviços.
✅ Documentação automática - Swagger UI em todos os serviços.
✅ Containerização - Isolamento e portabilidade com Docker.
✅ Tratamento de erros - Try/except em chamadas HTTP.
✅ Código modular - Separação em routes, models, services.

🤝 Contribuições
Pull requests são bem-vindos! Para mudanças importantes:

Faça um fork do projeto.
Crie uma branch para sua feature (git checkout -b feature/NovaFuncionalidade).
Commit suas mudanças (git commit -m 'Adiciona nova funcionalidade').
Push para a branch (git push origin feature/NovaFuncionalidade).
Abra um Pull Request.
📝 Licença
Este projeto é de código aberto e está disponível sob a licença MIT.

👨‍💻 Autores e Créditos
Desenvolvimento e implementação: Você 🙌
Documentação e suporte técnico: Claude Sonnet 4.5 (Abacus.AI)
📅 Última Atualização
09 de Novembro de 2025

📞 Suporte
Para dúvidas ou problemas:

Abra uma issue no GitHub.
Entre em contato via email: seu-email@exemplo.com.
🎓 Projeto desenvolvido como parte da disciplina de Arquitetura de Microsserviços
