from src.validator import AutomatonConfig
import json

with open("examples/test.json", "r") as f:
    config = json.load(f)[0]
try:
    automaton = AutomatonConfig(**config)
    print(f"Autómata válidado: {automaton.id}")
except Exception as e:
    print(f"Error de validación: {e}")