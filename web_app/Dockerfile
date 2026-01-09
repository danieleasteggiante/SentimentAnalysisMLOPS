FROM python:3.10.19-trixie
WORKDIR /usr/local/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

RUN useradd app
USER app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]