import os

class Config:
    SECRET_KEY = 'supersecretkey123'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///script-ddl-loja_online.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PERMANENT_SESSION_LIFETIME = 1200 # 20 minutos
    
    ITEMS_PER_PAGE = 10



