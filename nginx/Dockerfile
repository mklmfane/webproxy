# Dockerfile-nginx
FROM nginx:latest

# Nginx will listen on this port
EXPOSE 80 443 8080

# Remove the default config file that  includes /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-available/default
RUN rm /etc/nginx/nginx.conf

# We copy the requirements file in order to install Python dependencies
COPY default /etc/nginx/sites-available/
COPY default /etc/nginx/sites-enabled/
COPY nginx.conf /etc/nginx/


EXPOSE 80 8080 443

RUN nginx -s reload
RUN sudo /etc/init.d/nginx restart
