# 📰 News Data Processing & Analysis in PySpark (Dockerized)  

This project involves developing a **Dockerized PySpark-based application** to process and analyze public news data from the **AG News dataset**.  
The application extracts and counts word occurrences in news descriptions and stores the results in **Parquet format**.  

---

## 🚀 Key Features  

✅ **Predefined Word Count Analysis**: Counts occurrences of the words **"president", "the", and "Asia"**.  
✅ **Full Word Count Analysis**: Counts occurrences of **all unique words** in the dataset.  
✅ **PySpark-based Big Data Processing** for scalability.  
✅ **Parquet Storage with Timestamps** for structured data output.  
✅ **Dockerized** for portability and environment consistency.  
✅ **GitHub Actions for CI/CD** automating the Docker build process.  
✅ **Logging & Testing** for structured and maintainable code.  
✅ **YAML-based Configuration** for flexible input parameters and output control.  
✅ **Bash Scripts for Easy Execution**.  

---

## 🛠️ Technologies Used  

- **Big Data Processing**: PySpark  
- **Programming Language**: Python (3.11)  
- **Data Storage**: Parquet, PyArrow  
- **Containerization**: Docker (Debian-based)  
- **Package Management**: Conda  
- **Automation & CI/CD**: GitHub Actions  
- **Libraries & Frameworks**: Pandas, NumPy, Scikit-learn, Transformers, PyTorch, DuckDB, AWS Wrangler  
- **Logging & Testing**: Python Logging, PyTest  
- **Configuration Management**: YAML  

---

## 📌 Project Description  

The application **processes and analyzes the AG News dataset** to extract meaningful insights.  
It is structured with **modular code, logging, and testing**, following software engineering best practices.  

### 🔹 Workflow Overview  
1️⃣ **Predefined Word Count Analysis**:  
   - Extracts occurrences of `"president"`, `"the"`, and `"Asia"` from news descriptions.  
   - Saves the results in **Parquet format** with a timestamped filename.  

2️⃣ **Full Word Count Analysis**:  
   - Counts occurrences of **all unique words** in the dataset.  
   - Stores results in a separate **Parquet file with timestamps**.  

3️⃣ **Dockerized Processing Pipeline**:  
   - Uses a **Debian-based Docker image with Conda** for dependency management.  
   - Automates Docker image builds using **GitHub Actions**.  
   - Uses a **YAML-based configuration file** for input flexibility.  
   - Includes **structured logging** for debugging and monitoring.  
   - Provides a **Bash script for seamless execution**.  

---

## 🏗️ Setup & Execution  

### 🔹 1. Activate Virtual Environment (Optional)  
```bash
source .venv/bin/activate
