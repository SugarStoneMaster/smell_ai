from cs_detector.detection_rules.Generic import hyperparameters_randomness_not_explicitly_set
import unittest
import ast


# Sample test models and hyperparameters
test_model_dict = {
    'library': ['sklearn', 'tensorflow'],
    'method': ['LogisticRegression()', 'RandomForestClassifier()', 'Sequential()'],
    'hyperparameters': ['penalty,C,solver,max_iter', 'n_estimators,criterion,max_depth,min_samples_split,min_samples_leaf,random_state', 'optimizer,loss,metrics']
}

# Sample test libraries (libraries imported in the file)
test_libraries = ['sklearn', 'tensorflow']


class TestHyperparametersRandomness(unittest.TestCase):

    def test_missing_hyperparameters(self):
        # Test case where the function is missing some hyperparameters
        source_code = """
def train_model():
    model = LogisticRegression(solver='lbfgs')
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]
        libraries = ['sklearn']

        filename = "test_file.py"
        result, smells = hyperparameters_randomness_not_explicitly_set(libraries, filename, fun_node, test_model_dict)

        self.assertTrue(smells)
        self.assertEqual(smells[0]['smell_name'], 'hyperparameters_not_explicitly_set')
        self.assertIn('Missing parameters: penalty, C, max_iter', result[-1])

    def test_missing_random_state(self):
        # Test case where the function is missing 'random_state' (randomness uncontrolled)
        source_code = """
def train_model():
    model = RandomForestClassifier(n_estimators=100)
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]
        libraries = ['sklearn']

        filename = "test_file.py"
        result, smells = hyperparameters_randomness_not_explicitly_set(libraries, filename, fun_node, test_model_dict)

        self.assertTrue(smells)
        self.assertEqual(smells[0]['smell_name'], 'hyperparameters_not_explicitly_set')
        self.assertIn('Warning: Randomness is uncontrolled', result[-1])

    def test_all_hyperparameters_set(self):
        # Test case where all hyperparameters are set correctly
        source_code = """
def train_model():
        model = RandomForestClassifier(
            n_estimators=100, 
            criterion='gini', 
            max_depth=10, 
            min_samples_split=2, 
            min_samples_leaf=1, 
            random_state=42
        )
            """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]
        libraries = ['sklearn']

        filename = "test_file.py"
        result, smells = hyperparameters_randomness_not_explicitly_set(libraries, filename, fun_node, test_model_dict)

        self.assertFalse(smells)

    def test_non_model_function(self):
        # Test case where the function does not deal with a model
        source_code = """
def process_data():
    data = [1, 2, 3]
    return sum(data)
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]
        libraries = ['sklearn']

        filename = "test_file.py"
        result, smells = hyperparameters_randomness_not_explicitly_set(libraries, filename, fun_node, test_model_dict)

        self.assertFalse(smells)

    def test_function_with_no_libraries(self):
        # Test case where no relevant libraries are imported
        source_code = """
def train_model():
    model = RandomForestClassifier(n_estimators=100)
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]
        libraries = []

        filename = "test_file.py"
        result, smells = hyperparameters_randomness_not_explicitly_set(libraries, filename, fun_node, test_model_dict)

        self.assertFalse(smells)


if __name__ == '__main__':
    unittest.main()