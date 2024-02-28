# Aplicação usando Python e Django 4.1

## ADO.TE 

Aplicação que conecta pessoas que possuem animais para doação com interessadas em ter um animal de estimação.

Desenvolvida uma aplicação completa para adoção de animais.

## Tecnologias e práticas utilizadas

- Python
- Django 4.1
- SQLite
- Arquitetura MVT

## Funcionalidades

- Autenticação e Cadastro de Usuários
- Listagem, Cadastro e Remoção de Pets
- Listagem e Busca de Pets para adoção

## Login de Usuario

![alt text](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/logar.png?raw=true)

## Cadastro de Usuario

![alt text](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/cadastre-se.png?raw=true)

## Cadastro de Pet

![alt text](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/novo_pet.png?raw=true)

## Meus Pet

![alt text](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/seus_pets.png?raw=true)

## Lista de Pet

![alt text](https://github.com/IltonBJSilva/adote/blob/main/templates/static/readme/adote.png?raw=true)

## Comandos

### virtualenv (windows)

```
python -m venv env
env\Scripts\activate.bat
env\Scripts\deactivate.bat
```

### Instalar bibliotecas, gravar/instalar requerimentos

```
(env) pip install Django
(env) pip install Pillow

(env) pip freeze > requirements.txt
(env) pip install -r requirements.txt
```

### Criar projeto

```
(env) django-admin startproject adote .
```

### Criar super user (Django Administration)

```
(env) python manage.py createsuperuser
```

### Criar apps

```
(env) python manage.py startapp usuarios
(env) python manage.py startapp divulgar
```

### Migrations

```
(env) python manage.py makemigrations
(env) python manage.py migrate
```

### Executar projeto

```
(env) python manage.py runserver
```
