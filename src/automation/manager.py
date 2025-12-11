from typing import Dict, Any
import yaml
from pathlib import Path


class FlowManager:
    """Carrega e fornece acesso aos fluxos definidos em YAML.

    Simples: carrega todos YAMLs de um diretório `flows/` e mantém em memória.
    """


    def __init__(self, flows_path: str | Path):
        self.flows_path = Path(flows_path)
        self._flows: Dict[str, Dict[str, Any]] = {}
        self.load_all()


    def load_all(self) -> None:
        """Carrega todos os arquivos YAML do diretório flows."""
        self._flows = {}
        if not self.flows_path.exists():
            return
        for p in self.flows_path.glob("*.yaml"):
            with p.open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
                flow_id = data.get("id") or p.stem
                self._flows[flow_id] = data


    def get_flow(self, flow_id: str) -> Dict[str, Any] | None:
        return self._flows.get(flow_id)


    def list_flows(self) -> list:
        return list(self._flows.keys())