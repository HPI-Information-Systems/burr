FROM openjdk:11-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-setuptools python3-wheel \
    git \
    ant \
    curl \
    postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
WORKDIR /experiment
COPY requirements.txt /experiment
RUN pip3 install --no-cache-dir -r requirements.txt
RUN git clone https://github.com/d2rq/d2rq.git /experiment/d2rq

RUN mkdir -p /experiment/d2rq/lib/db-drivers
RUN curl -L -o /experiment/d2rq/lib/db-drivers/postgresql-42.7.4.jar \
    https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar

RUN sed -i 's|<classpathentry kind="lib" path="lib/db-drivers/postgresql-9.2-1003.jdbc4.jar"/>|<classpathentry kind="lib" path="lib/db-drivers/postgresql-42.7.4.jar"/>|' /experiment/d2rq/.classpath
RUN sed -i 's|source="1.5"|source="1.8"|g' /experiment/d2rq/build.xml
RUN sed -i 's|target="1.5"|target="1.8"|g' /experiment/d2rq/build.xml
RUN cd ./d2rq && ant jar && cd ..

#COPY ./ /experiment
ADD ./ /experiment


RUN pip3 install -e .
