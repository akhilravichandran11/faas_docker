FROM alpine:3.1

# Update
RUN apk add --update python py-pip

# Install app dependencies
RUN pip install Flask

# Bundle app source
COPY create_user.py /src/create_user.py

CMD ["python", "/src/create_user.py"]
