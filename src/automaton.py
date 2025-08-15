from typing import Dict, Tuple
from validator import AutomatonConfig

import graphviz

from datetime import datetime
import os


class Automaton:
    def __init__(self, config: AutomatonConfig):
        self.config = config
        self.current_state = config.initial_state
        self.transitionDict: Dict[Tuple[str, str], str] = {}


        #Dictionary creation for movements
        for transition in config.transitions:
            key = (transition.from_state, transition.symbol)
            if key in self.transitionDict:
                raise ValueError(f"Non-deterministic transition detected for state '{transition.from_state}' with symbol '{transition.symbol}'")
            self.transition_dict[key] = transition.to_state
    

    #Reset Method
    def reset(self):
        self.current_state = self.config.initial_state
    

    #Strings Validation Method
    def validateString(self, input_string: str) -> bool:
        self.reset()
        
        for symbol in input_string:
            key = (self.current_state, symbol)
            if key not in self.transitionDict:
                return False
            self.current_state = self.transition_dict[key]
        
        return self.current_state in self.config.acceptance_states
    


    #DIagram Generation Method
    def generateDiagram(self) -> str:
        dot = graphviz.Digraph(format='png')
        
        #Nodes Definition
        for state in self.config.states:
            if state in self.config.acceptance_states:
                dot.node(state, shape='doublecircle')
            else:
                dot.node(state, shape='circle')
        
        #Add Initial State Arrow
        dot.node('', shape='none')
        dot.edge('', self.config.initial_state)


        #Add Transitions (Edges)
        for transition in self.config.transitions:
            dot.edge(transition.from_state, transition.to_state, label=transition.symbol)


        #Save Diagram
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"automaton_{self.config.id}_{timestamp}"
        output_path = os.path.join("diagrams", filename)

        #Directory Creation
        os.makedirs("diagrams", exist_ok=True)
        dot.render(output_path, cleanup=True)
        
        return output_path + ".png"