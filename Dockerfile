FROM debian:bullseye-slim

# Set environment variables
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH="/opt/conda/bin:${PATH}"

# Install system dependencies
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
        wget \
        bzip2 \
        ca-certificates \
        curl \
        git \
        vim \
        procps \
        openjdk-11-jdk \
        build-essential \
        fonts-dejavu \
        unzip \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-py311_23.11.0-2-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    conda clean -afy

# Create and set up conda environment
RUN conda create -n env python=3.11 -y && \
    conda install -n env -c conda-forge \
        pyspark=3.5.0 \
        pytorch=2.1.2 \
        numpy=1.26.4 \
        pandas=2.2.1 \
        scipy=1.13.0 \
        scikit-learn=1.4.2 \
        polars=0.20.3 \
        pyarrow=15.0.2 \
        python-duckdb=0.10.1 \
        s3fs=2024.2.0 \
        spacy=3.7.4 \
        gensim=4.3.2 \
        numba=0.59.0 \
        sqlalchemy=2.0.29 \
        pytest=8.1.1 \
        openjdk=11.0.21 \
        -y && \
    conda clean -afy

# Install pip packages with verified versions
RUN /opt/conda/envs/env/bin/pip install --no-cache-dir \
    orjson==3.10.3 \
    awswrangler==3.7.0 \
    transformers==4.40.1 \
    accelerate==0.29.3 \
    neo4j==5.20.0 \
    umap-learn==0.5.6 \
    smart-open==7.1.0 \
    onnxruntime==1.17.1 \
    segeval==2.0.9 \
    datasets==2.19.1 \
    pyyaml==6.0.1

# Configure working environment
WORKDIR /app
COPY code/ /app/code/
COPY script/ /app/script/

# Set final environment variables
ENV PYTHONPATH=/app \
    JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64 \
    PATH="/opt/conda/envs/env/bin:${PATH}"

# Create directories
RUN mkdir -p /app/ztmp/data /app/logs

# Entrypoint
ENTRYPOINT ["python", "/app/code/src/run.py"]

CMD ["process_data"]
