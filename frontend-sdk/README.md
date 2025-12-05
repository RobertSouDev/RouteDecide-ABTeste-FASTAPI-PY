# SDK Frontend - A/B Testing

SDK JavaScript para rastreamento automático de conversões em testes A/B.

## 📋 Funcionalidades

- **Inicialização automática**: Obtém a variante do teste A/B automaticamente ao carregar a página
- **Tracking de cliques**: Intercepta automaticamente cliques em todos os botões da página
- **Envio de métricas**: Envia métricas de conversão para o backend automaticamente
- **Suporte a conteúdo dinâmico**: Funciona com botões adicionados dinamicamente via JavaScript

## 🚀 Instalação

Inclua o SDK no `<head>` da sua página HTML usando uma tag `<script>` com os atributos necessários:

```html
<head>
  <script 
    src="/caminho/para/ab-test-sdk.js"
    data-test-id="landing_001"
    data-api-url="http://localhost:8000">
  </script>
</head>
```

## 📝 Parâmetros

### Obrigatórios

- **`data-test-id`**: ID do teste A/B (ex: `"landing_001"`)

### Opcionais

- **`data-api-url`**: URL base da API (padrão: `"http://localhost:8000"`)

## 🔄 Como Funciona

1. **Inicialização**: Ao carregar a página, o SDK:
   - Lê os parâmetros dos atributos `data-*` da tag script
   - Chama automaticamente `POST /experiment` para obter a variante
   - Armazena o `variantId` em memória

2. **Tracking de Cliques**: O SDK:
   - Adiciona um event listener global usando event delegation
   - Intercepta cliques em todos os botões da página (incluindo botões adicionados dinamicamente)
   - Identifica botões por tag (`<button>`, `<input type="button">`, `<input type="submit">`) ou atributo `role="button"`

3. **Envio de Métricas**: Ao clicar em um botão, o SDK:
   - Extrai o texto do botão (prioridade: `aria-label` > `textContent` > `value` > `placeholder`)
   - Envia `POST /conversion` com:
     - `testId`: ID do teste passado em `data-test-id`
     - `variantId`: Variante obtida do endpoint `/experiment`
     - `event`: `"click-${texto do botão}"`

## 📊 Formato das Requisições

### POST /experiment

O SDK chama automaticamente este endpoint na inicialização:

```json
{
  "testId": "landing_001"
}
```

**Resposta esperada:**
```json
{
  "variantId": "variant_a",
  "sections": [...]
}
```

### POST /conversion

O SDK envia automaticamente este endpoint ao clicar em botões:

```json
{
  "testId": "landing_001",
  "variantId": "variant_a",
  "event": "click-Enviar"
}
```

## 🎯 Exemplo Completo

```html
<!DOCTYPE html>
<html>
<head>
  <title>Minha Landing Page</title>
  
  <!-- SDK de A/B Testing -->
  <script 
    src="https://meusite.com/sdk/ab-test-sdk.js"
    data-test-id="landing_001"
    data-api-url="https://api.meusite.com">
  </script>
</head>
<body>
  <h1>Bem-vindo!</h1>
  
  <!-- Qualquer botão será automaticamente rastreado -->
  <button>Clique Aqui</button>
  <input type="button" value="Enviar Formulário" />
  <button aria-label="Fazer Login">Login</button>
  
  <!-- Botões adicionados dinamicamente também serão rastreados -->
  <script>
    setTimeout(function() {
      var btn = document.createElement('button');
      btn.textContent = 'Botão Dinâmico';
      document.body.appendChild(btn);
    }, 1000);
  </script>
</body>
</html>
```

## 🔍 Detalhes Técnicos

### Identificação de Botões

O SDK identifica botões através de:
- Tags: `<button>`, `<input type="button">`, `<input type="submit">`
- Atributo `role="button"` em qualquer elemento
- Elementos `<a>` com handler `onclick`

### Extração de Texto do Botão

A ordem de prioridade para obter o texto do botão é:
1. `aria-label` (atributo)
2. `textContent` ou `innerText`
3. `value` (para inputs)
4. `placeholder` (para inputs)
5. Fallback: tipo ou tag do elemento

### Event Delegation

O SDK usa event delegation no `document`, capturando eventos na fase de captura (`true` como terceiro parâmetro). Isso garante que:
- Todos os botões sejam capturados, mesmo os adicionados dinamicamente
- Não seja necessário adicionar listeners individuais em cada botão
- O desempenho seja otimizado

### Tratamento de Erros

O SDK trata erros de forma silenciosa:
- Erros de rede são logados no console, mas não quebram a página
- Se o SDK não estiver inicializado, apenas loga um aviso
- Validação de parâmetros obrigatórios no início

## 🐛 Debug

O SDK loga informações úteis no console do navegador:
- `[AB Test SDK] SDK inicializado` - Quando o SDK é carregado
- `[AB Test SDK] Variante obtida: variant_a` - Quando a variante é recebida
- `[AB Test SDK] Conversão registrada: click-Enviar` - Quando uma conversão é enviada
- `[AB Test SDK] Erro ao obter variante: ...` - Em caso de erro na chamada do experiment
- `[AB Test SDK] Erro ao registrar conversão: ...` - Em caso de erro no envio de conversão

## ⚠️ Requisitos

- Navegadores modernos com suporte a:
  - `fetch()` API
  - `async/await`
  - `document.currentScript` ou fallback para última tag script
  - Event delegation

## 📦 Compatibilidade

- Chrome/Edge: ✅
- Firefox: ✅
- Safari: ✅
- IE11: ❌ (requer polyfills para fetch e async/await)

