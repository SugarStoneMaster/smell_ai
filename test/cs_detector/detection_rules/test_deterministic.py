import unittest
import ast

from cs_detector.detection_rules.Generic import deterministic_algorithm_option_not_used

class TestDeterministicAlgorithmOption(unittest.TestCase):

    def setUp(self):
        # Set up common values for the tests
        self.libraries = ['torch']
        self.filename = "test_file.py"

    def test_deterministic_algorithm_used(self):
        # Case where 'torch.use_deterministic_algorithms(True)' is used
        source_code = """
def train_model():
    torch.use_deterministic_algorithms(True)
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        result, smells = deterministic_algorithm_option_not_used(self.libraries, self.filename, fun_node)

        self.assertEqual(len(smells), 1)
        self.assertIn("deterministic_algorithm_option_not_used", result)

    def test_deterministic_algorithm_not_used(self):
        # Case where 'torch.use_deterministic_algorithms()' is not used
        source_code = """
def train_model():
    pass
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        result, smells = deterministic_algorithm_option_not_used(self.libraries, self.filename, fun_node)

        self.assertEqual(len(smells), 0)
        self.assertFalse(result)

    def test_deterministic_algorithm_used_false(self):
        # Case where 'torch.use_deterministic_algorithms(False)' is used
        source_code = """
def train_model():
    torch.use_deterministic_algorithms(False)
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        result, smells = deterministic_algorithm_option_not_used(self.libraries, self.filename, fun_node)

        self.assertEqual(len(smells), 0)
        self.assertFalse(result)

    def test_no_torch_usage(self):
        # Case where 'torch' is not used at all
        source_code = """
def train_model():
    print("No torch usage")
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        result, smells = deterministic_algorithm_option_not_used(self.libraries, self.filename, fun_node)

        self.assertEqual(len(smells), 0)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()