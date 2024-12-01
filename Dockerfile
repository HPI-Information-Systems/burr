FROM python:3.9-slim
WORKDIR ./experiment
COPY ./ /experiment
RUN pip3 install -r requirements.txt
CMD python3 /experiment/evaluator/experimenter/experiment_script.py
# docker build -t 'IMAGE_NAME' .
# docker run -v ./result:/results IMAGE_NAME --scenario BLUB --tag test wandb