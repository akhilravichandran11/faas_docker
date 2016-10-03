#using tiangolos ubuntu,nginx,wsgi and flask image
FROM tiangolo/uwsgi-nginx:python2.7
#Adding requirements to app directory and installing
ADD requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

#Add app configuration to Nginx
COPY nginx.conf /etc/nginx/conf.d/

#Copy our code(app) folder to container app folder
COPY ./app /app