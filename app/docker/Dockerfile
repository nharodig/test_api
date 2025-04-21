FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# requirements python
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt


RUN apt-get update \
    && apt-get install -y \
        netcat-openbsd
# copy all the code
COPY . .

EXPOSE 3000

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
