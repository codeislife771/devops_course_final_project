FROM alpine:3.22
RUN apk update 
RUN apk add python3 py3-pip

WORKDIR /app

RUN python3 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application files
COPY  templates/ templates/
COPY app.py .
COPY test_tasks.py .
COPY tasks.json  .

# Run using the venv's Pylsthon
CMD [ "python3", "app.py" ]
