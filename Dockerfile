# Use an official Python runtime as a parent image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY docker_content/. /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get --yes --force-yes update
RUN apt-get --yes --force-yes install gnupg2

################## BEGIN INSTALLATION ######################
# Install MongoDB Following the Instructions at MongoDB Docs
# Ref: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/

# Add the package verification key
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10

# Add MongoDB to the repository sources list
RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | tee /etc/apt/sources.list.d/mongodb.list

# Update the repository sources list once more
RUN apt-get update

# Install MongoDB package (.deb)
RUN apt-get --yes --force-yes install -y mongodb-10gen

# Create the default data directory
RUN mkdir -p /data/db

##################### INSTALLATION END #####################

FROM mongo
COPY movies_174_new.json /movies_174_new.json
COPY movies_174_new.json /movies_174_new.json
CMD mongoimport --host mongodb --db moviers --collection movies_174_new --type json --file /movies_174_new.json --jsonArray
CMD mongoimport --host mongodb --db moviers --collection user_ratings_4570_new --type json --file /user_ratings_4570_new.json --jsonArray


# make port 5000 available to the world outside
EXPOSE 5000

# Run app.py when the container launches
ENTRYPOINT ["python"]
CMD ["deploy.py"]
