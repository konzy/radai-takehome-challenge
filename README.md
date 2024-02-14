# Data Engineer Take-Home Challenge: Mini Pipeline for Text Summarization

### Objective

Develop a data processing pipeline that ingests large volumes of text data and produces concise summaries. The pipeline should leverage Python and be designed with enterprise-scale data processing tools in mind.

---

### Background

You're part of a dynamic team at a company specializing in NLP services, dedicated to assisting news aggregators and content curators. The company's mission is to automate the summarization of articles and reports from diverse sources, enabling rapid access to distilled insights. This task is crucial for staying ahead in the fast-paced world of news and content curation, where the ability to quickly summarize and understand large volumes of text data can provide a significant competitive edge.

### Overview

In this challenge, you are entrusted with the development of a pipeline capable of processing text data efficiently. The ultimate goal is to enhance this data in ways that bolster machine learning (ML) training scenarios. This includes considering how the result is stored, ensuring that it supports efficient data access patterns suitable for large-scale processing and ML model training, in offline batch processing context.

To kickstart your task, you are provided with a sample dataset alongside a foundational setup designed to simulate the ingestion of streaming text data. Your challenge is to extend and optimize this setup in a way explained below.

---

### Text Transformation

Implement a pipeline that adds a calculated feature to each text record, such as word count. 


## **Getting Started**

### **Setup Instructions**

1. **Environment Setup**: Ensure Docker and Docker Compose are installed on your system. The provided **`docker-compose.yml`** includes services for LocalStack (simulating AWS S3 and Kinesis) and placeholders for your processing scripts.
2. **Running the Pipeline**: Navigate to the directory containing **`docker-compose.yml`** and run **`docker-compose up`** to start the services. This will initialize the simulated AWS environment where your pipeline will operate. This would start two containers, one of them will exit after creating an S3 bucket (my-bucket) and a Kinesis stream (MyStream) populated with ~1000 records. You can alter number of records to be generated by changing the value of an environment variable in **`docker-compose.yml`** 

### **Data Storage**

- **Amazon S3 Bucket**: Processed data should be stored in the designated S3 bucket, structured to facilitate efficient batch reads. Consider how the data will be consumed in machine learning training when designing your storage schema.

## **Requirements**

- While not mandatory, you are encouraged to use an offline, enterprise-scale data processing solution such as Metaflow, MLFlow, Apache Flink or any other tool suitable for distributed processing of large datasets. These tools can significantly enhance your pipeline's ability to handle millions of records efficiently and are highly recommended for candidates familiar with these technologies. It's essential that the tool you choose can be run within a Docker container as part of the docker-compose environment locally.
- **Optimization for ML Training**: Architect your solution with a focus on machine learning training scenarios. This includes considerations on how data is batched, stored, and retrieved, ensuring optimized access patterns for large-scale machine learning model training.
- **Scalability**: Your system should be designed to process millions of text records efficiently, demonstrating a clear understanding of scalability principles and distributed processing techniques.
- **Documentation**: Provide comprehensive documentation on how to set up and run your solution, including any dependencies and environment setup. Clearly outline your design decisions, especially those related to the choice of data processing tools and storage schema optimizations for ML training.
