# Pacote de automação (FlowEngine) — versão 1
from .engine import FlowEngine
from .manager import FlowManager
from .state import InMemoryStateManager
from .triggers import keyword_trigger


__all__ = ["FlowEngine", "FlowManager", "InMemoryStateManager", "keyword_trigger"]