from typing import Dict, Any, Optional
from .contracts import ConversationState


class InMemoryStateManager:
    #Gerenciador de estado em memória (dev)


    def __init__(self):
        # map: user_id -> state dict
        self._states: Dict[str, ConversationState] = {}


    def get(self, user_id: str) -> Optional[ConversationState]:
        return self._states.get(user_id)


    def set(self, state: ConversationState):
        self._states[state.user_id] = state


    def update(self, user_id: str, **kwargs) -> None:
        state = self._states.get(user_id)
        if not state:
            return

        for key, value in kwargs.items():
            setattr(state, key, value)

    def clear(self, user_id: str):
        self._states.pop(user_id, None)