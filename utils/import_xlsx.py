import os
import json
import glob
import pandas as pd
import numpy as np
from cerberus import Validator

class Import:

    def map_xslx_to_json(self, excel_data_df: pd.DataFrame):

        """
        Common utility function to map excel file to json used in main class

        Args:
            excel_data_df: pandas.DataFrame
        """

        data = excel_data_df.to_json(orient='records')
        json_data = json.loads(data)
        
        return json_data


    def load_schema(self, schema_path: str):

        """
        Common utility function to read schema from json file.

        Args:
            excel_data_df: pandas.DataFrame
        """
        try:
            with open(schema_path, 'r') as f:
                schema = f.read()
            schema = json.loads(schema)
            return schema
        except IsADirectoryError as e:
            # raise Exception("Path to directory given instead of path to file.") from e
            return "Path to directory given instead of path to file."
        except ValueError:
            return "File is not JSON. Could not be decoded."
        except FileNotFoundError:
            return "File does not exist at given directory."
        

    def ingest_feature_data(self, data_path: str, 
                            schema_path: str = os.path.abspath(os.path.join('config', 'schema.json'))):

        """
        Read and concatenate xlsx files which contain claims flagged for edit.

        Args:
            data_path: path to folder containing excel files.
            schema_path: path to the desired schema, default is config/schema.json.

        Returns:
            pd.DataFrame
        """
        
        """ checking paths exist """
        if not os.path.exists(data_path):
            raise FileNotFoundError('File Path does not exist. Ensure you are in JENKINS_PIPELINE root directory')

        if not os.path.exists(schema_path):
            raise FileNotFoundError('Schema Path does not exist. Ensure you are in JENKINS_PIPELINE root directory')

        """ importing desired schema, initiating validator and defining empty df to which each file will be appended """
        schema_valid = self.load_schema(schema_path)
        schema_validator = Validator(schema_valid)


        feature_df = pd.DataFrame(columns=[key for key in schema_valid], dtype='float64')

    
        for file in glob.glob(os.path.join(data_path, '*.xlsx')):

            """ importing each file and ensuring all columns are of float type """
            feature_subset_df = pd.read_excel(file, dtype='float64')

            feature_subset_df = feature_subset_df.replace(np.nan, 0.0)

            """ mapping df to json so that it can be checked by cerberus validator """
            feature_data_json = self.map_xslx_to_json(feature_subset_df)
            
            for document in feature_data_json:
                v = schema_validator.validate(document)
                if not v:
                    err = schema_validator.errors
                    raise Exception(f"The following errors were raised: {err}")
            
            """ appending each individual df """
            feature_df = feature_df.append(feature_subset_df,ignore_index=True)

        if feature_df.empty:
            raise Exception('Empty pd.DataFrame')

        return feature_df

