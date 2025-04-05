from datetime import datetime
from django.contrib.messages import constants
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from .models import PedidoAdocao
from divulgar.models import Pet, Raca


def listar_pets(request):
    if request.method == "GET":
        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        pets = Pet.objects.filter(status="P").exclude(usuario=request.user)
        racas = Raca.objects.all()

        if cidade:
            pets = pets.filter(cidade__icontains=cidade)

        if raca_filter:
            pets = pets.filter(raca__id=raca_filter)
            raca_filter = Raca.objects.get(id=raca_filter)

        return render(
            request,
            'listar_pets.html',
            {'pets': pets, 'racas': racas, 'cidade': cidade, 'raca_filter': raca_filter}
        )


def pedido_adocao(request, id_pet):
    pet = Pet.objects.filter(id=id_pet, status="P").first()

    if not pet:
        messages.add_message(request, constants.WARNING, 'Esse pet já foi adotado ou não existe.')
        return redirect('/adotar')

    if pet.usuario == request.user:
        messages.add_message(request, constants.WARNING, 'Você não pode adotar um pet que você mesmo cadastrou.')
        return redirect('/adotar')

    pedido_existente = PedidoAdocao.objects.filter(pet=pet, usuario=request.user, status='AG').exists()
    if pedido_existente:
        messages.add_message(request, constants.INFO, 'Você já fez um pedido de adoção para esse pet.')
        return redirect('/adotar')

    pedido = PedidoAdocao(
        pet=pet,
        usuario=request.user,
        data=datetime.now()
    )
    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção realizado com sucesso. Você será notificado por e-mail caso ele seja aprovado.')
    return redirect('/adotar')


def processa_pedido_adocao(request, id_pedido):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)
    pet = pedido.pet

    # 🛡️ Permissões
    if status in ["A", "R"] and request.user != pet.usuario:
        messages.add_message(request, constants.ERROR, 'Você não tem permissão para aprovar ou recusar esse pedido.')
        return redirect('/divulgar/ver_pedido_adocao')

    if status == "C" and request.user != pedido.usuario:
        messages.add_message(request, constants.ERROR, 'Você não tem permissão para cancelar esse pedido.')
        return redirect('/adotar')

    # ✅ Aprovar
    if status == "A":
        pedido.status = 'AP'
        pet.status = 'A'
        mensagem = '''Olá, sua adoção foi aprovada! 🎉 
Seu novo amiguinho está esperando por você. Entre em contato com o responsável.'''

    # ❌ Recusar
    elif status == "R":
        pedido.status = 'R'
        mensagem = '''Olá, infelizmente sua adoção foi recusada. 😞 
Mas não desanime! Muitos pets ainda estão esperando por um lar.'''

    # ❎ Cancelar
    elif status == "C":
        pedido.status = 'C'
        mensagem = '''Olá, seu pedido de adoção foi cancelado com sucesso. Esperamos vê-lo de volta em breve!'''

    else:
        messages.add_message(request, constants.ERROR, 'Status de adoção inválido.')
        return redirect('/divulgar/ver_pedido_adocao')

    pedido.save()
    if status == "A":
        pet.save()

    if status in ["A", "R"]:
        send_mail(
            'Status da sua adoção - ADO.TE',
            mensagem,
            'iltonbatista2018@gmail.com.br',
            [pedido.usuario.email],
        )

    messages.add_message(request, constants.SUCCESS, 'Pedido processado com sucesso.')
    return redirect('/divulgar/ver_pedido_adocao' if request.user == pet.usuario else '/adotar')
