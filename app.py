import streamlit as st
import pandas as pd
import os
import time

from database import get_connection, Base
from models import Personagem, Mago, Guerreiro

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="RPG Objeto-Relacional", page_icon="⚔️", layout="wide")

IMG_MAGO = "images/mago.png"
IMG_GUERREIRO = "images/guerreiro.png"

def get_image(path):
    return path if os.path.exists(path) else "https://via.placeholder.com/150?text=Sem+Img"

# Conexão e Sessão
engine, Session = get_connection()
Base.metadata.create_all(engine)
session = Session()

# Inicializa Turno
if 'turno' not in st.session_state:
    st.session_state.turno = 1 

st.title("🛡️ Trabalho de BD: Modelo Objeto-Relacional")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("⚙️ Gerenciar Personagens")
    
    # 1. CRIAR NOVO
    with st.expander("Criar Novo Personagem", expanded=True):
        classe_selecionada = st.radio("Classe:", ["Mago", "Guerreiro"])
        nome_input = st.text_input("Nome:")
        inv_input = st.text_input("Inventário (separe por vírgula):", "Poção, Mapa")
        
        if classe_selecionada == "Mago":
            val_esp = st.number_input("Mana", min_value=10, value=100)
        else:
            val_esp = st.number_input("Força", min_value=10, value=50)
        
        hp_inicial = st.number_input("Saúde Inicial", min_value=10, value=100)

        if st.button("Salvar no Banco"):
            if not nome_input:
                st.error("Nome obrigatório!")
            else:
                lista_itens = [x.strip() for x in inv_input.split(',')]
                if classe_selecionada == "Mago":
                    p = Mago(nome=nome_input, mana=val_esp, saude=hp_inicial, inventario=lista_itens)
                else:
                    p = Guerreiro(nome=nome_input, forca=val_esp, saude=hp_inicial, inventario=lista_itens)
                
                session.add(p)
                session.commit()
                st.success("Criado com sucesso!")
                time.sleep(0.5) # Pequena pausa visual
                st.rerun()

    st.divider()
    
    # 2. REMOVER (CORRIGIDO COM ID)
    with st.expander("Remover Personagem"):
        p_removiveis = session.query(Personagem).all()
        if p_removiveis:
            p_sel = st.selectbox("Remover:", p_removiveis, format_func=lambda x: f"{x.nome} ({x.tipo})")
            
            if st.button("🔥 Apagar"):
                # Busca pelo ID para garantir que o objeto está na sessão atual
                obj_apagar = session.query(Personagem).get(p_sel.id)
                if obj_apagar:
                    session.delete(obj_apagar)
                    session.commit()
                    st.success(f"{p_sel.nome} deletado!")
                    time.sleep(1) # Pausa para ver a mensagem
                    st.rerun()
                else:
                    st.error("Erro ao apagar.")

# --- ÁREA PRINCIPAL ---
tab1, tab2, tab3 = st.tabs(["⚔️ Arena (Turnos)", "📜 Inventários", "💾 Tabelas SQL"])

