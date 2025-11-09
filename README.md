# Aplicação Escolar - Microsserviços

Integrantes - Artur Farrardo ; Thiago Lopes

## Execução e integração entre serviços
O projeto é composto por **três microsserviços** independentes que se integram por chamadas HTTP internas (nome de serviço do Docker). Cada serviço roda em seu próprio container e possui sua própria base de dados SQLite localizada em `/<serviço>/instance/*.db`.  
Os serviços são:
- `gerenciamento` — fornece recursos centrais de gestão (professores, turmas, alunos).
- `reservas` — gerencia reservas de salas/laboratórios.
- `atividades` — gerencia atividades e notas; também consome serviços do `gerenciamento` para validação de turmas/professores/alunos.

A integração entre serviços ocorre via chamadas REST HTTP. Os serviços `atividades` e `reservas` consultam o serviço `gerenciamento` usando a variável de ambiente `GERENCIAMENTO_URL` (por padrão apontando para `http://gerenciamento:5000` dentro da rede do Docker Compose).

---

## Descrição da API
**gerenciamento**
- Recursos principais: `/professores`, `/turmas`, `/alunos`
- Endpoints CRUD para cada recurso (GET list, GET by id, POST, PUT, DELETE)
- Swagger/UI disponível no serviço para documentação (configurado no app do serviço)

**reservas**
- Namespace: `/reservas`
- Endpoints CRUD para reservas: criar, listar, atualizar, deletar reservas.
- Antes de criar/atualizar uma reserva, valida `turma_id` consultando `gerenciamento` via `GERENCIAMENTO_URL`.

**atividades**
- Namespace: `/atividades` (gerencia atividades e notas)
- Endpoints CRUD para atividades e para notas associadas a alunos/atividades.
- Antes de criar/atualizar, valida `turma_id`, `professor_id` e `aluno_id` chamando `gerenciamento` via `GERENCIAMENTO_URL`.

Observação: cada serviço expõe rotas REST compatíveis com Flask/Flask-RESTX; a documentação interativa (Swagger) está configurada nos serviços que usam `flask_restx`/`swagger`.

---

## Instruções de execução (com Docker)
Pré-requisitos: Docker e Docker Compose instalados.

No diretório raiz do projeto (onde está o `docker-compose.yaml`), execute:
```bash
docker-compose up --build
```

Comportamento após subir:
- Container `gerenciamento` expõe a aplicação na porta `5000` (mapeada `5000:5000`).
- Container `atividades` está mapeado para porta externa `5002` (map `5002:5000`).
- `reservas` roda no container mas não possui mapeamento de porta externo no `docker-compose.yaml` (acesso via rede Docker pelos nomes dos serviços).
- `atividades` e `reservas` dependem do `gerenciamento` para validações (o `docker-compose` já define ligação entre containers).

Para parar e remover containers:
```bash
docker-compose down
```

---

## Explicação da arquitetura utilizada
Arquitetura adotada: **microserviços simples** com serviços independentes implementados em Flask (cada um com seu próprio código, dependências e banco SQLite local). Cada serviço contém:
- camada de rotas/controllers (API REST),
- camada de modelos (SQLAlchemy),
- lógica de aplicação/serviços internos,
- cliente HTTP para comunicação com outros serviços quando necessário.

Vantagens dessa abordagem no projeto:
- Independência de deploy e ciclo de vida por serviço.
- Separação de responsabilidades (gestão escolar vs reservas vs atividades).
- Facilidade para escalar ou migrar individualmente cada serviço.

---

## Descrição do ecossistema de microsserviços, destacando integração entre serviços
- **Comunicação:** Serviços se comunicam por **HTTP REST**. As chamadas entre serviços usam o nome do container definido no `docker-compose` (por exemplo `http://gerenciamento:5000`), configurado via variável de ambiente `GERENCIAMENTO_URL`.
- **Serviços que consomem `gerenciamento`:**
  - `atividades` usa `gerenciamento` para verificar `turma_id`, `professor_id` e `aluno_id` (`services/gerenciamento_client.py`).
  - `reservas` usa `gerenciamento` para verificar `turma_id` antes de persistir reservas.
- **Persistência:** Cada serviço mantém seu próprio banco SQLite em `/<serviço>/instance/*.db` (ex.: `gerenciamento/instance/escola.db`, `atividades/instance/atividades.db`, `reservas/instance/reservas.db`), evitando dependência direta de uma mesma base compartilhada.
- **Configuração de integração:** a URL base do serviço de gerenciamento é passada via variável de ambiente `GERENCIAMENTO_URL`. Em ambiente Docker Compose, isso é configurado no `docker-compose.yaml` (e internamente os containers resolvem os nomes um do outro).
- **Descobrimento:** o projeto usa o mecanismo nativo de descoberta do Docker Compose (resolução de nomes de container na rede criada pelo Compose). Não há serviço de discovery externo nem mensageria; a integração é síncrona via REST.
- **Documentação/contratos:** cada serviço expõe documentação (Swagger/Flask-RESTX) localmente, permitindo verificar contratos de API por serviço.

---
