# 🎓 Sistema de Gestão Escolar - Arquitetura de Microsserviços

> Plataforma modular para gerenciamento acadêmico com APIs independentes e escaláveis.

---

## 👥 Equipe de Desenvolvimento

- Artur Farrardo
- Thiago Lopes

## 📋 Sobre o Projeto

Este sistema foi desenvolvido utilizando **arquitetura de microsserviços** para gerenciar operações escolares de forma distribuída e eficiente. Cada módulo opera de forma independente, facilitando manutenção, escalabilidade e integração.

### Microsserviços disponíveis:

| Serviço | Responsabilidade | Porta |
|---------|------------------|-------|
| **Gerenciamento** | Cadastro de alunos, turmas e professores | 1300 |
| **Agendamentos** | Reserva de salas e laboratórios | 1301 |
| **Tarefas** | Gestão de atividades escolares e avaliações | 1302 |

---

## 🚀 Como Executar

### Pré-requisitos

- [Docker](https://www.docker.com/get-started) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) configurado

### 1️⃣ Subir os containers

No diretório raiz do projeto (onde está o `docker-compose.yml`), execute:

```bash
docker-compose up --build
```

Esse comando irá:
- Construir as imagens Docker de cada microsserviço
- Inicializar os bancos de dados SQLite
- Expor as APIs nas portas configuradas

Aguarde até que todas as mensagens de inicialização apareçam no terminal.

---

### 2️⃣ Verificar status dos containers

Em outro terminal, execute:

```bash
docker ps
```

Você deverá ver 3 containers rodando:
- `gerenciamento`
- `agendamentos`
- `tarefas`

---

## 🌐 Acessando as APIs

Após a inicialização, os serviços estarão disponíveis nos seguintes endereços:

| Microsserviço | URL Base |
|---------------|----------|
| **Gerenciamento** | [http://localhost:1300](http://localhost:8500) |
| **Agendamentos** | [http://localhost:1301](http://localhost:8501) |
| **Tarefas** | [http://localhost:1302](http://localhost:8502) |

---

## 📚 Documentação Interativa (Swagger)

Cada microsserviço possui documentação automática gerada pelo **Swagger UI**, permitindo testar endpoints diretamente no navegador:

| Serviço | Swagger UI |
|---------|------------|
| **Gerenciamento** | [http://localhost:8500/apidocs](http://localhost:1300/apidocs) |
| **Agendamentos** | [http://localhost:8501/apidocs](http://localhost:1301/apidocs) |
| **Tarefas** | [http://localhost:8502/apidocs](http://localhost:1302/apidocs) |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x** com Flask
- **SQLAlchemy** para ORM
- **SQLite** como banco de dados
- **Docker & Docker Compose** para containerização
- **Flasgger** para documentação Swagger
- **Arquitetura de Microsserviços** com comunicação via HTTP

---

## 🗂️ Estrutura do Projeto

```
.
├── docker-compose.yml
├── gerenciamento/
│   ├── app.py
│   ├── config.py
│   ├── models/
│   └── controllers/
├── agendamentos/
│   ├── app.py
│   ├── config.py
│   ├── models/
│   └── controllers/
└── tarefas/
    ├── app.py
    ├── config.py
    ├── models/
    └── controllers/
```

Cada microsserviço possui:
- **app.py**: Configuração principal e rotas
- **config.py**: Configurações de banco e ambiente
- **models/**: Definição das entidades do banco
- **controllers/**: Lógica de negócio e manipulação de dados

---

## 🔄 Comandos Úteis

### Parar os containers
```bash
docker-compose down
```

### Reiniciar um serviço específico
```bash
docker-compose restart tarefas
```

### Ver logs de um serviço
```bash
docker logs -f tarefas
```

### Remover volumes (limpar bancos de dados)
```bash
docker-compose down -v
```

---

## 🧪 Testando a API

Exemplo de requisição para listar tarefas:

```bash
curl http://localhost:8502/tarefas
```

Ou acesse diretamente pelo Swagger UI para testar de forma interativa.

---
