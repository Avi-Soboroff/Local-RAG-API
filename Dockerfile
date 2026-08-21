# First, download the python version the RAG API uses
FROM python:3.13-slim

# Create a folder called app inside the container and move into it
WORKDIR /app

# copy all the dependencies used in this project into this container, the /app folder, and install them
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the project files into the /app folder
COPY . .

# When the container is turned on, run the server command and listen for incoming external traffic from outside the container
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]