# models.py
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from database import Base
import random

# --- CLASSE PAI ---
class Personagem(Base):
    __tablename__ = 'personagens'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    tipo = Column(String(20))
    saude = Column(Integer, default=100)
    inventario = Column(JSON, default=[]) 
    
    __mapper_args__ = {
        'polymorphic_identity': 'personagem',
        'polymorphic_on': tipo
    }

    def receber_dano(self, dano):
        self.saude -= dano
        return f"❤️ {self.nome} perdeu {dano} de vida! (Restante: {self.saude})"

# --- CLASSES FILHAS ---
class Mago(Personagem):
    __tablename__ = 'magos'
    id = Column(Integer, ForeignKey('personagens.id'), primary_key=True)
    mana = Column(Integer)

    __mapper_args__ = {'polymorphic_identity': 'mago'}

    def atacar(self):
        dano = random.randint(10, self.mana // 2)
        return dano, f"✨ {self.nome} lança Bola de Fogo! (Poder: {dano})"

    def defender(self):
        # Mago defende usando Mana (Barreira Mágica)
        bloqueio = random.randint(1, self.mana // 3)
        return bloqueio, f"🛡️ {self.nome} ergue Barreira Mágica! (Defesa: {bloqueio})"

class Guerreiro(Personagem):
    __tablename__ = 'guerreiros'
    id = Column(Integer, ForeignKey('personagens.id'), primary_key=True)
    forca = Column(Integer)

    __mapper_args__ = {'polymorphic_identity': 'guerreiro'}

    def atacar(self):
        dano = random.randint(5, self.forca)
        return dano, f"⚔️ {self.nome} golpeia com Espada! (Poder: {dano})"

    def defender(self):
        # Guerreiro defende usando Força (Bloqueio com Escudo)
        bloqueio = random.randint(1, self.forca // 2)
        return bloqueio, f"🛡️ {self.nome} bloqueia com Escudo! (Defesa: {bloqueio})"