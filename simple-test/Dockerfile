# create dockerfile to run python script
# Use an official Python runtime as the base image
FROM ubuntu:20.04

# Set the working directory in the container
WORKDIR /app
RUN apt-get update && apt-get install -y ca-certificates
# Copy the requirements file to the working directory
COPY nak .


# start entrypoint.sh
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]