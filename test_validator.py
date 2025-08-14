from src.validator import AutomatonConfig
import json

with open("examples/test.json", "r") as f:
    config = json.load(f)[0]
try:
    automaton = AutomatonConfig(**config)
    print(f"Automaton validated: {automaton.id}")
except Exception as e:
    print(f"Validation error: {e}")