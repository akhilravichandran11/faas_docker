FROM python:2.7
ADD util.py /
ADD app.py /
RUN pip install requests
CMD [ "python" , "-u", "./app.py" ]