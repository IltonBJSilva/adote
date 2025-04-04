from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import PetForm

from .models import Tag, Raca, Pet
from adotar.models import PedidoAdocao




@login_required
def novo_pet(request):
    if request.method == "GET":
        tags = Tag.objects.all()
        racas = Raca.objects.all()
        return render(request, 'novo_pet.html', {'tags': tags, 'racas': racas})

    elif request.method == "POST":
        foto = request.FILES.get('foto')
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        estado = request.POST.get('estado')
        cidade = request.POST.get('cidade')
        telefone = request.POST.get('telefone')
        tags = request.POST.getlist('tags')
        raca = request.POST.get('raca')

        pet = Pet(
            usuario=request.user,
            foto=foto,
            nome=nome,
            descricao=descricao,
            estado=estado,
            cidade=cidade,
            telefone=telefone,
            raca_id=raca,
        )
        pet.save()

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
    try:
        pet = Pet.objects.get(id=id)
    except Pet.DoesNotExist:
        messages.add_message(request, constants.ERROR, 'Esse pet não existe!')
        return redirect('/divulgar/seus_pets')

    if pet.usuario != request.user:
        messages.add_message(request, constants.ERROR, 'Esse pet não é seu!')
        return redirect('/divulgar/seus_pets')

    PedidoAdocao.objects.filter(pet=pet).delete()

    pet.delete()
    messages.add_message(request, constants.SUCCESS, 'Pet removido com sucesso.')
    return redirect('/divulgar/seus_pets')


@login_required
def ver_pet(request, id):
    try:
        pet = Pet.objects.get(id=id)
    except Pet.DoesNotExist:
        messages.add_message(request, constants.ERROR, 'Pet não encontrado.')
        return redirect('/')

    return render(request, 'ver_pet.html', {'pet': pet})


@login_required
def ver_pedido_adocao(request):
    if request.method == "GET":
        pedidos_como_dono = PedidoAdocao.objects.filter(pet__usuario=request.user, status="AG")
        pedidos_como_solicitante = PedidoAdocao.objects.filter(usuario=request.user, status="AG")
        pedidos = pedidos_como_dono | pedidos_como_solicitante
        return render(request, 'ver_pedido_adocao.html', {'pedidos': pedidos.distinct()})


@login_required
def dashboard(request):
    if request.method == "GET":
        return render(request, 'dashboard.html')


@csrf_exempt
def api_adocoes_por_raca(request):
    racas = Raca.objects.all()
    qtd_adocoes = [
        PedidoAdocao.objects.filter(pet__raca=raca, status='AP').count()
        for raca in racas
    ]

    labels = [raca.raca for raca in racas]
    data = {
        'qtd_adocoes': qtd_adocoes,
        'labels': labels,
    }
    return JsonResponse(data)


@login_required
def editar_pet(request, id):
    pet = get_object_or_404(Pet, id=id)

    if pet.usuario != request.user:
        messages.error(request, 'Você não tem permissão para editar este pet.')
        return redirect('seus_pets')

    if request.method == "POST":
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet atualizado com sucesso!')
            return redirect('seus_pets')
    else:
        form = PetForm(instance=pet)

    return render(request, 'editar_pet.html', {'form': form, 'pet': pet})
