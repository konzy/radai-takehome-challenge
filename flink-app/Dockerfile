FROM apache/flink:1.18.1

# update
RUN apt-get update -y && apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev \
  libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
  xz-utils tk-dev libffi-dev liblzma-dev openssl git

# # install python
ENV PYTHON_VERSION='3.8.18'
ENV PYTHON_VERSION_SHORT='3.8'
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz && \
tar -xvf Python-$PYTHON_VERSION.tgz && \
cd Python-$PYTHON_VERSION && \
./configure --without-tests --enable-shared && \
make -j6 && \
make install && \
ldconfig /usr/local/lib && \
cd .. && \
rm -f Python-$PYTHON_VERSION.tgz

# python cleanup
RUN rm -rf Python-$PYTHON_VERSION && \
ln -s /usr/local/bin/python3 /usr/local/bin/python && \
apt-get clean && \
rm -rf /var/lib/apt/lists/*

# install requirements
COPY requirements.txt .
RUN pip3 install --no-cache-dir -v -r requirements.txt

# copy s3 jar to flink plugins
ENV FLINK_VERSION='1.18.1'
RUN mkdir /opt/flink/plugins/s3-fs-hadoop && cp /opt/flink/opt/flink-s3-fs-hadoop-$FLINK_VERSION.jar /opt/flink/plugins/s3-fs-hadoop

# install kinesis jar and copy to lib
ENV FLINK_VERSION_SHORT='1.18'
ENV MAVEN_VERSION='3.9.7'
ENV KINESIS_CONNECTOR_VERSION='4.3.0'
RUN curl -O  https://dlcdn.apache.org/maven/maven-3/$MAVEN_VERSION/binaries/apache-maven-$MAVEN_VERSION-bin.tar.gz && \
    tar xzvf apache-maven-$MAVEN_VERSION-bin.tar.gz && \
    apache-maven-$MAVEN_VERSION/bin/mvn dependency:get -Dartifact=org.apache.flink:flink-connector-kinesis:$KINESIS_CONNECTOR_VERSION-$FLINK_VERSION_SHORT

RUN find $HOME/.m2/repository/ -type f -name "*.jar" | xargs -I'{}' cp '{}' /opt/flink/lib

RUN cp $HOME/.m2/repository/org/apache/flink/flink-connector-kinesis/$KINESIS_CONNECTOR_VERSION-$FLINK_VERSION_SHORT/flink-connector-kinesis-$KINESIS_CONNECTOR_VERSION-$FLINK_VERSION_SHORT.jar /usr/local/lib/python$PYTHON_VERSION_SHORT/site-packages/pyflink/lib
RUN cp $HOME/.m2/repository/org/apache/flink/flink-connector-kinesis/$KINESIS_CONNECTOR_VERSION-$FLINK_VERSION_SHORT/flink-connector-kinesis-$KINESIS_CONNECTOR_VERSION-$FLINK_VERSION_SHORT.jar /opt/flink/lib

COPY pom.xml .
RUN mkdir ./maven-dependencies
RUN apache-maven-$MAVEN_VERSION/bin/mvn install -Dmaven.repo.local=./maven-dependencies
RUN find ./maven-dependencies -type f -name "*.jar" | xargs -I'{}' cp '{}' /usr/local/lib/python$PYTHON_VERSION_SHORT/site-packages/pyflink/lib
RUN find ./maven-dependencies -type f -name "*.jar" | xargs -I'{}' cp '{}' /opt/flink/lib

ENV CLASSPATH=/opt/flink/lib

RUN rm -rf apache-maven-$MAVEN_VERSION

# copy jobs to flink jobs directory
RUN mkdir -p /opt/flink/pyflink/jobs
COPY flink-jobs/flink_app.py /opt/flink/pyflink/jobs

COPY ./flink-conf.yaml /opt/flink/conf

CMD ["python", "./opt/flink/pyflink/jobs/flink_app.py"]
