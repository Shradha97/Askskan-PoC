FROM python:3.9-slim

ARG INDEX_URL
ENV PIP_EXTRA_INDEX_URL=$INDEX_URL
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y gcc g++
WORKDIR /
COPY /askskan/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt
COPY . /askskan
EXPOSE 7860
RUN chmod +x /askskan/askskan/startup.sh
CMD ["/askskan/askskan/startup.sh", "-clean", "-table", "--stream", "--auth", "--rootpath", "/askskan"]
