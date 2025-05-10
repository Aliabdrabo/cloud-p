# Step 1: Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Step 2: Set the working directory inside the container
WORKDIR /app
# Step 3: Copy the requirements.txt file into the container
COPY requirements.txt /app/
# Step 4: Install the dependencies from the requirements.txt file
RUN pip install --no-cache-dir -r requirements.txt
# Step 5: Copy the rest of the application code into the container
COPY . /app/
# Step 6: Expose the port that Flask will run on
EXPOSE 5000
# Step 7: Set the environment variable to make Flask run in production mode
ENV FLASK_ENV=production
ENV FLASK_APP=infrastructure.api.app
# Step 8: Define the command to run the Flask application
CMD ["gunicorn", "--bind=0.0.0.0:5000", "infrastructure.api.app:app"]