# === ABA 1: ARENA ===
with tab1:
    st.subheader("Batalha: Ataque vs Defesa")
    st.caption("O dano final será o Ataque menos a Defesa.")
    
    personagens = session.query(Personagem).all()
    
    if len(personagens) < 2:
        st.warning("⚠️ Crie pelo menos 2 personagens.")
    else:
        col_esq, col_meio, col_dir = st.columns([2, 1, 2])
        
        # Seleção Lutador 1
        with col_esq:
            st.markdown("### 🔴 Lutador 1")
            lutador1 = st.selectbox("Selecione:", personagens, key="l1", format_func=lambda p: p.nome)
            st.image(get_image(IMG_MAGO if lutador1.tipo == 'mago' else IMG_GUERREIRO), width=180)
            st.metric("Vida", lutador1.saude)

        # Seleção Lutador 2
        with col_dir:
            st.markdown("### 🔵 Lutador 2")
            opcoes_l2 = [p for p in personagens if p.id != lutador1.id]
            if opcoes_l2:
                lutador2 = st.selectbox("Selecione:", opcoes_l2, key="l2", format_func=lambda p: p.nome)
                st.image(get_image(IMG_MAGO if lutador2.tipo == 'mago' else IMG_GUERREIRO), width=180)
                st.metric("Vida", lutador2.saude)
            else:
                lutador2 = None

        # Indicador de Turno
        with col_meio:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.session_state.turno % 2 != 0:
                seta = "➡️ ATACA ➡️"
                cor = "red"
            else:
                seta = "⬅️ ATACA ⬅️"
                cor = "blue"
            st.markdown(f"<h3 style='text-align:center; color:{cor}'>{seta}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align:center'>Turno: {st.session_state.turno}</p>", unsafe_allow_html=True)

        st.divider()
        
        # LÓGICA DO BOTÃO LUTAR
        if lutador1 and lutador2:
            if st.button("🔥 RODAR TURNO", use_container_width=True):
                
                # 1. Merge (Reconectar à sessão)
                lutador1 = session.merge(lutador1)
                lutador2 = session.merge(lutador2)

                # 2. Definir Papeis
                if st.session_state.turno % 2 != 0:
                    atacante = lutador1
                    defensor = lutador2
                else:
                    atacante = lutador2
                    defensor = lutador1

                # 3. Rolar Dados (Ataque e Defesa)
                val_atk, msg_atk = atacante.atacar()
                val_def, msg_def = defensor.defender()

                # 4. Calcular Dano Real
                dano_final = max(0, val_atk - val_def)
                msg_dano = defensor.receber_dano(dano_final)
                
                session.commit()
                
                # 5. Exibir Resultados
                c1, c2, c3 = st.columns(3)
                c1.info(f"**Ataque:**\n{msg_atk}")
                c2.warning(f"**Defesa:**\n{msg_def}")
                
                if dano_final > 0:
                    c3.error(f"**Resultado:**\n{msg_dano}")
                else:
                    c3.success(f"**Resultado:**\n🛡️ Bloqueio Total!")

                # 6. PAUSA DRAMÁTICA (O que você pediu!)
                with st.spinner('Calculando próximo turno...'):
                    time.sleep(3) 

                # 7. Verificar Fim de Jogo ou Próximo Turno
                if defensor.saude <= 0:
                    st.toast(f"☠️ {defensor.nome} Morreu!", icon="☠️")
                    
                    # Remove do banco com segurança via ID
                    defensor_morto = session.query(Personagem).get(defensor.id)
                    if defensor_morto:
                        session.delete(defensor_morto)
                        session.commit()
                    
                    st.balloons()
                    st.session_state.turno = 1 
                    st.rerun()
                else:
                    st.session_state.turno += 1
                    st.rerun()

            if st.button("Reiniciar Turnos"):
                st.session_state.turno = 1
                st.rerun()

# === ABA 2: INVENTÁRIOS ===
with tab2:
    st.subheader("Fichas Completas")
    lista = session.query(Personagem).all()
    if lista:
        cols = st.columns(3)
        for i, p in enumerate(lista):
            with cols[i%3].container(border=True):
                st.image(get_image(IMG_MAGO if p.tipo == 'mago' else IMG_GUERREIRO))
                st.markdown(f"**{p.nome}** ({p.tipo})")
                st.progress(min(p.saude, 100)/100, f"HP: {p.saude}")
                st.code(p.inventario)

# === ABA 3: TABELAS ===
with tab3:
    st.subheader("Banco de Dados")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Personagens (Pai)**")
        st.dataframe(pd.read_sql("SELECT * FROM personagens", engine), hide_index=True)
    with c2:
        st.markdown("**Classes Filhas**")
        st.dataframe(pd.read_sql("SELECT * FROM magos", engine), hide_index=True)
        st.dataframe(pd.read_sql("SELECT * FROM guerreiros", engine), hide_index=True)