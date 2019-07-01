FROM python:3.7

WORKDIR /app
COPY . .
RUN pip install -r req.txt

ENTRYPOINT ["bash", "docker-entrypoint.sh"]
