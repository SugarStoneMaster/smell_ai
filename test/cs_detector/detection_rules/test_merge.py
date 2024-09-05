import unittest
import ast

from cs_detector.code_extractor.dataframe_detector import load_dataframe_dict
from cs_detector.detection_rules.Generic import merge_api_parameter_not_explicitly_set

df_dict = load_dataframe_dict("../../../obj_dictionaries/dataframes.csv")


class TestMergeAPIParameter(unittest.TestCase):

    def setUp(self):
        self.libraries = ['pandas']
        self.filename = "test_file.py"

    def test_merge_no_parameters(self):
        # Case where 'merge()' is called without any parameters
        source_code = """

def process_data():
    df1 = pandas.DataFrame()
    df2 = pandas.DataFrame()
    df1.merge(df2)
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        result, smells = merge_api_parameter_not_explicitly_set(self.libraries, self.filename, fun_node, df_dict)

        self.assertEqual(len(smells), 1)
        self.assertIn("merge_api_parameter_not_explicitly_set", result)

    def test_merge_all_parameters(self):
        # Case where 'merge()' is called with all required parameters
        source_code = """
def process_data():
    df1 = pandas.DataFrame()
    df2 = pandas.DataFrame()
    df1.merge(df2, how='inner', on='id', validate='one_to_one')
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        result, smells = merge_api_parameter_not_explicitly_set(self.libraries, self.filename, fun_node, df_dict)

        self.assertEqual(len(smells), 0)
        self.assertFalse(result)

    def test_merge_some_missing_parameters(self):
        # Case where 'merge()' is called with some missing parameters (e.g., 'how' missing)
        source_code = """
def process_data():
    df1 = pandas.DataFrame()
    df2 = pandas.DataFrame()
    df1.merge(df2, on='id', validate='one_to_one')
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        result, smells = merge_api_parameter_not_explicitly_set(self.libraries, self.filename, fun_node, df_dict)

        self.assertEqual(len(smells), 1)
        self.assertIn("merge_api_parameter_not_explicitly_set", result)

    def test_no_merge_call(self):
        # Case where no 'merge()' function is called
        source_code = """
def process_data():
    df1 = pandas.DataFrame()
    df1.sum()
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        result, smells = merge_api_parameter_not_explicitly_set(self.libraries, self.filename, fun_node, df_dict)

        self.assertEqual(len(smells), 0)
        self.assertFalse(result)

    def test_merge_with_keywords_none(self):
        # Case where 'merge()' is called but with no keywords (edge case)
        source_code = """
def process_data():
    df1 = pandas.DataFrame()
    df2 = pandas.DataFrame()
    df1.merge(df2, how=None, on=None, validate=None)
        """
        tree = ast.parse(source_code)
        fun_node = tree.body[0]

        result, smells = merge_api_parameter_not_explicitly_set(self.libraries, self.filename, fun_node, df_dict)

        self.assertEqual(len(smells), 1)
        self.assertIn("merge_api_parameter_not_explicitly_set", result)


if __name__ == '__main__':
    unittest.main()