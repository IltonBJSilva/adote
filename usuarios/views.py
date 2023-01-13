from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.shortcuts import render, redirect


#Função para cadastrar no sistema
def cadastro(request):
    if request.method == "GET":
        #Caso usuario esteja autenticado, dar um redirect
        if request.user.is_authenticated:
            return redirect('/divulgar/novo_pet')

        return render(request, 'cadastro.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if (len(nome.strip()) == 0
            or len(email.strip()) == 0
            or len(senha.strip()) == 0
            or len(confirmar_senha.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return render(request, 'cadastro.html')

        if senha != confirmar_senha:
            messages.add_message(request, constants.ERROR, 'Digite duas senhas iguais')
            return render(request, 'cadastro.html')

        #Criar Usuario
        try:
            user = User.objects.create_user(
                username=nome,
                email=email,
                password=senha,
            )

            messages.add_message(request, constants.SUCCESS, 'Usuário criado com sucesso')
            return render(request, 'cadastro.html')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return render(request, 'cadastro.html')


#Função para logar no sistema
def logar(request):
    if request.method == "GET":
        #caso o usuario estreja autenticado, logar dando redirect a esse endereço
        if request.user.is_authenticated:
            return redirect('/divulgar/novo_pet')

        return render(request, 'login.html')
    elif request.method == "POST":
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')

        #autenticar no banco de dados
        user = authenticate(username=nome, password=senha)
        if user is not None:
            login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Usuário logado com sucesso')
            return redirect('/divulgar/novo_pet')

        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
            return render(request, 'login.html')


def sair(request):
    #Deslogar o usuario
    logout(request)
    return redirect('/auth/login')
