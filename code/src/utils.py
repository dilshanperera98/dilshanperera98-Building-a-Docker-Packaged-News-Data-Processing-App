"""Utility functions for the data processing pipeline."""
import os
import yaml
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration YAML file
        
    Returns:
        Dictionary containing configuration parameters
        
    Raises:
        FileNotFoundError: If the config file doesn't exist
    """
    logger.info(f"Loading configuration from {config_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at {config_path}")
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    logger.info("Configuration loaded successfully")
    return config

def get_output_path(
    dir_out: str, 
    file_prefix: str, 
    date_format: str = "%Y%m%d"
) -> str:
    """
    Generate output path with formatted date.
    
    Args:
        dir_out: Output directory
        file_prefix: Prefix for the output file
        date_format: Format for the date string
        
    Returns:
        Formatted output path including directory, prefix, and date
    """
    # Create output directory if it doesn't exist
    os.makedirs(dir_out, exist_ok=True)
    
    # Get current date in required format
    current_date = datetime.now().strftime(date_format)
    
    # Format the output path
    output_path = os.path.join(dir_out, f"{file_prefix}_{current_date}.parquet")
    logger.info(f"Output will be saved to {output_path}")
    
    return output_path

def validate_args(args: Dict[str, Any], required_args: List[str]) -> bool:
    """
    Validate that required arguments are present.
    
    Args:
        args: Dictionary of arguments
        required_args: List of required argument keys
        
    Returns:
        True if all required arguments are present, False otherwise
    """
    for arg in required_args:
        if arg not in args or args[arg] is None:
            logger.error(f"Required argument '{arg}' is missing")
            return False
    return True

def setup_logger(output_dir: str, logger_name: str) -> logging.Logger:
    """
    Setup a logger that outputs to both console and file.
    
    Args:
        output_dir: Directory to save log file
        logger_name: Name of the logger
        
    Returns:
        Configured logger instance
    """
    # Create log directory if it doesn't exist
    log_dir = os.path.join(output_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create file handler
    log_file = os.path.join(log_dir, f"{logger_name}_{datetime.now().strftime('%Y%m%d')}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger