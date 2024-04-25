# Creating a Streamlined Data Pipeline: Using Kafka, Spark, Airflow, and Docker

In today's digital landscape, data engineering is essential for managing the vast amount of datawe encounter daily. We'll use Kafka for data streaming, Spark for processing, Airflow for managing tasks, 
Docker for easy deployment, S3 for storage, and Python for scripting.

To show how it works, we have the Random Name API, a tool that gives us random data whenever we ask for it. First, we'll create a Python script to fetch data from this API at regular intervals, 
making it seem like streaming data. This same script will also send the data to Kafka for storage.

Then, we'll use Airflow to manage everything. Its DAGs will ensure our Python script runs smoothly and keeps streaming data into our pipeline. Once the data is in Kafka, Spark will jump in to 
process it before saving it in S3 for further analysis.

One cool thing about our setup is that each part runs in its own Docker container. This makes everything easier to manage and scale up if needed.

## Architecture

<img width="773" alt="Screenshot 2024-04-25 001738" src="https://github.com/THANUSHKIRAN/API-Streaming/assets/53527645/cf3d8a06-c54d-48fb-94e5-d86bfbb4115d">

## Tech Stack

Python,Docker, Kubernetes, Kafka, Spark, Airflow and AWS








