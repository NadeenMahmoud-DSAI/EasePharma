# 1. Use Python 3.10 as the base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the source code folder
COPY src/ src/

# 5. Create the data directory (to ensure it exists)
RUN mkdir -p src/data

# 6. Expose Port 5000 (Standard for Flask)
EXPOSE 5000

# 7. Run the application
# We use host=0.0.0.0 so the container accepts outside connections
CMD ["python", "src/run.py"]