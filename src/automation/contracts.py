from dataclasses import dataclass, Field
from typing import Optional, Dict, Any

@dataclass
class EngineInput:
    user_id: str
    text: str
    step: str
    metadata: Optional[Dict] = None
    
    def advance(self, step_id: str):
        self.step = step_id
        
    def with_flow(self, flow_id: str):
        self.flow = flow_id
    
@dataclass
class ConversationState:
    user_id: str
    flow: str
    step: str
    meta: Dict 
    
    def next_step(self, step_id: str):
        return ConversationState(
            user_id=self.user_id,
            flow=self.flow,
            step=step_id,
            meta=self.meta or {}
        )
    
    
    
@dataclass
class EngineOutput:
    reply: str
    state: Optional[ConversationState]
    end_conversation: bool = False
    
