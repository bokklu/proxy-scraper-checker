FROM python:3.8-slim

RUN apt-get update && \
	apt-get install -y --no-install-recommends gcc libc-dev make

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r docker-scripts/requirements.txt

CMD [ "python", "src/main.py" ]