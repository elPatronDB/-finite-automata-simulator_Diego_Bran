from typing import Dict, Tuple
from .validator import AutomatonConfig
import graphviz
from datetime import datetime
import os

class Automaton:
    def __init__(self, config: AutomatonConfig):
        self.config = config
        self.transition_map: Dict[Tuple[str, str], str] = {}
                
        for trans in config.transitions:
            key = (trans.from_state, trans.symbol)
            self.transition_map[key] = trans.to_state


    def _process_recursive(self, state: str, string: str, index: int) -> bool:
        if index == len(string):
            return state in self.config.acceptance_states

        symbol = string[index]


        if symbol not in self.config.alphabet:
            return False

        next_state = self.transition_map.get((state, symbol))


        if next_state is None:
            return False

        return self._process_recursive(next_state, string, index + 1)



    def validate_string(self, string: str) -> bool:
        return self._process_recursive(self.config.initial_state, string, 0)



    def generate_diagram(self) -> str:
        dot = graphviz.Digraph(format='png')
        dot.attr(rankdir='LR')
        dot.node('', shape='none')
        dot.edge('', self.config.initial_state, arrowhead='normal')


        for state in self.config.states:
            shape = 'doublecircle' if state in self.config.acceptance_states else 'circle'
            dot.node(state, shape=shape)


        for trans in self.config.transitions:
            dot.edge(trans.from_state, trans.to_state, label=trans.symbol)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"automata_{self.config.id}_{timestamp}.png"
        os.makedirs('generated_diagrams', exist_ok=True)
        filepath = os.path.join('generated_diagrams', filename)
        dot.render(filepath, cleanup=True)

        return filepath