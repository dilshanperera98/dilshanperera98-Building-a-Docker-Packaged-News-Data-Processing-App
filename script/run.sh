#!/bin/bash
set -e

# Activate conda environment
source /opt/conda/etc/profile.d/conda.sh
conda activate env

# Create log directory
mkdir -p /app/logs

# Run specific words processing
echo "Running word count for specific words..."
python /app/code/src/run.py process_data -cfg /app/code/config/cfg.yaml -dataset news -dirout /app/ztmp/data/ 2>&1 | tee /app/logs/data_processed.txt

# Run all words processing
echo "Running word count for all words..."
python /app/code/src/run.py process_data_all -cfg /app/code/config/cfg.yaml -dataset news -dirout /app/ztmp/data/ 2>&1 | tee /app/logs/data_processed_all.txt

# Print pip list to file
echo "Generating pip list output..."
pip list 2>&1 | tee /app/logs/pip_list.txt

echo "All processes completed successfully!"