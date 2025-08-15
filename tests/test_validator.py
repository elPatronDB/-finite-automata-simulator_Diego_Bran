import unittest
from src.validator import AutomatonValidator, AutomatonError

class TestAutomatonValidator(unittest.TestCase):
    # Test suite for AutomatonValidator
    def setUp(self):
        self.valid_config = {
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

    # Test cases for AutomatonValidator
    def test_valid_config(self):
        try:
            validator = AutomatonValidator(self.valid_config)
            validator.validate()
            self.assertTrue(True, "Valid configuration should not raise exceptions")
        except AutomatonError:
            self.fail("Valid configuration raised an unexpected exception")


    # Test cases for various validation errors
    def test_missing_initial_state(self):
        config = self.valid_config.copy()
        config["initial_state"] = ""
        with self.assertRaises(AutomatonError) as context:
            validator = AutomatonValidator(config)
            validator.validate()
        self.assertEqual(str(context.exception), "Missing initial state in Automaton JSON")


    # Test cases for initial state not in states
    def test_initial_state_not_in_states(self):
        config = self.valid_config.copy()
        config["initial_state"] = "q2"
        with self.assertRaises(AutomatonError) as context:
            validator = AutomatonValidator(config)
            validator.validate()
        self.assertEqual(str(context.exception), "Oh no! The initial state is not in states")


    # Test cases for acceptance states not in states
    def test_invalid_acceptance_states(self):
        config = self.valid_config.copy()
        config["acceptance_states"] = {"q2"}
        with self.assertRaises(AutomatonError) as context:
            validator = AutomatonValidator(config)
            validator.validate()
        self.assertEqual(str(context.exception), "Oh no! Acceptance states should be in states")

    # Test cases for empty alphabet
    def test_empty_alphabet(self):
        config = self.valid_config.copy()
        config["alphabet"] = set()
        with self.assertRaises(AutomatonError) as context:
            validator = AutomatonValidator(config)
            validator.validate()
        self.assertEqual(str(context.exception), "The alphabet is empty")

    # Test cases for empty states
    def test_empty_states(self):
        config = self.valid_config.copy()
        config["states"] = set()
        with self.assertRaises(AutomatonError) as context:
            validator = AutomatonValidator(config)
            validator.validate()
        self.assertEqual(str(context.exception), "The states are empty")

    # Test cases for transitions not in states
    def test_invalid_transition_from_state(self):
        config = self.valid_config.copy()
        config["transitions"][0]["from_state"] = "q2"
        with self.assertRaises(AutomatonError) as context:
            validator = AutomatonValidator(config)
            validator.validate()
        self.assertEqual(str(context.exception), "Transition is not in states")


    # Test cases for transitions not in states
    def test_invalid_transition_to_state(self):
        config = self.valid_config.copy()
        config["transitions"][0]["to_state"] = "q2"
        with self.assertRaises(AutomatonError) as context:
            validator = AutomatonValidator(config)
            validator.validate()
        self.assertEqual(str(context.exception), "Transition state is not in states")

    # Test cases for transition symbol not in alphabet
    def test_invalid_transition_symbol(self):
        config = self.valid_config.copy()
        config["transitions"][0]["symbol"] = "2"
        with self.assertRaises(AutomatonError) as context:
            validator = AutomatonValidator(config)
            validator.validate()
        self.assertEqual(str(context.exception), "Transition symbol not in alphabet")

    # Test cases for missing transitions for each state and symbol
    def test_missing_transition(self):
        config = self.valid_config.copy()
        config["transitions"] = [
            {"from_state": "q0", "symbol": "0", "to_state": "q0"},
            {"from_state": "q1", "symbol": "0", "to_state": "q0"}
        ]
        with self.assertRaises(AutomatonError) as context:
            validator = AutomatonValidator(config)
            validator.validate()
        self.assertEqual(str(context.exception), "A Transition is missing for state and symbol")

    # Test cases for invalid config format
    def test_invalid_config_format(self):
        config = self.valid_config.copy()
        del config["id"]
        with self.assertRaises(AutomatonError) as context:
            validator = AutomatonValidator(config)
            validator.validate()
        self.assertTrue("Oh no! There is a problem" in str(context.exception))

if __name__ == '__main__':
    unittest.main()