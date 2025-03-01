"""Module for processing news data and generating word count statistics."""
import os
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

import pyspark.sql.functions as F
from pyspark.sql import SparkSession, DataFrame
from datasets import load_dataset
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType

# Configure logging
logger = logging.getLogger(__name__)

class DataProcessor:
    """
    Class to process data and generate word count statistics.
    """
    
    def __init__(self, config: Dict[str, Any], spark_session: Optional[SparkSession] = None):
        """
        Initialize the DataProcessor.
        
        Args:
            config: Configuration dictionary
            spark_session: Existing SparkSession (optional)
        """
        self.config = config
        self.spark = spark_session or self._create_spark_session()
        logger.info("DataProcessor initialized")
    
    def _create_spark_session(self) -> SparkSession:
        """
        Create a SparkSession.
        
        Returns:
            Configured SparkSession
        """
        spark_config = self.config.get("spark", {})
        app_name = spark_config.get("app_name", "WordCountProcessor")
        master = spark_config.get("master", "local[*]")
        
        logger.info(f"Creating SparkSession with app_name={app_name}, master={master}")
        
        return (
            SparkSession.builder
            .appName(app_name)
            .master(master)
            .config("spark.sql.execution.arrow.pyspark.enabled", "true")
            .getOrCreate()
        )
    
    def load_dataset(self, dataset_name: str) -> DataFrame:
        """
        Load dataset from Hugging Face.
        
        Args:
            dataset_name: Name of the dataset to load
            
        Returns:
            Spark DataFrame containing the loaded dataset
            
        Raises:
            ValueError: If dataset configuration is not found
        """
        dataset_config = self.config.get("dataset", {}).get(dataset_name)
        if not dataset_config:
            raise ValueError(f"Dataset configuration for {dataset_name} not found")
        
        source = dataset_config.get("source")
        logger.info(f"Loading dataset {source} from Hugging Face")
        
        # Load dataset using Hugging Face's datasets library
        hf_dataset = load_dataset(source, split="test")
        
        # Convert to pandas DataFrame first
        pandas_df = hf_dataset.to_pandas()
        
        # Create Spark DataFrame manually to avoid distutils dependency
        # Define schema based on dataset structure
        columns = list(pandas_df.columns)
        
        # Create rows from pandas data
        rows = pandas_df.to_dict('records')
        
        # Create RDD from rows
        rdd = self.spark.sparkContext.parallelize(rows)
        
        # Convert RDD to DataFrame
        spark_df = self.spark.createDataFrame(rdd)
        
        logger.info(f"Dataset loaded with {spark_df.count()} rows")
        
        return spark_df
    
    def process_specific_words(
        self, 
        spark_df: DataFrame, 
        dataset_name: str, 
        output_dir: str
    ) -> str:
        """
        Process specific words and count their occurrences.
        
        Args:
            spark_df: Spark DataFrame containing the dataset
            dataset_name: Name of the dataset being processed
            output_dir: Directory to save output
            
        Returns:
            Path to the saved parquet file
        """
        dataset_config = self.config.get("dataset", {}).get(dataset_name)
        description_col = dataset_config.get("description_column", "description")
        target_words = dataset_config.get("target_words", ["president", "the", "Asia"])
        
        logger.info(f"Processing specific words: {target_words}")
        
        # Create a list of expressions to count each word
        count_expressions = [
            F.sum(F.expr(f"size(array_remove(split(regexp_replace({description_col}, '[^a-zA-Z0-9\\s]', ' '), ' '), ''))")).alias("total_words")
        ]
        
        # Process each target word
        word_counts = []
        for word in target_words:
            # Count occurrences of the exact word (case sensitive)
            count = spark_df.select(
                F.sum(
                    F.size(
                        F.expr(f"array_intersect(split(regexp_replace({description_col}, '[^a-zA-Z0-9\\s]', ' '), ' '), array('{word}'))")
                    )
                ).alias("count")
            ).collect()[0]["count"]
            
            word_counts.append((word, count))
        
        # Create a DataFrame with the word counts
        word_count_df = self.spark.createDataFrame(word_counts, ["word", "word_count"])
        
        # Save the result
        output_prefix = self.config.get("output", {}).get("word_count_file_prefix", "word_count")
        current_date = datetime.now().strftime("%Y%m%d")
        output_path = os.path.join(output_dir, f"{output_prefix}_{current_date}.parquet")
        
        logger.info(f"Saving specific word counts to {output_path}")
        word_count_df.write.mode("overwrite").parquet(output_path)
        
        # Show the result
        logger.info("Word count result:")
        word_count_df.show()
        
        return output_path
    
    def process_all_words(
        self, 
        spark_df: DataFrame, 
        dataset_name: str, 
        output_dir: str
    ) -> str:
        """
        Process all unique words and count their occurrences.
        
        Args:
            spark_df: Spark DataFrame containing the dataset
            dataset_name: Name of the dataset being processed
            output_dir: Directory to save output
            
        Returns:
            Path to the saved parquet file
        """
        dataset_config = self.config.get("dataset", {}).get(dataset_name)
        description_col = dataset_config.get("description_column", "description")
        
        logger.info("Processing all unique words")
        
        # Explode the text into individual words and count each unique word
        word_count_df = spark_df.select(
            F.explode(
                F.split(
                    F.regexp_replace(F.col(description_col), "[^a-zA-Z0-9\\s]", " "), 
                    "\\s+"
                )
            ).alias("word")
        ).filter(F.col("word") != "")
        
        # Group by word and count occurrences
        word_count_df = word_count_df.groupBy("word").count().withColumnRenamed("count", "word_count")
        
        # Save the result
        output_prefix = self.config.get("output", {}).get("word_count_all_file_prefix", "word_count_all")
        current_date = datetime.now().strftime("%Y%m%d")
        output_path = os.path.join(output_dir, f"{output_prefix}_{current_date}.parquet")
        
        logger.info(f"Saving all word counts to {output_path}")
        word_count_df.write.mode("overwrite").parquet(output_path)
        
        # Show the result (limited to top 20 words)
        logger.info("All word count result (top 20):")
        word_count_df.orderBy(F.col("word_count").desc()).limit(20).show()
        
        return output_path
    
    def stop(self):
        """Stop the SparkSession."""
        if self.spark:
            logger.info("Stopping SparkSession")
            self.spark.stop()