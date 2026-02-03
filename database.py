# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

Base = declarative_base()

def get_connection():
    # Cria o banco SQLite
    engine = create_engine('sqlite:///rpg_battle.db', connect_args={'check_same_thread': False})
    
    # expire_on_commit=False é CRUCIAL para o Streamlit não perder os dados do objeto
    Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
    
    return engine, Session