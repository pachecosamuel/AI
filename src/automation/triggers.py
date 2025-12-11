from typing import Callable, Dict, Any


# Trigger simples por palavra-chave — função utilitária


def keyword_trigger(message: str, keywords: Dict[str, str]) -> str | None:
    """Retorna o key correspondente se alguma keyword bater no texto.


    keywords: {'ola': 'welcome_flow', 'ajuda': 'support_flow'}
    """
    text = (message or "").lower()
    for k, flow_id in keywords.items():
        if k.lower() in text:
            return flow_id
        return None