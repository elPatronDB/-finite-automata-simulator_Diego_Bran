from flask import Flask, request, jsonify
from typing import List, Dict

from .validator import AutomatonConfig
from .automaton import Automaton




app = Flask(__name__)



@app.route('/process-automata', methods=['POST'])



def process_automata():
    if not request.is_json:
        return jsonify({"Error": "Sould be a JSON"}), 400

    data = request.get_json()
    
    if not isinstance(data, list):
        return jsonify({"Error": "JSON should contain a list"}), 400

    results: List[Dict] = []
    
    for automaton in data:
        automaton_id = automaton.get("id")
        
        if not automaton_id:
            results.append({"id": None, "success": False, "error_description": "No ID in Automaton"})
            continue
        
        result = {"id": automaton_id}
        
        try:
            automaton_config = AutomatonConfig(**automaton)
            automaton = Automaton(automaton_config)
            
            inputs_validation = [
                {"input": s, "result": automaton.validate_string(s)}
                for s in automaton_config.test_strings
            ]


            diagram_path = automaton.generate_diagram()
            result.update({
                "success": True,
                "inputs_validation": inputs_validation,
                "diagram_path": diagram_path
            })
        except Exception as e:
            result.update({
                "success": False,
                "error_description": str(e)
            })

        results.append(result)


    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)