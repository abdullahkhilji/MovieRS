# Use an official Python runtime as a parent image
FROM python:3.6-alpine

RUN adduser -D moviers

# Set the working directory to /app
WORKDIR /home/app

# Copy the current directory contents into the container at /app
COPY docker_content/. /home/app

COPY boot.sh /home/app/


RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.6/main' >> /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.6/community' >> /etc/apk/repositories


RUN apk update
RUN apk add gnupg mongodb=3.4.4-r0 

################## BEGIN INSTALLATION ######################
# Install MongoDB Following the Instructions at MongoDB Docs
# Ref: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

# Add the package verification key
#RUN apt-key adv --no-tty --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

# Add MongoDB to the repository sources list
#RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/mongodb.list

# Update the repository sources list once more
#RUN apt-get update

# Install MongoDB package (.deb)
#RUN apt-get -y --allow-unauthenticated install mongodb-10gen

# Create the default data directory
RUN mkdir -p /data/db

##################### INSTALLATION END #####################

FROM mongo
COPY movies_174_new.json /movies_174_new.json
COPY movies_174_new.json /movies_174_new.json
CMD mongoimport --host mongodb --db moviers --collection movies_174_new --type json --file /movies_174_new.json --jsonArray
CMD mongoimport --host mongodb --db moviers --collection user_ratings_4570_new --type json --file /user_ratings_4570_new.json --jsonArray


RUN chmod +x /home/app/boot.sh

ENV FLASK_APP moviers.py

RUN chown -R moviers:moviers ./
USER moviers



EXPOSE 5000
ENTRYPOINT ["./boot.sh"]

