import unittest
import ast

# Assuming recursive_search_variables is imported from the module
from cs_detector.code_extractor.dataframe_detector import recursive_search_variables, load_dataframe_dict

df_dict = load_dataframe_dict("../../../obj_dictionaries/dataframes.csv")


class TestRecursiveSearchVariables(unittest.TestCase):

    def setUp(self):
        self.libraries = ['pandas']

    def test_single_dataframe_assignment(self):
        # Code where a dataframe is assigned to a variable
        source_code = """
def process_data():
    df = pd.read_csv("data.csv")
    new_df = df
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        # Starting list with 'df' because it's the initial dataframe
        result = recursive_search_variables(fun_node, ['df'], df_dict)

        # Expected to return both 'df' and 'new_df' since they are assigned the dataframe
        self.assertIn('df', result)
        self.assertIn('new_df', result)

    def test_dataframe_method_call(self):
        # Code where a dataframe undergoes method chaining (e.g., merge, groupby)
        source_code = """
def process_data():
    df = pd.read_csv("data.csv")
    merged_df = df.merge(another_df, how='inner')
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        # Starting with 'df' (dataframe read by read_csv)
        result = recursive_search_variables(fun_node, ['df'], df_dict)

        # Expected to return 'df' and 'merged_df'
        self.assertIn('df', result)
        self.assertIn('merged_df', result)

    def test_no_dataframe(self):
        # Code without any dataframe
        source_code = """
def process_data():
    data = [1, 2, 3, 4]
    result = sum(data)
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        # No dataframe expected
        result = recursive_search_variables(fun_node, [], df_dict)
        self.assertEqual(result, [])

    def test_dataframe_method_with_subscript(self):
        # Code where a dataframe is accessed with subscript (e.g., df['column'])
        source_code = """
def process_data():
    df = pd.read_csv("data.csv")
    selected_df = df[['col1', 'col2']]
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        # Starting with 'df' (dataframe read by read_csv)
        result = recursive_search_variables(fun_node, ['df'], df_dict)

        # Expected to include 'selected_df' since it selects from df
        self.assertIn('selected_df', result)
        self.assertIn('df', result)

    def test_dataframe_chained_assignment(self):
        # Code where a dataframe undergoes multiple operations
        source_code = """
def process_data():
    df = pd.read_csv("data.csv")
    grouped_df = df.groupby("column")
    result_df = grouped_df.set_index("index")
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        # Starting with 'df' (dataframe read by read_csv)
        result = recursive_search_variables(fun_node, ['df'], df_dict)

        # Expected to return 'df', 'grouped_df', and 'result_df'
        self.assertIn('df', result)
        self.assertIn('grouped_df', result)
        self.assertIn('result_df', result)

if __name__ == '__main__':
    unittest.main()