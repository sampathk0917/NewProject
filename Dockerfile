FROM python:alpine3.16
RUN file="$(python3 --version)" && echo $file
RUN pip3 install requests python-dotenv
COPY server.py server.py 
COPY get_forex_data.py get_forex_data.py
COPY server.py server.py
COPY .env .env
RUN  python3 get_forex_data.py
EXPOSE 8000
ENTRYPOINT ["python3", "server.py"]