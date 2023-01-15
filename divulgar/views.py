from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import render, redirect

from adotar.models import PedidoAdocao
from django.views.decorators.csrf import csrf_exempt
from .models import Tag, Raca, Pet
from django.http import HttpResponse, JsonResponse

#Mostrar somente se tiver logad
@login_required
def novo_pet(request):
    if request.method == "GET":
        #Quando logar, ja retornar todos os objetos cadastrado
        tags = Tag.objects.all()
        racas = Raca.objects.all()
        return render(request, 'novo_pet.html', {'tags': tags, 'racas': racas})
    #Quando enviar o form
    elif request.method == "POST":
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        #O input vai fornecer varias informações para receber os dados como uma lista, por isso o getlist
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')

        # TODO: Validar dados
        # TODO: Usar API dos correiros
        # TODO: Adicionar mensagens de erros

        # Primeiro salva os dados do Pet
        #Model = view
        pet = Pet(
            usuario=request.user,
            foto=foto, nome=nome,
            descricao=descricao,
            estado=estado,
            cidade=cidade,
            telefone=telefone,
            raca_id=raca,
        )
        pet.save()

        # Primeiro salvar o pet e depois adiciona as tag, pois e um many to many

        # Depois salva as tags relacionadas ao Pet
        for tag_id in tags:
            tag = Tag.objects.get(id=tag_id)
            pet.tags.add(tag)
        pet.save()

        return redirect('/divulgar/seus_pets')


@login_required
def seus_pets(request):
    if request.method == "GET":
        pets = Pet.objects.filter(usuario=request.user)
        return render(request, 'seus_pets.html', {'pets': pets})


@login_required
def remover_pet(request, id):
    pet = Pet.objects.get(id=id)

    if not pet.usuario == request.user:
        messages.add_message(request, constants.ERROR, 'Esse pet não é seu! hehehe')
        return redirect('/divulgar/seus_pets')

    elif pet.usuario not in request.user:
        messages.add_message(request, constants.ERROR, 'Esse pet não existe!')
        return redirect('/divulgar/seus_pets')

    pet.delete()

    messages.add_message(request, constants.SUCCESS, 'Removido com sucesso.')
    return redirect('/divulgar/seus_pets')


@login_required
def ver_pet(request, id):
    if request.method == "GET":
        pet = Pet.objects.get(id=id)
        # TODO: Colocar hover nas tag
        return render(request,'ver_pet.html',{'pet':pet})

#Ver os pedidos de adoção
@login_required
def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos = PedidoAdocao.objects.filter(usuario=request.user).filter(status="AG")
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos})

@login_required
def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html')


@csrf_exempt
def api_adocoes_por_raca(request):
    racas = Raca.objects.all()

    qtd_adocoes = []
    for raca in racas:
        adocoes = PedidoAdocao.objects.filter(pet__raca=raca).filter(status='AP').count()

        qtd_adocoes.append(adocoes)


    racas = [raca.raca for raca in racas]
    data = {'qtd_adocoes': qtd_adocoes,
            'labels': racas}

    return JsonResponse(data)






