from datetime import datetime
from django.contrib.messages import constants
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import PedidoAdocao

from divulgar.models import Pet, Raca
from django.core.mail import send_mail


#Função para listar
def listar_pets(request):
    if request.method == "GET":
        cidade = request.GET.get('cidade')
        raca_filter = request.GET.get('raca')

        pets = Pet.objects.filter(status="P")
        racas = Raca.objects.all()

        #caso o usuario digite alguma cidade
        if cidade:
            #icotains e não precisa digitar o nome inteiro da cidade, encontra so com algumas letras
            pets = pets.filter(cidade__icontains=cidade)

        #caso o usuario opte pelo filtro de raças
        if raca_filter:
            pets = pets.filter(raca__id=raca_filter)
            raca_filter = Raca.objects.get(id=raca_filter)

        # TODO: Colocar filtro de todos os cães


        return render(
            request,
            'listar_pets.html',
            {'pets': pets, 'racas': racas, 'cidade': cidade, 'raca_filter': raca_filter}
        )

def pedido_adocao(request, id_pet):
    #buscar no banco de dados
    pet = Pet.objects.filter(id=id_pet).filter(status="P")


    if not pet.exists():
        messages.add_message(request, constants.WARNING, 'Esse pet ja foi adotado')
        return redirect('/adotar')


    #Criar o pedido de adoção
    pedido = PedidoAdocao(pet=pet.first(), # Pega o primeiro da lista com o .first
                          usuario=request.user, # Passando o usuario logado
                          data=datetime.now()) # a data do pedido

    pedido.save()

    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção realizado, você receberá um e-mail caso ele seja aprovado.')
    return redirect('/adotar')




def processa_pedido_adocao(request, id_pedido):
    status = request.GET.get('status')
    pedido = PedidoAdocao.objects.get(id=id_pedido)
    #pet = Pet.objects.get(status=s)

    if status == "A":
        pedido.status = 'AP'
        Pet.status = 'A'
        string = '''Olá, sua adoção foi aprovada. ...'''
    elif status == "R":
        string = '''Olá, sua adoção foi recusada. ...'''
        Pet.status = 'P'
        pedido.status = 'R'

    pedido.save()

    # TODO: Alterar status do PET

    print(pedido.usuario.email)
    email = send_mail(
        'Sua adoção foi processada',
        string,
        'iltonbatista2018@gmail.com.br',
        [pedido.usuario.email,],
    )

    messages.add_message(request, constants.SUCCESS, 'Pedido de adoção processado com sucesso')
    return redirect('/divulgar/ver_pedido_adocao')









