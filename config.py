import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_API_BASE_URL = "https://api.github.com" #github rest api bağlantısının alınması
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")# ayarlar kısmından oluşturup config.py dosyasında 
    #tanıtacağınız personal access key iniz
    SECRET_KEY = os.getenv("SECRET_KEY")#flash mesajları formlar için secret key

