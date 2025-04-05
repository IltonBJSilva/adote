# 🐾 ADO.TE – Plataforma para Adoção de Animais

Aplicação desenvolvida com **Python** e **Django 4.1** para conectar pessoas que querem doar pets com quem deseja adotar um novo amigo.

---

## 🚀 Funcionalidades

- ✅ Cadastro e autenticação de usuários
- 🐶 Cadastro de animais para doação
- 🔍 Busca e filtragem de pets por cidade e raça
- 📥 Solicitação de adoção com controle de status
- 📊 Dashboard com dados estatísticos
- ✏️ Edição e remoção de pets

---

## 🛠️ Tecnologias e boas práticas

- Python 3.12
- Django 4.1
- SQLite
- Bootstrap 5
- Templates com HTML + CSS customizado
- Arquitetura MVT (Model-View-Template)

---

## 🖼️ Interfaces do Sistema

### 🔐 Login do Usuário

![Login](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/tela_login.png?raw=true)

### 📝 Cadastro de Usuário

![Cadastro](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/tela_cadastro.png?raw=true)

### 🐕 Cadastro de Pet

![Cadastro Pet](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/tela_divulgar.png?raw=true)

### 🗃️ Meus Pets

![Meus Pets](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/tela_meus_pets.png?raw=true)

### 📄 Informações do Pet

![Info Pet](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/tela_info_pet.png?raw=true)

### 📝 Edição de Pet

![Editar Pet](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/tela_editar.png?raw=true)

### 📥 Solicitações de Adoção

![Solicitações](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/tela_solicitacoes.png?raw=true)

### 📈 Dashboard

![Dashboard](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/tela_dashboard.png?raw=true)

### 🐾 Listagem de Pets para Adoção

![Listagem](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/tela_listagem.png?raw=true)

---

## ⚙️ Como rodar o projeto

### 1. Crie um ambiente virtual


```bash
python -m venv env
env\Scripts\activate.bat  # Windows
```


### 2. Instale os requisitos

```bash
pip install -r requirements.txt
```

### 3. Realize as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Crie o superusuário


```bash
python manage.py createsuperuser
```

### 5. Rode o servidor

```bash
python manage.py runserver
```

---

## 🧪 Apps Django utilizados

- `Usuarios`: gerenciamento de login, cadastro e autenticação
- `Divulgar`: CRUD dos pets e lógica das adoções
- `adotar`: listagem pública e controle de solicitações

---

## 📦 Estrutura de diretórios

```bash
adote/
├── adote/
├── divulgar/
├── usuarios/
├── static/
│   └── readme/
│       └── (prints das telas do sistema)
├── templates/
└── manage.py
```

---

## 💡 Autor

Desenvolvido com 💜 por **Ilton Batista**.
