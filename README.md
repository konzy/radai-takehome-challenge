# Data Engineer Take-Home Challenge: Mini ETL Pipeline.

### Objective

Develop a data processing pipeline that tranforms a large volume of text data from a Kinesis stream into a format suitable for the continuous training a text summarization model. The pipeline should leverage Python and be designed with enterprise-scale data processing tools in mind.

---

### Background

You're part of a dynamic team at a company specializing in NLP services dedicated to assisting news aggregators and content curators. The company's mission is to automate the summarization of articles and reports from diverse sources, enabling rapid access to distilled insights. This task is crucial for staying ahead in the fast-paced world of news and content curation, where the ability to quickly summarize and understand large volumes of text data can provide a significant competitive edge. 


### Overview

The NLP model must be trained on a regular schedule to keep up-to-date on the stylistic elements of modern journalism. Therefore in this challenge, you are entrusted with the development of a data pipeline capable of processing incoming text data efficiently. The ultimate goal is to enhance this data in ways that bolster machine learning (ML) training scenarios. This includes considering how the result is stored, ensuring that it supports efficient data access patterns suitable for large-scale processing and ML model training.

To kickstart your task, you are provided with a sample dataset alongside a foundational setup designed to simulate the ingestion of streaming text data. Your challenge is to extend and optimize this setup in a way explained below.

---

### Objective

Develop a data processing pipeline that retrieves each record from a Kinesis stream, enriches it by adding a calculated feature (e.g., word count) to every record, and computes the average of this metric for all records. The enriched records, now including the additional feature, should then be stored in an S3 bucket, ready for subsequent processing steps. Note that only the enriched records need to be stored; the calculated average does not require storage."


## **Getting Started**

### **Setup Instructions**

1. **Environment Setup**: Ensure Docker and Docker Compose are installed on your system. The provided **`docker-compose.yml`** includes services for LocalStack (simulating AWS S3 and Kinesis).
2. **Running the Pipeline**: Execute ```docker-compose up``` to launch the services. This command initiates a simulated AWS environment for your pipeline's operation. The setup involves starting two containers: one for simulating AWS services like S3 and Kinesis, and another for populating the Kinesis stream (named "MyStream") with approximately 1000 records and creating an S3 bucket ("my-bucket") for storage. The population script runs iteratively, simulating the continuous generation of data. 

### **Note to Candidates**
We understand that real-world data engineering projects often require dealing with incomplete information or making educated guesses about the best approach to a problem. In this challenge, should you encounter any ambiguities or feel that certain details are not specified, you are encouraged to make reasonable assumptions to fill in the gaps. Please document any such assumptions and the rationale behind them in your submission. This will help us understand your thought process and decision-making skills in navigating real-world scenarios.

## **Requirements**

- While not mandatory, you are encouraged to use an enterprise-scale data processing solution such as Metaflow, MLFlow, Spark, Apache Flink, or any other tool suitable for distributed processing of large datasets. Be prepared to justify your choice.
- Incorporate any new dependencies into the docker-compose environment, ensuring they can run locally and offline within Docker containers.
- Design your solution to facilitate machine learning training, focusing on data batching, storage, and retrieval for optimized access in large-scale ML model training.
- Provide documentation on how to set up and run your solution. Outline your design decisions, especially those related to the choice of data processing tools and storage for ML training.

## Submission Instructions

Clone this repository to download the boiler plate. Build your application based on this foundation and update the README accordingly. Submit your completed challenge via email.


# I Didn't Complete the Challenge
## Approach
My approach was to use Flink to read from the Kinesis stream and do the needed aggregations and then store to s3. 
This is so that it would emulate the managed Kinesis/Flink offering on AWS "Amazon Kinesis Data Analytics for SQL".
This would make the setup on AWS easy, as they will provision Kinesis and Flink, and the required jars to connect them as well as the s3 jar.
This AWS offering is also serverless, making it so that we don't need to keep Kubernetes pods running when there isn't any data flowing.

## Challenges
This was my first time using localstack, Kinesis, and PyFlink. 
My idea was to write the feature creation in Python so that in the future we could also do online training of the model.
Flink was fairly easy to write, after understanding that there are two different ways to define aggregations, data streams and tables.
It was pretty quick to make a test application that uses tables to print to the screen.

The problem arose when I went to connect Flink to LocalStack.
I think I ended up having the correct jar loaded in the right location, and the credentials defined correctly as well.
I couldn't find any Github projects that were similar to the same setup I was going after.

## Running It
I made a new Flink 1.18 Dockerfile that will use Maven to download the dependencies and put them in the right folder.
Build it using docker and tag it with `briank/pyflink:1.18`

Then use `docker compose` to spin up the cluster using the new Flink image.

The `flink-jobs` folder gets copied to the image to `/opt/flink/pyflink/jobs` and the `entrypoint` in the docker compose yaml will start the app.

The way that this is set up makes it easy to change and add to in the future, all that needs to happen is that a new python file is made in the `flink-jobs` folder and added to the entrypoint argument.

To add the new file, just append `&& python <path-to-file>` and that's it.

## Other Approaches to Delivery
### Approach 1
I would have paid for the pro version of localstack.

I had issues with connecting Kinesis and Flink. Also, the local testing environment would have been different than the AWS environment.
Purchasing the pro version would eliminate the issue with authentication and jars.
Both of these are needed in the local environment, but not the deployed version on AWS.
Also the pro version of localstack is pretty cheap and you can use it to create Cloud Formation scripts so that you can make multiple environments, eg. dev, stage.

### Approach 2
If that didn't work or if I couldn't buy the pro version of Localstack, I'd use Kafka and Flink.

Kafka and Flink are both open source projects, we can make this application cloud agnostic.
AWS can be expensive and moving to another cloud provider in the future may be more difficult as we build out this application.
If we make it cloud agnostic at the start, we can test performance on other platforms and migrate faster.
We would also use Terraform for deployment of this pod.

