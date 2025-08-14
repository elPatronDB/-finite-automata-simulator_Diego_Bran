from pydantic import BaseModel, ValidationError
from typing import List, Set


class AutomatonError(Exception):
    pass

class Transition(BaseModel):
    from_state: str
    to_state: str
    symbol: str

class AutomatonConfig(BaseModel):
    id: str
    name: str
    initial_state: str
    acceptance_states: set[str]
    alphabet: set[str]
    states: set[str]
    transitions: list[Transition]
    test_strings: list[str]

class AutomatonValidator:
    def __init__(self, config: dict):
        try:
            self.config = AutomatonConfig(**config)
        except ValidationError as e:
            raise AutomatonError(f"Oh no! There is a problem: {e}")
    
    def validate(self):
        # Validación de la configuración del autómata
        if not self.config.initial_state:
            raise AutomatonError("Missing initial state in Automaton JSON")
        
        if self.config.initial_state not in self.config.states:
            raise AutomatonError("Oh no! The initial state is not in states")
        
        # Validación de los estados de aceptación
        if not all(state in self.config.states for state in self.config.acceptance_states):
            raise AutomatonError("Oh no! Acceptance states should be in states")

        if not self.config.alphabet:
            raise AutomatonError("The alphabet is empty")
        
        if not self.config.states:
            raise AutomatonError("The states are empty")
        
        
        #Ciclo para validar las transiciones
        for transition in self.config.transitions:
            if transition.from_state not in self.config.states:
                raise AutomatonError(f"Transition is not in states")
            
            if transition.to_state not in self.config.states:
                raise AutomatonError(f"Transition state is not in states")
            
            if transition.symbol not in self.config.alphabet:
                raise AutomatonError(f"Transition symbol not in alphabet")

            
        # Ciclo para validad transiciones completas - Asegura que cada estado debe tener una transición
        for state in self.config.states:
            for symbol in self.config.alphabet:
                if not any(t.from_state == state and t.symbol == symbol for t in self.config.transitions):
                    raise AutomatonError(f"A Transition is missing for state and symbol")
        

            
            