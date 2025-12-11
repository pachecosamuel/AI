from typing import Dict, Any


class InMemoryStateManager:
    #Gerenciador de estado em memória (dev)


    def __init__(self):
        # map: user_id -> state dict
        self._store: Dict[str, Dict[str, Any]] = {}


    def get(self, user_id: str) -> Dict[str, Any]:
        return self._store.get(user_id, {"flow_id": None, "step_id": None, "meta": {}})


    def set(self, user_id: str, state: Dict[str, Any]) -> None:
        self._store[user_id] = state


    def update(self, user_id: str, **kwargs) -> None:
        st = self.get(user_id)
        st.update(kwargs)
        self._store[user_id] = st


    def clear(self, user_id: str) -> None:
        if user_id in self._store:
            del self._store[user_id]