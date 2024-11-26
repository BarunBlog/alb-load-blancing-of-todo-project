FROM python:3.10-alpine

RUN apk update && apk add --no-cache \
    make


# Create and set the working directory inside the container
WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

# Copy the sh file to the docker
COPY run_web.sh /run_web.sh

# converted it to executable
RUN chmod +x /run_web.sh

# EXPOSE & CMD instructions are runtime directives, so they don't create any layer during build process
# Expose the port that app will run on
EXPOSE 8000

# Run the shell file to run the server
CMD ["sh", "./run_web.sh"]