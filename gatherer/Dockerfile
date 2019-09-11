FROM centos:7

RUN yum update -y \
    && yum install -y https://centos7.iuscommunity.org/ius-release.rpm \
    && yum install -y java-1.8.0-openjdk.x86_64 wget python36u python36u-libs python36u-devel python36u-pip \
    && yum install -y which gcc gcc-c++

USER root
ENV JAVA_HOME /usr/lib/jvm/jre-1.8.0
ENV HADOOP_USER hdfs
ENV HADOOP_PREFIX /usr/local/hadoop
ENV HADOOP_COMMON_HOME /usr/local/hadoop
ENV HADOOP_HDFS_HOME /usr/local/hadoop
ENV HADOOP_CONF_DIR /opt/cluster-conf

RUN wget -q -O - http://apache.mirrors.pair.com/hadoop/common/hadoop-2.7.7/hadoop-2.7.7.tar.gz | tar -xzf - -C /usr/local \
&& ln -s /usr/local/hadoop-2.7.7 /usr/local/hadoop \
&& groupadd -r hadoop \
&& groupadd -r $HADOOP_USER && useradd -r -g $HADOOP_USER -G hadoop $HADOOP_USER

RUN mkdir -p $HADOOP_CONF_DIR
RUN chown -R $HADOOP_USER:hadoop /usr/local/hadoop-2.7.7 && chmod -R 775 $HADOOP_CONF_DIR

ENV HADOOP_USER_NAME $HADOOP_USER
ENV PATH="${HADOOP_PREFIX}/bin:${PATH}"

RUN ln -s /usr/bin/pip3.6 /bin/pip
RUN rm /usr/bin/python
RUN ln -s /usr/bin/python3.6 /usr/bin/python

RUN pip install -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]
