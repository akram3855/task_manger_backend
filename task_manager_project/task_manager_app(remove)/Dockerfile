# Use a lightweight Python base image. The version matches the packages you're using.
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Set environment variables to optimize Python's behavior in Docker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the requirements file and install the dependencies
# This is a key step where Docker reads your requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project's code into the container
COPY . .

# Expose the port that the Django development server will run on
EXPOSE 8000

# This is the command to start your application.
# The project name has been updated to 'task_manager_project'.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "task_manager_project.wsgi:application"]