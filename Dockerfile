# Use official Python base image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies and PDM
RUN pip install pdm

# Copy only the PDM files first to leverage Docker caching
COPY pdm.lock pyproject.toml ./

# Install dependencies using PDM
RUN pdm install

# Copy the entire project into the container
COPY . .

# Perform migrations
RUN pdm run alembic upgrade head

# Expose the application port
EXPOSE 8000

# Run the FastAPI server
CMD ["pdm", "run", "python", "main.py"]
