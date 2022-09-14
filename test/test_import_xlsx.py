from pathlib import Path
import unittest
import os
import pandas as pd
import numpy as np


from utils.import_xlsx import Import

class TestDataFrame(unittest.TestCase):

    def setUp(self):
        """Initialising Import which will be tested
        """
        self.import_utils = Import()

    def test_ingest_feature_data(self):

        DATA_PATH = os.path.abspath((os.path.join("test", "data")))
        SCHEMA_PATH = os.path.abspath((os.path.join("config", "schema.json")))

        actual_output = self.import_utils.ingest_feature_data(data_path=DATA_PATH)

        schema_valid = self.import_utils.load_schema(SCHEMA_PATH)
        
        expected_output = pd.DataFrame(columns=[key for key in schema_valid], dtype="float64")
        expected_output_row1 = {"A": "2", "B": "28", "C": "1", "D": "0"}
        expected_output_row2 = {"A": "70", "B": "10", "C": "14", "D": "100"}
        expected_output = expected_output.append([expected_output_row1, expected_output_row2], ignore_index=True).astype("float64")

        pd.testing.assert_frame_equal(actual_output, expected_output)

    def test_invalid_data_path_raises_exception(self):
        """ defining incorrect path"""
        INCORRECT_PATH = "incorrect/data/path"

        with self.assertRaises(FileNotFoundError) as exception_context:
            self.import_utils.ingest_feature_data(data_path = INCORRECT_PATH)

        self.assertEqual(str(exception_context.exception),"File Path does not exist. Ensure you are in JENKINS_PIPELINE root directory")


    def test_invalid_schema_path_raises_exception(self):
        """ defining incorrect path"""
        INCORRECT_PATH = "incorrect/schema/path"

        with self.assertRaises(FileNotFoundError) as exception_context:
            self.import_utils.ingest_feature_data(data_path = Path("data"), schema_path=INCORRECT_PATH)

        self.assertEqual(str(exception_context.exception),"Schema Path does not exist. Ensure you are in JENKINS_PIPELINE root directory")
    
    def test_empty_dataframe_raises_exception(self):
        """ setting the path to be the root of project directory as there will be no excel files here resulting in an empty df """
        EMPTY_DATA_PATH = os.getcwd()

        with self.assertRaises(Exception) as exception_context:
            self.import_utils.ingest_feature_data(data_path = EMPTY_DATA_PATH)

        self.assertEqual(str(exception_context.exception),"Empty pd.DataFrame")
    
    def test_load_schema(self):

        CORRECT_INPUT = os.path.abspath(os.path.join('config', 'schema.json'))
        actual_output = self.import_utils.load_schema(schema_path = CORRECT_INPUT)
        
        expected_output = {
                            "A": {"type": "float", "allow_unknown": False, "empty": False, "minlength": 1},
                            "B": {"type": "float", "allow_unknown": False, "empty": False, "minlength": 1},
                            "C": {"type": "float", "allow_unknown": False, "empty": False, "minlength": 1},
                            "D": {"type": "float", "allow_unknown": False, "empty": False, "minlength": 1}
                        }

        self.assertEqual(actual_output, expected_output)


    def test_invalid_file_directory_load_schema_raises_exception(self):

        """ giving path to directory rather than path to file """
        INCORRECT_INPUT = os.path.abspath(os.path.join('config'))

        actual_output = self.import_utils.load_schema(schema_path = INCORRECT_INPUT)
        
        self.assertEqual(actual_output, "Path to directory given instead of path to file.")


    def test_not_json_file_load_schema_raises_exception(self):

        """ giving file that is not JSON """
        INCORRECT_INPUT = os.path.abspath(os.path.join('test/data', 'test1.xlsx'))
        actual_output = self.import_utils.load_schema(schema_path = INCORRECT_INPUT)
        
        self.assertEqual(actual_output, "File is not JSON. Could not be decoded.")
    
    def test_file_not_found_raises_exception(self):

        """ giving file that is not JSON """
        INCORRECT_INPUT = os.path.abspath(os.path.join('test/data', 'test2.xlsx'))
        actual_output = self.import_utils.load_schema(schema_path = INCORRECT_INPUT)
        
        self.assertEqual(actual_output, "File does not exist at given directory.")