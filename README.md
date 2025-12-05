# Backend MVP - A/B Testing (Landing Única)

Servidor FastAPI para distribuição de variações de landing page com base em percentuais, registro de impressões e conversões.

> **Versão:** 0.1.0  
> **Python:** >=3.8  
> **Framework:** FastAPI
teste se foi pro ar

## 📑 Índice

- [Objetivo](#-objetivo)
- [Funcionalidades MVP](#-funcionalidades-mvp)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação](#-instalação)
- [Como Usar - Guia Passo a Passo](#-como-usar---guia-passo-a-passo)
- [Endpoints Detalhados](#-endpoints-detalhados)
- [Fluxo Completo de Uso](#-fluxo-completo-de-uso)
- [Como Funciona a Distribuição](#-como-funciona-a-distribuição)
- [Armazenamento](#️-armazenamento)
- [Documentação Interativa](#-documentação-interativa)
- [Considerações Técnicas](#-considerações-técnicas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Troubleshooting](#-troubleshooting)
- [Testando a API](#-testando-a-api)
- [Exemplos Completos](#-exemplos-completos)
- [Segurança e Produção](#-segurança-e-produção)

## 🎯 Objetivo

Fornecer um backend simples capaz de:
- Distribuir variações de uma landing page com base em percentuais configuráveis
- Registrar impressões (visualizações) e conversões
- Fornecer métricas de desempenho por variante

## 📋 Funcionalidades MVP

- 1 experimento ativo por vez
- 2+ variantes com distribuição percentual configurável
- Seções pré-definidas por variante
- Registro de impressões
- Registro de conversões
- Métricas de conversão por variante
- Sem autenticação administrativa (pode ser adicionada depois)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- PDM (opcional, mas recomendado) ou pip

## 🚀 Instalação

### Com PDM (recomendado)

1. Instale o PDM (se ainda não tiver):
```bash
pip install pdm
```

2. Configure o projeto:
```bash
pdm install
```

3. Execute o servidor:
```bash
pdm run uvicorn main:app --reload
```

### Com pip

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o servidor:
```bash
uvicorn main:app --reload
```

O servidor estará disponível em `http://localhost:8000`

### Verificar Instalação

Após iniciar o servidor, você pode verificar se está funcionando acessando:
- **Documentação interativa:** `http://localhost:8000/docs`
- **Endpoint raiz:** `http://localhost:8000/`

## 📖 Como Usar - Guia Passo a Passo

### Passo 1: Criar um Experimento

Primeiro, você precisa criar um experimento A/B definindo as variantes e suas distribuições.

**Exemplo:** Criar um teste com 2 variantes (50% cada)

```bash
curl -X POST "http://localhost:8000/admin/test" \
  -H "Content-Type: application/json" \
  -d '{
    "testId": "landing_001",
    "name": "Teste de Landing Page",
    "variants": [
      {
        "variantId": "A",
        "distribution": 50,
        "sections": [
          { "id": "hero_a", "contentUrl": "https://cdn.exemplo.com/hero_a.html" },
          { "id": "features_a", "contentUrl": "https://cdn.exemplo.com/features_a.html" },
          { "id": "cta_a", "contentUrl": "https://cdn.exemplo.com/cta_a.html" }
        ]
      },
      {
        "variantId": "B",
        "distribution": 50,
        "sections": [
          { "id": "hero_b", "contentUrl": "https://cdn.exemplo.com/hero_b.html" },
          { "id": "features_b", "contentUrl": "https://cdn.exemplo.com/features_b.html" },
          { "id": "cta_b", "contentUrl": "https://cdn.exemplo.com/cta_b.html" }
        ]
      }
    ]
  }'
```

**Resposta:**
```json
{
  "ok": true,
  "message": "Test created"
}
```

**⚠️ Importante:** A soma das distribuições deve ser exatamente 100.

**Exemplo com 3 variantes (30%, 40%, 30%):**
```bash
curl -X POST "http://localhost:8000/admin/test" \
  -H "Content-Type: application/json" \
  -d '{
    "testId": "landing_002",
    "name": "Teste com 3 Variantes",
    "variants": [
      {
        "variantId": "A",
        "distribution": 30,
        "sections": [
          { "id": "hero_a", "contentUrl": "https://cdn.exemplo.com/hero_a.html" }
        ]
      },
      {
        "variantId": "B",
        "distribution": 40,
        "sections": [
          { "id": "hero_b", "contentUrl": "https://cdn.exemplo.com/hero_b.html" }
        ]
      },
      {
        "variantId": "C",
        "distribution": 30,
        "sections": [
          { "id": "hero_c", "contentUrl": "https://cdn.exemplo.com/hero_c.html" }
        ]
      }
    ]
  }'
```

### Passo 2: Obter Variante para Exibir

Quando um visitante acessa sua landing page, você deve chamar este endpoint para obter qual variante deve ser exibida.

**Opção 1: Usando GET (query parameters)**
```bash
curl "http://localhost:8000/experiment?testId=landing_001&visitorId=usuario123"
```

**Opção 2: Usando POST (JSON no body)**
```bash
curl -X POST "http://localhost:8000/experiment" \
  -H "Content-Type: application/json" \
  -d '{
    "testId": "landing_001",
    "visitorId": "usuario123"
  }'
```

**Resposta:**
```json
{
  "variantId": "B",
  "sections": [
    { "id": "hero_b", "contentUrl": "https://cdn.exemplo.com/hero_b.html" },
    { "id": "features_b", "contentUrl": "https://cdn.exemplo.com/features_b.html" },
    { "id": "cta_b", "contentUrl": "https://cdn.exemplo.com/cta_b.html" }
  ]
}
```

**Como funciona:**
- O backend seleciona uma variante baseada na distribuição configurada usando hash determinístico
- **O mesmo visitante sempre verá a mesma variante** (garantindo consistência no teste A/B)
- Com distribuição 50/50, aproximadamente 50% dos visitantes verão A e 50% verão B
- A seleção é baseada em hash do `testId + visitorId`, garantindo consistência entre requisições
- Uma impressão é automaticamente registrada para a variante retornada
- Use o `visitorId` para identificar visitantes únicos (recomendado: UUID salvo no localStorage)

**Exemplo de uso no JavaScript:**
```javascript
// Gerar ou recuperar visitorId (salvar no localStorage)
let visitorId = localStorage.getItem('visitorId');
if (!visitorId) {
  visitorId = crypto.randomUUID();
  localStorage.setItem('visitorId', visitorId);
}

// Obter variante
const response = await fetch('http://localhost:8000/experiment', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    testId: 'landing_001',
    visitorId: visitorId
  })
});

const data = await response.json();
// data.variantId = "A" ou "B"
// data.sections = array de seções para montar a landing page
```

### Passo 3: Registrar Conversão

Quando um visitante realiza uma ação desejada (ex: preenche formulário, clica em botão), registre a conversão.

```bash
curl -X POST "http://localhost:8000/conversion" \
  -H "Content-Type: application/json" \
  -d '{
    "testId": "landing_001",
    "variantId": "B",
    "visitorId": "usuario123",
    "event": "lead"
  }'
```

**Resposta:**
```json
{
  "ok": true
}
```

**Parâmetros:**
- `testId`: ID do experimento
- `variantId`: ID da variante que o visitante viu (obtido no Passo 2)
- `visitorId`: ID do visitante (mesmo usado no Passo 2)
- `event`: Tipo de evento/conversão (ex: "lead", "purchase", "signup")

**Validação:**
- O sistema valida se o visitante realmente viu a variante antes de registrar a conversão
- Se o visitante não tiver visto a variante, retornará erro 400

**Exemplo de uso no JavaScript:**
```javascript
// Quando o usuário converte (ex: clica em "Enviar")
await fetch('http://localhost:8000/conversion', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    testId: 'landing_001',
    variantId: data.variantId, // Variante obtida no Passo 2
    visitorId: visitorId,
    event: 'lead'
  })
});
```

### Passo 4: Visualizar Métricas

Para ver o desempenho de cada variante, consulte as métricas do experimento.

```bash
curl "http://localhost:8000/admin/test/landing_001/metrics"
```

**Resposta:**
```json
{
  "testId": "landing_001",
  "variants": [
    {
      "variantId": "A",
      "impressions": 240,
      "conversions": 31,
      "conversionRate": 0.129
    },
    {
      "variantId": "B",
      "impressions": 210,
      "conversions": 44,
      "conversionRate": 0.209
    }
  ]
}
```

**Métricas retornadas:**
- `impressions`: Número de vezes que a variante foi exibida
- `conversions`: Número de conversões registradas
- `conversionRate`: Taxa de conversão (conversions / impressions)

## 🌐 Endpoints Detalhados

### 1. POST /admin/test

Cria ou atualiza um experimento.

**Request Body:**
```json
{
  "testId": "landing_001",
  "name": "Nome do Teste",
  "variants": [
    {
      "variantId": "A",
      "distribution": 50,
      "sections": [
        {
          "id": "hero_a",
          "contentUrl": "https://cdn.exemplo.com/hero_a.html"
        }
      ]
    }
  ]
}
```

**Validações:**
- A soma de todas as `distribution` deve ser exatamente 100
- Cada variante deve ter pelo menos uma seção
- `testId` deve ser único

### 2. GET /experiment ou POST /experiment

Retorna a variante a ser exibida e registra uma impressão.

**GET - Query Parameters:**
- `testId`: ID do experimento
- `visitorId`: ID do visitante

**POST - Request Body:**
```json
{
  "testId": "landing_001",
  "visitorId": "usuario123"
}
```

**Response:**
```json
{
  "variantId": "A",
  "sections": [
    {
      "id": "hero_a",
      "contentUrl": "https://cdn.exemplo.com/hero_a.html"
    }
  ]
}
```

**Comportamento:**
- Seleção **determinística** baseada em hash do `testId + visitorId`
- O mesmo visitante sempre verá a mesma variante (consistência garantida)
- Registra automaticamente uma impressão
- Respeita as porcentagens de distribuição no agregado

### 3. POST /conversion

Registra uma conversão por visitante.

**Request Body:**
```json
{
  "testId": "landing_001",
  "variantId": "A",
  "visitorId": "usuario123",
  "event": "lead"
}
```

**Response:**
```json
{
  "ok": true
}
```

### 4. GET /admin/test/{testId}/metrics

Retorna as métricas de cada variante do teste.

**Response:**
```json
{
  "testId": "landing_001",
  "variants": [
    {
      "variantId": "A",
      "impressions": 100,
      "conversions": 10,
      "conversionRate": 0.1
    }
  ]
}
```

### 5. GET /admin/tests

Lista todos os testes cadastrados.

**Response:**
```json
{
  "tests": [
    {
      "testId": "landing_001",
      "name": "Teste de Landing Page",
      "status": "active",
      "variantCount": 2
    }
  ]
}
```

## 🔁 Fluxo Completo de Uso

1. **Admin cria teste** → `POST /admin/test`
   - Define variantes e distribuições (ex: 50/50)

2. **Visitante acessa site** → `GET/POST /experiment`
   - Frontend obtém qual variante exibir
   - Backend seleciona aleatoriamente baseado na distribuição
   - Backend registra impressão automaticamente

3. **Visitante converte** → `POST /conversion`
   - Frontend registra quando usuário realiza ação desejada
   - Backend armazena a conversão

4. **Admin consulta métricas** → `GET /admin/test/{testId}/metrics`
   - Visualiza impressões, conversões e taxa de conversão por variante
   - Compara desempenho das variantes

5. **Admin lista testes** → `GET /admin/tests`
   - Visualiza todos os testes cadastrados com seus status

6. **Admin atualiza teste** → `POST /admin/test`
   - Pode alterar distribuições ou adicionar novas variantes

## 🎲 Como Funciona a Distribuição

O sistema usa **hash determinístico** para distribuir as variantes, garantindo consistência:

- **Distribuição 50/50**: Aproximadamente 50% dos visitantes verão A e 50% verão B
- **Distribuição 30/40/30**: Aproximadamente 30% verão A, 40% verão B e 30% verão C
- **Consistência garantida**: O mesmo visitante sempre verá a mesma variante (baseado em hash do `testId + visitorId`)

**Exemplo prático:**
- Se 100 visitantes únicos acessarem com distribuição 50/50
- Espera-se aproximadamente 50 verem variante A e 50 verem variante B
- O mesmo visitante sempre verá a mesma variante, mesmo em requisições diferentes
- Isso garante que o teste A/B seja válido e consistente

## 🗄️ Armazenamento

O projeto usa **armazenamento em memória** para MVP. Todos os dados são mantidos em estruturas Python (dicionários e listas) durante a execução do servidor.

**⚠️ Importante:** Os dados são perdidos quando o servidor é reiniciado. Para produção, recomenda-se migrar para um banco de dados persistente (PostgreSQL, MongoDB, etc.).

### Estrutura de Dados

- **tests**: Dicionário que armazena os experimentos (testId, name, variants, status)
- **impressions**: Lista que registra todas as impressões (testId, variantId, visitorId, timestamp)
- **conversions**: Lista que registra todas as conversões (testId, variantId, visitorId, event, timestamp)

## 📝 Documentação Interativa

Acesse `http://localhost:8000/docs` para ver a documentação interativa da API (Swagger UI). Você pode testar todos os endpoints diretamente pela interface web.

Alternativamente, acesse `http://localhost:8000/redoc` para a documentação em formato ReDoc.

## 🔧 Considerações Técnicas

- **Arquitetura**: Projeto organizado em camadas (API, Services, Repositories, Schemas)
- **Distribuição**: Implementada usando hash determinístico (MD5) do `testId + visitorId`, garantindo que o mesmo visitante sempre veja a mesma variante
- **visitorId**: Deve ser um identificador único do visitante (recomenda-se usar UUID salvo no localStorage do frontend)
- **Seleção de Variante**: Baseada em hash determinístico, garantindo consistência no teste A/B
- **Validação de Conversão**: O sistema valida se o visitante realmente viu a variante antes de registrar a conversão
- **Tratamento de Exceções**: Exceções customizadas com handlers globais para respostas HTTP consistentes
- **Configuração**: Configurações centralizadas em `core/config.py`
- **Autenticação**: Não implementada no MVP (pode ser adicionada depois)
- **CORS**: Configurado para aceitar requisições de qualquer origem (ajuste para produção)

## 📦 Estrutura do Projeto

```
test-A-b/
├── main.py              # Aplicação FastAPI principal
├── api/                 # Camada de API
│   ├── routes/          # Rotas da API (admin, experiment, conversion)
│   └── dependencies.py  # Dependências compartilhadas
├── core/                # Configurações e exceções
│   ├── config.py        # Configurações centralizadas
│   └── exceptions.py    # Exceções customizadas
├── services/            # Lógica de negócio
│   ├── test_service.py      # Serviço de gerenciamento de testes
│   ├── metrics_service.py   # Serviço de métricas
│   └── variant_selector.py   # Seleção de variantes
├── repositories/        # Camada de acesso a dados
│   └── test_repository.py
├── schemas/             # Modelos Pydantic
│   └── models.py
├── storage.py           # Armazenamento em memória
├── pyproject.toml       # Configuração do projeto (PDM)
├── requirements.txt     # Dependências (pip)
└── README.md            # Esta documentação
```

## 🚨 Troubleshooting

### Erro: "Total distribution must equal 100"
- Verifique se a soma de todas as `distribution` nas variantes é exatamente 100
- Exemplo: 50 + 50 = 100 ✅ | 30 + 40 + 30 = 100 ✅

### Erro: "Test not found or inactive"
- Verifique se o `testId` está correto
- Verifique se o teste está com status "active"

### Variantes sempre retornam a mesma para o mesmo visitante
- Isso é esperado e correto! O sistema garante que o mesmo visitante sempre veja a mesma variante
- Para testar diferentes variantes, use `visitorId` diferentes
- A distribuição funciona no agregado: com muitos visitantes únicos, você verá a distribuição configurada

### Erro: "Visitor did not see variant"
- O sistema valida se o visitante realmente viu a variante antes de registrar conversão
- Certifique-se de chamar `/experiment` antes de registrar a conversão
- Use o mesmo `visitorId` em ambas as chamadas
- Verifique se o `variantId` na conversão corresponde ao retornado pelo `/experiment`

### Como testar diferentes variantes
- Use `visitorId` diferentes para ver diferentes variantes
- A distribuição funciona no agregado: com muitos visitantes únicos, você verá a distribuição configurada
- Para testes manuais, gere diferentes UUIDs: `crypto.randomUUID()` no JavaScript ou `uuid.uuid4()` no Python

## 🧪 Testando a API

### Usando curl

Todos os exemplos neste README usam `curl`, mas você pode usar qualquer cliente HTTP:
- **Postman** ou **Insomnia** (interfaces gráficas)
- **httpie** (alternativa moderna ao curl)
- **Swagger UI** em `http://localhost:8000/docs` (teste direto no navegador)
- **Python requests** ou **JavaScript fetch** (programaticamente)

### Exemplo com httpie

```bash
# Instalar httpie: pip install httpie

# Criar teste
http POST http://localhost:8000/admin/test \
  testId=teste_simples \
  name="Teste 50/50" \
  variants:='[{"variantId":"A","distribution":50,"sections":[{"id":"hero","contentUrl":"https://exemplo.com/a.html"}]},{"variantId":"B","distribution":50,"sections":[{"id":"hero","contentUrl":"https://exemplo.com/b.html"}]}]'
```

## 📚 Exemplos Completos

### Exemplo 1: Teste Simples 50/50

```bash
# 1. Criar teste
curl -X POST "http://localhost:8000/admin/test" \
  -H "Content-Type: application/json" \
  -d '{
    "testId": "teste_simples",
    "name": "Teste 50/50",
    "variants": [
      {
        "variantId": "A",
        "distribution": 50,
        "sections": [
          { "id": "hero", "contentUrl": "https://exemplo.com/a.html" }
        ]
      },
      {
        "variantId": "B",
        "distribution": 50,
        "sections": [
          { "id": "hero", "contentUrl": "https://exemplo.com/b.html" }
        ]
      }
    ]
  }'

# 2. Obter variante (o mesmo visitorId sempre verá a mesma variante)
curl "http://localhost:8000/experiment?testId=teste_simples&visitorId=user1"

# 3. Registrar conversão
curl -X POST "http://localhost:8000/conversion" \
  -H "Content-Type: application/json" \
  -d '{
    "testId": "teste_simples",
    "variantId": "A",
    "visitorId": "user1",
    "event": "click"
  }'

# 4. Ver métricas
curl "http://localhost:8000/admin/test/teste_simples/metrics"

# 5. Listar todos os testes
curl "http://localhost:8000/admin/tests"
```

## 🔐 Segurança e Produção

### Recomendações para Produção

- **Autenticação**: Implementar autenticação para endpoints administrativos (`/admin/*`)
- **CORS**: Restringir `CORS_ORIGINS` em `core/config.py` para domínios específicos
- **Banco de Dados**: Migrar de armazenamento em memória para banco de dados persistente
- **Rate Limiting**: Implementar rate limiting para prevenir abuso
- **HTTPS**: Usar HTTPS em produção
- **Logging**: Adicionar logging estruturado para monitoramento
- **Validação**: Validar e sanitizar todas as entradas do usuário
- **Variáveis de Ambiente**: Mover configurações sensíveis para variáveis de ambiente

### Configuração de CORS

Para restringir CORS em produção, edite `core/config.py`:

```python
CORS_ORIGINS: List[str] = [
    "https://seusite.com",
    "https://www.seusite.com"
]
```

## 🛠️ Desenvolvimento

### Executar em modo desenvolvimento

```bash
# Com PDM
pdm run uvicorn main:app --reload

# Com pip
uvicorn main:app --reload
```

O flag `--reload` permite que o servidor reinicie automaticamente quando você fizer alterações no código.

### Estrutura de Código

O projeto segue uma arquitetura em camadas:

- **API Layer** (`api/`): Rotas e endpoints HTTP
- **Service Layer** (`services/`): Lógica de negócio
- **Repository Layer** (`repositories/`): Acesso a dados
- **Schema Layer** (`schemas/`): Modelos de dados e validação
- **Core** (`core/`): Configurações e exceções compartilhadas

### Adicionar Novos Endpoints

1. Defina os schemas em `schemas/models.py`
2. Crie a lógica de negócio em `services/`
3. Adicione as rotas em `api/routes/`
4. Registre a rota em `main.py`


