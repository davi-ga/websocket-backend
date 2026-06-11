
# Websocket Back-end

API REST + WebSocket para chat em tempo real entre usuários, desenvolvida como teste técnico para a YellotMob.

## Sumário

- [Stack](#stack)
- [Arquitetura](#arquitetura)
- [Endpoints da API](#endpoints-da-api)
  - [Autenticação](#autenticação)
  - [Usuários](#usuários)
  - [Salas](#salas)
  - [Utilitários](#utilitários)
- [WebSocket](#websocket)
- [Como executar](#como-executar)
- [Acessando a aplicação](#acessando-a-aplicação)
- [Testes](#testes)

## Stack

| Camada | Tecnologia |
|---|---|
| Framework | Django 5.1 + Django REST Framework |
| ASGI / WebSocket | Daphne + Django Channels 4 |
| Banco de dados | PostgreSQL 17 |
| Channel layer | Redis |
| Documentação | drf-spectacular (Swagger / ReDoc) |
| Testes | pytest-django + pytest-cov |
| Containers | Docker Compose |

## Arquitetura

```
core/               # Configurações globais
  api/              # Centralização de URLs da API
  health/           # Verificação de status do projeto
  swagger/          # Documentação do projeto
  utils/            # Utilitários globais
features/
  authentication/   # Login e logout via sessão (cookie)
  users/            # Cadastro e perfil de usuário
  rooms/            # Salas de chat (REST + WebSocket consumer)
```

O servidor utiliza **sessões Django** como mecanismo de autenticação. O cookie `sessionid` gerado no login é também usado para autenticar conexões WebSocket.

## Decisões

### Django Sessions

A rota WebSocket utiliza `AuthMiddlewareStack` do Django Channels, que autentica conexões a partir da sessão Django já existente no cookie. Adotar JWT exigiria um middleware customizado para extrair e validar o token na URL da conexão, além de lógica de renovação via `refresh_token`. Dado o escopo do projeto e a familiaridade com `AuthMiddlewareStack`, optou-se por manter Django Sessions.

**CSRF:** Por padrão, o Django exige o `csrf_token` em requisições `POST`, o que dificulta testes via Postman/Insomnia. Para contornar isso foi criada a classe `CsrfExemptSessionAuthentication`, que sobrescreve `enforce_csrf` sem executar a validação. Essa abordagem é adequada para demonstração, mas em produção o gerenciamento do CSRF token deve ser feito pelo front-end.

### Redis

O Redis é utilizado tanto como Channel Layer para o Django Channels quanto como backend de cache. Por ser leve, de fácil integração com o Django e amplamente adotado em ambientes de desenvolvimento, ele é provisionado via Docker como um serviço dedicado no compose.

### Estruturação do Sistema

A aplicação segue uma arquitetura orientada a features, toda a lógica de negócio reside em `features/`, com cada módulo encapsulando seus próprios models, views, serializers, rotas e testes. O `core/` concentra apenas configurações globais e utilitários transversais, como Swagger e Health Check, garantindo baixo acoplamento entre os domínios.

### Containers

O `docker-compose.yml` define uma rede interna compartilhada entre todos os serviços, volumes persistentes para o banco de dados e o Redis, e healthchecks customizados que garantem que cada serviço só seja considerado pronto após responder corretamente, evitando condições de corrida na inicialização.

### Usuário

O model de usuário foi customizado a partir do `AbstractBaseUser` em conjunto com um `BaseUserManager` personalizado, substituindo o `username` pelo `email` como identificador principal e adicionando o campo `name`. Essa abordagem mantém compatibilidade total com o sistema de autenticação e permissões do Django.

### Consumer

O `ChatConsumer` estende `AsyncWebsocketConsumer` seguindo as convenções do Django Channels, sobrescrevendo `connect`, `disconnect` e `receive` para gerenciar o ciclo de vida da conexão, a entrada e saída do grupo da sala e o recebimento e persistência de mensagens.

### HiddenField

Foi implementada uma subclasse de `HiddenField` que resolve o usuário autenticado diretamente a partir do `request` disponível no contexto do serializer. Com isso, os campos de autoria (criador da sala, remetente da mensagem) são preenchidos automaticamente, sem expô-los na entrada da API.

### Testes

Os testes utilizam `pytest` + `pytest-django`, com fixtures centralizadas em `conftest.py` que cobrem criação de usuários, salas, mensagens, `APIClient` autenticado, `APIRequestFactory` e mocks de usuário para testes assíncronos.

A estrutura segue a separação por camada onde cada arquivo de teste cobre uma frente específica entre Model, View e Serializer. Testes do `core` e do `consumer` fogem desse padrão por natureza, e cada função de teste possui um único foco de verificação.

Os testes do consumer utilizam `WebsocketCommunicator` do `channels.testing` para simular conexões reais. Dependências externas (`get_room`, `save_message`) são isoladas via `unittest.mock.patch`, e usuários autenticados são injetados diretamente no `scope` como `MagicMock`, eliminando acesso ao banco durante os testes de conexão.

A cobertura total medida com `pytest-cov` é de **99%**.



## Endpoints da API

### Autenticação
| Método | URL | Descrição |
|---|---|---|
| `POST` | `/api/auth/login/` | Login - cria sessão e retorna cookie |
| `POST` | `/api/auth/logout/` | Logout - invalida a sessão |

### Usuários
| Método | URL | Descrição | Auth |
|---|---|---|---|
| `POST` | `/api/users/` | Criar conta | Não |
| `GET` | `/api/users/me/` | Dados do usuário autenticado | Sim |

### Salas
| Método | URL | Descrição | Auth |
|---|---|---|---|
| `GET` | `/api/rooms/` | Listar salas | Sim |
| `POST` | `/api/rooms/` | Criar sala | Sim |
| `GET` | `/api/rooms/{id}/` | Detalhe da sala com histórico de mensagens | Sim |

### Utilitários
| Método | URL | Descrição |
|---|---|---|
| `GET` | `/api/health/` | Health check |
| `GET` | `/api/docs/swagger-ui/` | Documentação interativa (Swagger) |
| `GET` | `/api/docs/schema/redoc/` | Documentação (ReDoc) |

## WebSocket

```
ws://localhost:{API_PORT}/room/{id}/chat/
```

- Requer o cookie `sessionid` (obtido após login).
- Conexões de usuários não autenticados são rejeitadas.
- **Mensagens enviadas** (JSON):
  ```json
  { "message": "texto da mensagem" }
  ```
- **Mensagens recebidas** (JSON):
  ```json
  { "username": "nome do autor", "message": "texto da mensagem" }
  ```
- Mensagens de sistema (`"username": "system"`) são emitidas automaticamente quando um usuário entra ou sai da sala.
- Todas as mensagens são persistidas no banco de dados.

## Como executar

### 1. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

Edite o `.env` com as configurações do banco, Redis e chave secreta.

### 2. Subir os containers

```bash
docker compose up --build
```

Isso inicializa o PostgreSQL, o Redis e a API (com migrações automáticas na inicialização).

### 3. Criar superusuário (opcional)

```bash
docker compose exec wapi python manage.py createsuperuser
```

## Acessando a aplicação

- **API**: `http://localhost:{API_PORT}`
- **Swagger UI**: `http://localhost:{API_PORT}/api/docs/swagger-ui/`
- **Admin**: `http://localhost:{API_PORT}/admin/`
- **Chat (template de teste)**: `http://localhost:{API_PORT}/chat/`

## Testes

```bash
# Executar todos os testes com cobertura
docker compose exec -it wapi pytest

# Executar testes de um módulo específico
docker compose exec -it wapi pytest features/rooms/tests/
```
