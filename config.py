import os

# Hostname ko .i.aivencloud.com ke sath sahi kar diya hai
HOST = os.getenv("DB_HOST", "hotel-db-udayprajapati1625-6ae3.i.aivencloud.com")
USER = os.getenv("DB_USER", "avnadmin")
PASSWORD = os.getenv("DB_PASSWORD", "") # Aiven dashboard wala password yahan likhein
DATABASE = os.getenv("DB_NAME", "defaultdb")  
PORT = int(os.getenv("DB_PORT", 21216))
