FROM python:3.9

# Inštalácia LibreOffice (potrebná na konverziu DOCX → PDF)
RUN apt-get update && apt-get install -y libreoffice

# Nastavenie pracovného adresára
WORKDIR /app

# Kopírovanie súborov
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Spustenie aplikácie
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "convert:app"]
