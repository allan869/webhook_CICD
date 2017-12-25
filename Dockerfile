FROM reg.cctv.cn/library/python:3.6-alpine-utc8
COPY requirements.txt /src/

WORKDIR /src

RUN pip install -r requirements.txt

COPY . /src/
ENTRYPOINT ["/src/docker-entrypoint.sh"]
CMD ["python", "runserver.py"]
