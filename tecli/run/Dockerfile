ARG  ENVIRONMENT
ARG  ENVIRONMENT_VERSION
FROM conservationinternational/${ENVIRONMENT}:${ENVIRONMENT_VERSION}

COPY src /project/gefcore/script
COPY requirements.txt /project/requirements.txt

RUN pip install --no-cache-dir -r /project/requirements.txt

USER $USER
