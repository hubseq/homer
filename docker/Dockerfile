# Use miniconda image base from Dockerhub
FROM continuumio/miniconda3

# Metadata
LABEL container.base.image = "miniconda3:python3.9"
LABEL software.name = "homer"

# Install system packages and AWS CLI
RUN apt-get -y update && \
    apt-get -y install python3-pip zip unzip
RUN pip install awscli boto3
# RUN conda install -c bioconda homer

# install homer
RUN mkdir /homer
COPY homer/ /homer/
ENV PATH="/homer/bin/:/homer/:$PATH"
WORKDIR /

# copy relevant scripts to root dir
RUN mkdir -p global_utils/src
COPY src/run_main.py /
COPY src/global_utils/src/module_utils.py /global_utils/src/
COPY src/global_utils/src/file_utils.py /global_utils/src/
COPY src/global_utils/src/global_keys.py /global_utils/src/
COPY src/global_utils/src/aws_s3_utils.py /global_utils/src/
ENV PATH="/usr/local/bin/:$PATH"

ENTRYPOINT ["python","/run_main.py"] 
