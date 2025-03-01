"""Unit tests for the DataProcessor class."""
import unittest
import tempfile
import os
import shutil
from unittest.mock import patch, MagicMock

import pandas as pd
from pyspark.sql import SparkSession

# Add the src directory to path to import modules
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from data_processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment before all tests."""
        # Create a test SparkSession
        cls.spark = (
            SparkSession.builder
            .appName("TestWordCountProcessor")
            .master("local[*]")
            .getOrCreate()
        )
        
        # Create a temporary directory for test outputs
        cls.test_dir = tempfile.mkdtemp()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        # Stop SparkSession
        if cls.spark:
            cls.spark.stop()
            
        # Remove temporary directory
        shutil.rmtree(cls.test_dir, ignore_errors=True)
    
    def setUp(self):
        """Set up before each test."""
        # Test config
        self.config = {
            "spark": {
                "app_name": "TestWordCountProcessor",
                "master": "local[*]"
            },
            "dataset": {
                "news": {
                    "name": "ag_news",
                    "source": "sh0416/ag_news",
                    "description_column": "description",
                    "target_words": ["president", "the", "Asia"]
                }
            },
            "output": {
                "format": "parquet",
                "word_count_file_prefix": "word_count",
                "word_count_all_file_prefix": "word_count_all"
            }
        }
        
        # Create processor with existing SparkSession
        self.processor = DataProcessor(self.config, self.spark)
        
        # Sample data for testing
        data = [
            {"description": "The president of the United States visited Asia today."},
            {"description": "Asia is a large continent with many countries."},
            {"description": "The economy is growing in Asian markets."}
        ]
        
        # Create test DataFrame
        pandas_df = pd.DataFrame(data)
        self.test_df = self.spark.createDataFrame(pandas_df)
    
    @patch('data_processor.load_dataset')
    def test_load_dataset(self, mock_load_dataset):
        """Test loading dataset."""
        # Mock the Hugging Face dataset
        mock_dataset = MagicMock()
        mock_dataset.to_pandas.return_value = pd.DataFrame({
            "description": ["Test description 1", "Test description 2"]
        })
        mock_load_dataset.return_value = mock_dataset
        
        # Call the method
        result = self.processor.load_dataset("news")
        
        # Verify the result
        self.assertEqual(result.count(), 2)
        self.assertTrue("description" in result.columns)
        
        # Verify mock was called with the right arguments
        mock_load_dataset.assert_called_once_with("sh0416/ag_news", split="test")
    
    def test_process_specific_words(self):
        """Test processing specific words."""
        # Call the method
        output_path = self.processor.process_specific_words(
            self.test_df, 
            "news", 
            self.test_dir
        )
        
        # Verify output file exists
        self.assertTrue(os.path.exists(output_path))
        
        # Read the output file
        result_df = self.spark.read.parquet(output_path)
        
        # Verify the content
        self.assertEqual(result_df.count(), 3)  # Three target words
        
        # Check if all target words are in the result
        words = [row["word"] for row in result_df.select("word").collect()]
        self.assertTrue("president" in words)
        self.assertTrue("the" in words)
        self.assertTrue("Asia" in words)
    
    def test_process_all_words(self):
        """Test processing all unique words."""
        # Call the method
        output_path = self.processor.process_all_words(
            self.test_df, 
            "news", 
            self.test_dir
        )
        
        # Verify output file exists
        self.assertTrue(os.path.exists(output_path))
        
        # Read the output file
        result_df = self.spark.read.parquet(output_path)
        
        # Verify we have results
        self.assertTrue(result_df.count() > 0)
        
        # Check some specific words
        result_dict = {row["word"]: row["word_count"] for row in result_df.collect()}
        self.assertTrue("president" in result_dict)
        self.assertTrue("Asia" in result_dict)
        self.assertTrue("the" in result_dict)

if __name__ == "__main__":
    unittest.main()