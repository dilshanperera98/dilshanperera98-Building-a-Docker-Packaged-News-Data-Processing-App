"""Main entry point for the news data processing application."""
import os
import sys
import argparse
import logging
import subprocess
from typing import Dict, Any, List
from data_processor import DataProcessor
from utils import load_config, setup_logger

def parse_args() -> Dict[str, Any]:
    """
    Parse command line arguments.
    
    Returns:
        Dictionary containing parsed arguments
    """
    parser = argparse.ArgumentParser(description="Process news data and count word occurrences")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Define the process_data command
    process_data = subparsers.add_parser("process_data", help="Process specific words")
    process_data.add_argument("-cfg", "--config", type=str, required=True, help="Path to config file")
    process_data.add_argument("-dataset", type=str, required=True, help="Dataset name")
    process_data.add_argument("-dirout", type=str, required=True, help="Output directory")
    
    # Define the process_data_all command
    process_data_all = subparsers.add_parser("process_data_all", help="Process all unique words")
    process_data_all.add_argument("-cfg", "--config", type=str, required=True, help="Path to config file")
    process_data_all.add_argument("-dataset", type=str, required=True, help="Dataset name")
    process_data_all.add_argument("-dirout", type=str, required=True, help="Output directory")
    
    # Define the test command
    test_parser = subparsers.add_parser("test", help="Run unit tests")
    test_parser.add_argument("-p", "--path", type=str, default="/app/code/tests", help="Path to test directory")
    
    return vars(parser.parse_args())

def run_tests(test_path: str):
    """
    Run unit tests using pytest.
    
    Args:
        test_path (str): Path to the test directory
    """
    try:
        result = subprocess.run(
            ["pytest", test_path], 
            capture_output=True, 
            text=True, 
            check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Tests failed:")
        print(e.stdout)
        print(e.stderr)
        sys.exit(1)

def main():
    """Main entry point for the application."""
    # Parse command line arguments
    args = parse_args()
    
    # If running tests
    if args["command"] == "test":
        run_tests(args.get("path", "/app/code/tests"))
        return
    
    # Set up logging
    os.makedirs(args.get("dirout", "output"), exist_ok=True)
    logger = setup_logger(args["dirout"], f"pipeline_{args['command']}")
    
    logger.info(f"Starting command: {args.get('command')}")
    
    try:
        # Load configuration
        config = load_config(args["config"])
        
        # Initialize data processor
        processor = DataProcessor(config)
        
        # Load dataset
        dataset = processor.load_dataset(args["dataset"])
        
        # Execute command
        if args["command"] == "process_data":
            output_path = processor.process_specific_words(
                dataset, 
                args["dataset"], 
                args["dirout"]
            )
            logger.info(f"Process completed successfully. Output saved to {output_path}")
            
        elif args["command"] == "process_data_all":
            output_path = processor.process_all_words(
                dataset, 
                args["dataset"], 
                args["dirout"]
            )
            logger.info(f"Process completed successfully. Output saved to {output_path}")
            
        else:
            logger.error(f"Unknown command: {args.get('command')}")
            sys.exit(1)
            
    except Exception as e:
        logger.exception(f"Error executing command {args.get('command')}: {str(e)}")
        sys.exit(1)
        
    finally:
        # Stop the processor
        if 'processor' in locals():
            processor.stop()
    
    logger.info(f"Command {args.get('command')} completed successfully")

if __name__ == "__main__":
    main()
