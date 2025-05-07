FROM ubuntu:25.04

WORKDIR /yt-client
RUN apt-get update && \
    apt-get install python3 python3-pip -y

COPY requirements.txt ./
RUN pip3 install -r requirements.txt --break-system-packages
COPY server.py ./

EXPOSE 6688
ENTRYPOINT ["fastapi"]
CMD ["run", "server.py", "--host", "0.0.0.0", "--port", "6688"]
