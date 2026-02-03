# database.py
import streamlit as st 
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

Base = declarative_base()

# O decorador @st.cache_resource garante que o Streamlit
# execute essa função apenas UMA VEZ e reaproveite a conexão
# nas próximas interações (cliques de botão, recargas, etc).
@st.cache_resource
def get_connection():
    # Cria o banco SQLite
    engine = create_engine('sqlite:///rpg_battle.db', connect_args={'check_same_thread': False})
    
    # expire_on_commit=False é CRUCIAL para o cache funcionar bem com SQLAlchemy
    Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
    
    return engine, Session