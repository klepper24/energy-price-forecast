# Use the official Airflow image as the base
FROM apache/airflow:2.10.5-python3.12

# Copy the requirements.txt file into the container
COPY requirements.txt /requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r /requirements.txt