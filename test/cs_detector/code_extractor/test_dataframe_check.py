import unittest
import ast

# Assuming dataframe_check and search_pandas_library are imported from your module
from cs_detector.code_extractor.dataframe_detector import dataframe_check, load_dataframe_dict

df_dict = load_dataframe_dict("../../../obj_dictionaries/dataframes.csv")


class TestDataFrameCheck(unittest.TestCase):

    def setUp(self):
        self.libraries = ['pandas']

    def test_single_dataframe_assignment(self):
        # Test case with a single DataFrame assignment
        source_code = """
def process_data():
    df = pandas.read_csv("data.csv")
    new_df = df
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]  # Get the function node

        result = dataframe_check(fun_node, self.libraries, df_dict)

        # Expected result should include 'df' and 'new_df'
        self.assertIn('df', result)
        self.assertIn('new_df', result)

    def test_dataframe_method_chaining(self):
        # Test case with method chaining
        source_code = """
def process_data():
    df = pandas.read_csv("data.csv")
    result_df = df.merge(another_df, how='inner')
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]  # Get the function node

        result = dataframe_check(fun_node, self.libraries, df_dict)

        # Expected result should include 'df' and 'result_df'
        self.assertIn('df', result)
        self.assertIn('result_df', result)

    def test_dataframe_subscript(self):
        # Test case where a DataFrame is accessed via subscript
        source_code = """
def process_data():
    df = pandas.read_csv("data.csv")
    selected_df = df[['col1', 'col2']]
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]  # Get the function node

        result = dataframe_check(fun_node, self.libraries, df_dict)

        # Expected result should include 'df' and 'selected_df'
        self.assertIn('df', result)
        self.assertIn('selected_df', result)

    def test_dataframe_with_no_pandas_import(self):
        # Test case where no pandas library is used
        source_code = """
def process_data():
    df = some_function_call()
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]  # Get the function node

        result = dataframe_check(fun_node, [], df_dict)

        # Expected result should be None as there's no pandas library
        self.assertIsNone(result)

    def test_dataframe_chained_methods(self):
        # Test case with chained pandas DataFrame methods
        source_code = """
def process_data():
    df = pandas.read_csv("data.csv")
    df2 = df.drop(columns=['col1'])
    df3 = df2.fillna(0)
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]  # Get the function node

        result = dataframe_check(fun_node, self.libraries, df_dict)

        # Expected result should include 'df', 'df2', and 'df3'
        self.assertIn('df', result)
        self.assertIn('df2', result)
        self.assertIn('df3', result)


if __name__ == '__main__':
    unittest.main()