FROM python-hadoop

WORKDIR /usr/schema
ENV JAVA_HOME /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.222.b10-1.el7_7.x86_64

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .

USER root
ENV HADOOP_USER_NAME root

ENTRYPOINT ["./entrypoint.sh"]
