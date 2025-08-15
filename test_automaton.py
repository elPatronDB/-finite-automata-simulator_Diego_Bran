from src.validator import AutomatonValidator
from src.automaton import Automaton

config_data = {
    "id": "automata_1",
    "name": "Reconocedor de números pares",
    "initial_state": "q0",
    "acceptance_states": {"q0"},
    "alphabet": {"0", "1"},
    "states": {"q0", "q1"},
    "transitions": [
        {"from_state": "q0", "symbol": "0", "to_state": "q0"},
        {"from_state": "q0", "symbol": "1", "to_state": "q1"},
        {"from_state": "q1", "symbol": "0", "to_state": "q0"},
        {"from_state": "q1", "symbol": "1", "to_state": "q1"}
    ],
    "test_strings": ["0", "10", "101", "1010", ""]
}

validator = AutomatonValidator(config_data)
validator.validate()
automaton = Automaton(validator.config)
for s in validator.config.test_strings:
    print(f"String {s}: {automaton.validate_string(s)}")
print(f"Diagram: {automaton.generate_diagram()}")