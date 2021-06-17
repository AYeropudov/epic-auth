FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /opt/services/chat
#VOLUME ["/opt/services/flaskapp/src"]
# We copy the requirements.txt file first to avoid cache invalidations
COPY requirements.txt /opt/services/chat
WORKDIR /opt/services/chat
RUN pip install -r requirements.txt
COPY . /opt/services/chat
CMD ["python", "main.py"]