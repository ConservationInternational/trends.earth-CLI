FROM conservationinternational/trends.earth-environment

COPY requirements.txt /project/requirements.txt
RUN pip install -r /project/requirements.txt

COPY src /project/gefcore/script

USER $USER
