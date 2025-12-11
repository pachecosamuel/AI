from typing import Dict, Any, Optional
from .manager import FlowManager
from .state import InMemoryStateManager

class FlowEngine:
    """Engine simples de execução de fluxos baseado em steps definidos em YAML.


    - mantém estado por usuário via state_manager
    - avança passos conforme 'next' no YAML
    - suporta escolha por mapping simples
    """
    
    def __init__(
        self,
        flow_manager: FlowManager,
        state_manager: InMemoryStateManager,
        default_flow: str | None = None
    ):
        self.flow_manager = flow_manager
        self.state_manager = state_manager
        self.default_flow = default_flow
        
    
    def start_flow_for_user(self, user_id: str, flow_id: str) -> Dict[str, Any]:
        flow = self.flow_manager.get_flow(flow_id)
        if not flow:
            raise ValueError("Flow not found")
        
        # start at first step
        first_step = flow.get("steps", [])[0]
        state = {"flow_id": flow_id, "step_id": first_step["id"], "meta": {}}
        self.state_manager.set(user_id, state)
        return self._render_step(flow, first_step)
    
    
    def handle_message(self, user_id: str, text: str) -> Dict[str, Any]:
        # 1) get state
        state = self.state_manager.get(user_id)
        flow_id = state.get("flow_id") or self.default_flow
        if not flow_id:
            raise ValueError("No flow assigned to user and no default_flow set")


        flow = self.flow_manager.get_flow(flow_id)
        if not flow:
            raise ValueError("Flow not found")


        step = self._find_step(flow, state.get("step_id"))
        if not step:
        # restart
            return self.start_flow_for_user(user_id, flow_id)


        # if current step expects a choice mapping
        next_cfg = step.get("next")
        if next_cfg and next_cfg.get("type") == "choice":
            
            mapping = next_cfg.get("mapping", {})
            choice = text.strip()
            next_step_id = mapping.get(choice)
            
            if not next_step_id:
                # keep same step or respond invalid
                return {"reply": "Opção inválida. Tente novamente.", "end": False}
            
            next_step = self._find_step(flow, next_step_id)
            if next_step is None:
                return {"reply": "Erro interno no fluxo.", "end": True}
            
            # update state
            self.state_manager.update(user_id, flow_id=flow_id, step_id=next_step["id"])
            return self._render_step(flow, next_step)


        # default: if step has next type end -> restart
        if next_cfg and next_cfg.get("type") == "end":
            # clear state
            self.state_manager.clear(user_id)
            return {"reply": "Fluxo finalizado.", "end": True}
        
        # fallback: reply with current message
        return {"reply": step.get("message"), "end": False}
    
    def _render_step(self, flow: Dict[str, Any], step: Dict[str, Any]) -> Dict[str, Any]:
        return {"reply": step.get("message"), "end": (step.get("next", {}).get("type") == "end")}
    
    def _find_step(self, flow: Dict[str, Any], step_id: Optional[str]) -> Optional[Dict[str, Any]]:
        for s in flow.get("steps", []):
            if s.get("id") == step_id:
                return s
    
        return None