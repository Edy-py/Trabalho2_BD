# 🛡️ Trabalho de BD: Modelo Objeto-Relacional

Este projeto consiste numa aplicação de combate RPG interativa desenvolvida para demonstrar a implementação prática de um **Modelo Objeto-Relacional (ORM)**. A aplicação utiliza Python, SQLAlchemy e Streamlit para mapear conceitos de orientação a objetos para um banco de dados relacional.

O objetivo central é ilustrar como a herança e o polimorfismo de classes (como Guerreiros e Magos) são geridos dentro de tabelas SQL.

## 🏗️ Estrutura do Projeto

* **`app.py`**: Interface principal desenvolvida em Streamlit. Gere os turnos da batalha, a criação, visualização de tabelas SQL e a remoção de personagens.
* **`models.py`**: Define as classes de domínio (`Personagem`, `Mago` e `Guerreiro`) utilizando o mapeamento polimórfico do SQLAlchemy.
* **`database.py`**: Configura a ligação ao banco de dados SQLite e a gestão de sessões via `scoped_session`.
* **`requirements.txt`**: Lista as dependências necessárias para a execução do projeto: `pandas`, `SQLAlchemy` e `streamlit`.
* **`images/`**: Pasta contendo os recursos visuais para Magos e Guerreiros.

---

## 🛠️ Configuração e Instalação

Siga os passos abaixo para preparar o seu ambiente local:

### 1. Criar um Ambiente Virtual (venv)
O ambiente virtual isola as bibliotecas do projeto para evitar conflitos.

* **Linux / macOS:**
    ```bash
    python3 -m venv venv
    ```
* **Windows:**
    ```bash
    python -m venv venv
    ```

### 2. Ativar o Ambiente Virtual

* **Linux / macOS:**
    ```bash
    source venv/bin/activate
    ```
* **Windows:**
    ```bash
    venv\Scripts\activate
    ```

### 3. Instalar as Dependências
Com o ambiente ativado, instale os pacotes necessários:
```bash
pip install -r requirements.txt
```

### 4. 🚀 Como Executar
Para iniciar a aplicação, utilize o comando do Streamlit diretamente no seu terminal:

 ```bash
    streamlit run app.py
 ```
A interface será aberta automaticamente no seu navegador padrão (geralmente no endereço `http://localhost:8501`).

### 📜 Detalhes do Modelo Objeto-Relacional

**Herança de Tabela:** A classe `Personagem` serve como base (tabela pai), enquanto `Mago` e `Guerreiro` possuem as suas próprias tabelas que se relacionam via chave estrangeira com a tabela principal.

**Polimorfismo:** O sistema utiliza a coluna `tipo` para determinar qual classe instanciar, permitindo que cada classe tenha métodos específicos de `atacar()` e `defender()`.

**Armazenamento JSON:** O inventário dos personagens é guardado utilizando o tipo `JSON` diretamente no SQLite, demonstrando flexibilidade no armazenamento de coleções.

**Persistência:** Todas as ações (criação, dano sofrido e morte) são persistidas em tempo real no ficheiro de base de dados `rpg_battle.db`.
