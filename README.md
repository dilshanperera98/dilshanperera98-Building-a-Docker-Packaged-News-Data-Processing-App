News Data Processing & Analysis in PySpark (Dockerized)

▪ Developed a Dockerized PySpark application to process the AG News dataset.
▪ Extracted and counted word occurrences from the news descriptions.
▪ Implemented two word frequency analyses:
   Predefined words ("president", "the", "Asia").
   All unique words in the dataset.
▪ Stored results as Parquet files with timestamps.
▪ Packaged the application in a Debian-based Docker image with Conda.
▪ Automated the Docker build using GitHub Actions.
▪ Included logging, type hints, basic tests, and structured code quality.
▪ Provided bash scripts & YAML-based config files for easy execution.

▪ Technologies Used
  Big Data Processing: PySpark
  Programming Language: Python (3.11)
  Data Storage: Parquet, PyArrow
  Containerization: Docker (Debian-based)
  Package Management: Conda
  Automation & CI/CD: GitHub Actions
  Libraries & Frameworks: Pandas, NumPy, Scikit-learn, Transformers, PyTorch, DuckDB, AWS Wrangler
  Logging & Testing: Python Logging, PyTest
  Configuration Management: YAML


 🪧 Project Description
This project involved developing a Dockerized PySpark-based application to process and analyze public news data from the AG News dataset. The main objective was to extract and count word occurrences from the news description column and store the results in Parquet format.

The application performed two main tasks:

Predefined Word Count Analysis:

Counted occurrences of the words "president", "the", and "Asia" in the news descriptions.
Saved results in Parquet format with a timestamped filename.
Full Word Count Analysis:

Counted occurrences of all unique words in the dataset’s news descriptions.
Stored the results in a separate Parquet file with a timestamped filename.
The project was structured with modular and well-documented code, following software engineering best practices such as logging, type hints, and basic unit testing.

To ensure portability and automation, the entire application was packaged into a Docker container (Debian-based) using Conda for dependency management. The Docker image build was automated using GitHub Actions, ensuring a seamless deployment process.

A YAML-based configuration file was implemented to allow flexibility in input parameters, output directories, and dataset selection. A Bash script was also included for streamlined execution of the processing pipeline.

Additionally, the project incorporated structured logging and pipeline logs, capturing key steps such as Docker builds, data processing, and dependency installations.
