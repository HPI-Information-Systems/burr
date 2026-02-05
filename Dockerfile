FROM nvidia/cuda:12.2.0-base-ubuntu22.04

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11 python3-pip postgresql-client git ant curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y python3-dev
RUN export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

RUN apt-get update && apt-get install -y build-essential



# RUN apt-get update && apt-get install -y --no-install-recommends \
# #    python3 python3-pip python3-setuptools python3-wheel \
#     git \
#     ant \
#     curl \
#     postgresql-client && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*
RUN apt-get update \
 && apt-get install -y --no-install-recommends openjdk-11-jdk-headless \
 && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1
WORKDIR /experiment
COPY requirements.txt /experiment
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install datasets trl

RUN git clone https://github.com/Lasklu/d2rq /experiment/d2rq

RUN mkdir -p /experiment/d2rq/lib/db-drivers
RUN curl -L -o /experiment/d2rq/lib/db-drivers/postgresql-42.7.4.jar \
    https://repo1.maven.org/maven2/org/postgresql/postgresql/42.7.4/postgresql-42.7.4.jar

RUN sed -i 's|<classpathentry kind="lib" path="lib/db-drivers/postgresql-9.2-1003.jdbc4.jar"/>|<classpathentry kind="lib" path="lib/db-drivers/postgresql-42.7.4.jar"/>|' /experiment/d2rq/.classpath
RUN sed -i 's|source="1.5"|source="1.8"|g' /experiment/d2rq/build.xml
RUN sed -i 's|target="1.5"|target="1.8"|g' /experiment/d2rq/build.xml
RUN cat ./d2rq/build.xml | grep javac
RUN cd ./d2rq && ant jar && cd ..
#RUN cd ./d2rq && ant -Dcompile.encoding=UTF-8 clean jar

ADD ./ /experiment
# RUN pip3 install peft
# RUN pip install transformers==4.51.2
# RUN pip install sentence_transformers==3.4.1
# RUN pip install pytorch_lightning umap-learn scipy scipy scikit-learn networkx matplotlib seaborn plotly
RUN cd /experiment
RUN pip3 install -e .
