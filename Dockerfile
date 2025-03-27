FROM python:3.9
WORKDIR /app
COPY app.py db.py requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]