from automation.manager import FlowManager
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
FLOWS_DIR = BASE_DIR / "automation" / "flows"

fm = FlowManager(str(FLOWS_DIR))

print("Flows carregados:")
print(fm.list_flows())
