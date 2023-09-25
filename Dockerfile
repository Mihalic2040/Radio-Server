# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set environment variables
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY req.txt /app/




# set display port to avoid crash
RUN apt-get update && apt-get install -y screen openssl


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r req.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose port 5000 for Flask to listen on
EXPOSE 5000

# Define the command to run your application
CMD ["bash", "run.sh"]
