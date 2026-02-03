FROM python:3.11-slim

WORKDIR /app

# Copy the entire project context
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r backend/app/requirements.txt

# Expose the port (Render often uses 10000, but 8000 is fine if configured)
EXPOSE 8000

# Run the application
# We use the same module path as the local script to ensure consistency
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
