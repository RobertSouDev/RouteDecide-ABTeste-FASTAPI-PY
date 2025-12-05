/**
 * SDK de A/B Testing - Tracking de Conversões
 * 
 * Este SDK intercepta cliques em botões e envia métricas de conversão
 * para o backend de testes A/B.
 */
(function() {
  'use strict';

  // Encontrar a tag script atual para ler os atributos data-*
  var currentScript = document.currentScript || 
    (function() {
      var scripts = document.getElementsByTagName('script');
      return scripts[scripts.length - 1];
    })();

  // Ler parâmetros dos atributos data-*
  var testId = currentScript.getAttribute('data-test-id');
  var apiUrl = currentScript.getAttribute('data-api-url') || 'http://localhost:8000';

  // Validar parâmetros obrigatórios
  if (!testId) {
    console.error('[AB Test SDK] testId é obrigatório via atributo data-test-id');
    return;
  }

  // Estado interno do SDK
  var variantId = null;
  var sections = [];
  var isInitialized = false;
  var experimentCallInProgress = false;

  // Expor API pública em window.testeab
  window.testeab = {
    sections: sections,
    variantId: null,
    isInitialized: false
  };

  /**
   * Chama o endpoint /experiment para obter a variante do visitante
   */
  async function getExperiment() {
    if (experimentCallInProgress) {
      return;
    }

    experimentCallInProgress = true;

    try {
      const response = await fetch(`${apiUrl}/experiment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          testId: testId
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      variantId = data.variantId;
      sections = data.sections || [];
      isInitialized = true;
      
      // Atualizar window.testeab com os dados obtidos
      window.testeab.variantId = variantId;
      window.testeab.sections = sections;
      window.testeab.isInitialized = true;
      
      console.log('[AB Test SDK] Variante obtida:', variantId);
      console.log('[AB Test SDK] Seções obtidas:', sections);
    } catch (error) {
      console.error('[AB Test SDK] Erro ao obter variante:', error);
      // Não quebra a página, apenas loga o erro
    } finally {
      experimentCallInProgress = false;
    }
  }

  /**
   * Envia métrica de conversão para o backend
   */
  async function sendConversion(buttonText) {
    if (!isInitialized || !variantId) {
      console.warn('[AB Test SDK] SDK ainda não inicializado ou variantId não disponível');
      return;
    }

    const event = `click-${buttonText}`;

    try {
      const response = await fetch(`${apiUrl}/conversion`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          testId: testId,
          variantId: variantId,
          event: event
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      console.log('[AB Test SDK] Conversão registrada:', event);
    } catch (error) {
      console.error('[AB Test SDK] Erro ao registrar conversão:', error);
      // Não quebra a página, apenas loga o erro
    }
  }

  /**
   * Obtém o texto de um botão
   * Tenta várias formas de obter o texto: textContent, innerText, value, aria-label
   */
  function getButtonText(button) {
    // Prioridade: aria-label > textContent > innerText > value > placeholder
    if (button.getAttribute('aria-label')) {
      return button.getAttribute('aria-label').trim();
    }
    
    var text = button.textContent || button.innerText || '';
    if (text.trim()) {
      return text.trim();
    }
    
    if (button.value) {
      return button.value.trim();
    }
    
    if (button.placeholder) {
      return button.placeholder.trim();
    }
    
    // Fallback: usar tipo ou tag
    return button.type || button.tagName || 'button';
  }

  /**
   * Handler de clique em botões
   */
  function handleButtonClick(event) {
    var target = event.target;
    
    // Verificar se é um botão ou está dentro de um botão
    var button = target;
    while (button && button !== document.body) {
      if (button.tagName === 'BUTTON' || 
          (button.tagName === 'INPUT' && button.type === 'button') ||
          (button.tagName === 'INPUT' && button.type === 'submit') ||
          (button.tagName === 'A' && button.onclick) ||
          button.getAttribute('role') === 'button') {
        var buttonText = getButtonText(button);
        sendConversion(buttonText);
        break;
      }
      button = button.parentElement;
    }
  }

  /**
   * Inicializa o SDK
   */
  function init() {
    // Chamar /experiment para obter a variante
    getExperiment();

    // Adicionar event listener usando event delegation no document
    // Isso captura todos os botões, incluindo os adicionados dinamicamente
    document.addEventListener('click', handleButtonClick, true);

    console.log('[AB Test SDK] SDK inicializado');
  }

  // Aguardar o DOM estar pronto antes de inicializar
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    // DOM já está pronto
    init();
  }
})();

