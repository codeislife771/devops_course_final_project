FROM alpine:3.22.0
RUN apk update 
RUN apk add python3 py3-pip

WORKDIR /app

RUN python3 -m venv venv
COPY requirements.txt .
RUN ./venv/bin/pip install -r requirements.txt

# Copy application files
COPY  templates/ templates/
COPY app.py .
COPY tasks.json  .

# Run using the venv's Python
CMD [ "./venv/bin/python3", "app.py" ]
