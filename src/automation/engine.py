from typing import Dict, Any, Optional
from .manager import FlowManager
from .state import InMemoryStateManager
from .contracts import EngineInput, EngineOutput, ConversationState

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
        default_flow: str 
    ):
        self.flow_manager = flow_manager
        self.state_manager = state_manager
        self.default_flow = default_flow
        
    
    def start_flow_for_user(self, user_id: str, flow_id: str):
        flow = self.flow_manager.get_flow(flow_id)
        if not flow:
            raise ValueError("Flow not found")
        
        first_step = flow.get("steps", [])[0]
        
        state = ConversationState(
            user_id=user_id,
            flow=flow_id,
            step=first_step["id"],
            meta={}
        )
        
        self.state_manager.set(state)
        return self._render_step(flow, first_step)
    
    
    def handle_message(self, user_id: str, text: str):
        # 1) get state
        state = self.state_manager.get(user_id)
        if not state:
            return self.start_flow_for_user(user_id, self.default_flow)
        
        
        # 2) get flow
        flow = self.flow_manager.get_flow(state.flow)
        if not flow:
            raise ValueError("No flow assigned to user and no default_flow set")


        # 3) get step
        step = self._find_step(flow, state.step)
        if not step:
        # restart
            return self.start_flow_for_user(user_id, state.flow)


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
            new_state = state.next_step(next_step["id"])
            self.state_manager.set(new_state)
            
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
    
    
    def handle(self, input: EngineInput) -> EngineOutput:
        # Ponto único de entrada da engine, recebe um engine input e retorna un engine output
        
        # 1° Executa lógica existente
        result = self.handle_message(
            user_id=input.user_id,
            text=input.text
        )

        state = self.state_manager.get(input.user_id)
        
        # 4° retorna resposta formalizada
        return EngineOutput(
            reply=result.get("reply", ""),
            state=state,
            end_conversation=result.get("end", False)
        )