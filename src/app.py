from flask import Flask, request, jsonify
from .validator import AutomatonValidator, AutomatonError
from .automaton import Automaton
from typing import List, Dict

app = Flask(__name__)


@app.route('/process-automata', methods=['POST'])
def process_automata():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "Input must be a list of automata"}), 400

    results: List[Dict] = []
    for automaton in data:
        automaton_id = automaton.get("id")
        if not automaton_id:
            results.append({"id": None, "success": False, "error_description": "No se proporcionó un ID para el autómata"})
            continue
        result = {"id": automaton_id}
        try:
            validator = AutomatonValidator(automaton)
            validator.validate()
            automaton_instance = Automaton(validator.config)
            inputs_validation = [
                {"input": s, "result": automaton_instance.validate_string(s)}
                for s in validator.config.test_strings
            ]
            diagram_path = automaton_instance.generate_diagram()
            result.update({
                "success": True,
                "inputs_validation": inputs_validation,
                "diagram_path": diagram_path
            })
        except Exception as e:
            result.update({
                "success": False,
                "error_description": f"Error inesperado: {str(e)}"
            })
        results.append(result)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)