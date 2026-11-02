# Dio Bank

API bancária assíncrona desenvolvida com FastAPI como projeto de estudo da Formação Python Backend Developer da DIO.

A aplicação oferece cadastro de contas, autenticação JWT e operações financeiras internas entre contas do mesmo banco.

## Tecnologias

- Python 3.14+
- FastAPI
- Uvicorn
- Poetry
- Pydantic Settings
- `databases` com SQLite e aiosqlite
- SQLAlchemy Core
- Alembic
- PyJWT
- Ruff

## Escopo atual

A aplicação contempla:

- criação de contas;
- consulta autenticada de contas;
- cancelamento autenticado de contas;
- login por `user_id` com emissão de token JWT;
- depósito;
- saque com validação de saldo;
- extrato;
- transferência interna;
- PIX interno;
- TED interno;
- documentação OpenAPI pelo Swagger.

As operações de PIX, TED e transferência são internas. Integrações com bancos externos, chaves PIX, tarifas e liquidação interbancária não fazem parte do escopo atual.

## Requisitos

- Python 3.14 ou superior;
- Poetry 2.5.1 ou compatível;
- Git.

## Configuração

Copie o arquivo de exemplo para criar o arquivo local de configuração.

No PowerShell, na raiz do projeto, copie o arquivo de exemplo para criar o arquivo local de configuração:

```powershell
Copy-Item .env.example .env
```

Revise o `.env` e defina uma chave JWT local forte em `JWT_SECRET_KEY`. O arquivo `.env` não deve ser versionado.

Variáveis utilizadas:

```text
ENVIRONMENT=local
DATABASE_URL=sqlite:///./bank.db
JWT_SECRET_KEY=<chave-secreta-local>
```

## Instalação e execução no Windows

Na raiz do projeto, instale as dependências:

```powershell
poetry install
```

Inicie a aplicação:

```powershell
poetry run uvicorn src.main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

## Banco de dados e migrations

O banco local utilizado no desenvolvimento é o SQLite, definido por `DATABASE_URL`.

Para aplicar as migrations:

```powershell
poetry run alembic upgrade head
```

Para verificar se o schema está alinhado aos models:

```powershell
poetry run alembic check
```

## Documentação da API

Com a aplicação em execução, acesse:

- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>
- OpenAPI JSON: <http://127.0.0.1:8000/openapi.json>

## Autenticação

O login é público e utiliza `user_id`:

```http
POST /auth/login
Content-Type: application/json
```

```json
{
  "user_id": 123
}
```

A resposta contém um `access_token`. No Swagger, clique em `Authorize` e informe:

```text
Bearer <access_token>
```

Não compartilhe tokens reais.

## Endpoints

### Sistema

| Método | Rota | Autenticação | Descrição |
| --- | --- | --- | --- |
| GET | `/` | Não | Verifica a disponibilidade da API. |

### Contas

| Método | Rota | Autenticação | Descrição |
| --- | --- | --- | --- |
| POST | `/accounts/` | Não | Cria uma conta pública vinculada ao `user_id`. |
| GET | `/accounts/` | JWT | Lista contas. Requer `limit` e aceita `skip`. |
| PATCH | `/accounts/{account_id}/cancel` | JWT | Cancela uma conta ativa. |

Exemplo de criação:

```json
{
  "user_id": 123
}
```

Exemplo de cancelamento:

```json
{
  "cancellation": "request_holder",
  "notes_cancellation": "Solicitação do titular"
}
```

Os valores aceitos para `cancellation` são:

- `request_holder`;
- `other_reasons`.

### Transações

Todas as rotas de transação exigem JWT.

| Método | Rota | Descrição |
| --- | --- | --- |
| POST | `/transactions/deposit` | Deposita valor positivo em uma conta. |
| POST | `/transactions/withdraw` | Saca valor positivo com validação de saldo. |
| GET | `/transactions/{account_id}/statement` | Consulta o extrato de uma conta. |
| POST | `/transactions/transfer` | Transfere entre duas contas internas. |
| POST | `/transactions/pix` | Realiza PIX interno entre duas contas. |
| POST | `/transactions/ted` | Realiza TED interno entre duas contas. |

Exemplo de depósito ou saque:

```json
{
  "account_id": 1,
  "amount": 100.0
}
```

Exemplo de transferência, PIX ou TED:

```json
{
  "source_account_id": 1,
  "destination_account_id": 2,
  "amount": 50.0
}
```

## Estrutura principal

```text
dio_bank/
├── migrations/              # migrations do Alembic
├── src/
│   ├── controllers/         # camada HTTP e rotas
│   ├── models/              # tabelas SQLAlchemy Core
│   ├── schemas/             # contratos Pydantic
│   ├── services/            # regras de negócio
│   ├── config.py            # configurações do ambiente
│   ├── database.py          # conexão e metadata
│   ├── exceptions.py        # exceções de negócio
│   ├── main.py              # aplicação FastAPI
│   └── security.py          # autenticação JWT
├── .env.example
├── alembic.ini
├── poetry.lock
└── pyproject.toml
```

## Verificações locais

Com o ambiente configurado, execute:

```powershell
poetry run python -m py_compile src/*.py src/controllers/*.py src/models/*.py src/schemas/*.py src/services/*.py
poetry run alembic check
```

Para validar o projeto, execute também:

```powershell
poetry run ruff check .
```

## Referências

- Desafio Dio Bank: <https://web.dio.me/lab/apis-assincronas-com-fastapi>
- FastAPI: <https://fastapi.tiangolo.com/>
- Segurança OAuth2/JWT no FastAPI: <https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/>
- OpenAPI e metadados no FastAPI: <https://fastapi.tiangolo.com/tutorial/metadata/>
- Poetry: <https://python-poetry.org/docs/>
- Alembic: <https://alembic.sqlalchemy.org/tutorial.html>
