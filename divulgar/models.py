from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag


class Raca(models.Model):
    raca = models.CharField(max_length=50)

    def __str__(self):
        return self.raca


class Pet(models.Model):
    choices_status = (('P', 'Para adoção'),
                      ('A', 'Adotado'))

    #Chave estrangeira do usuario um para um
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    foto = models.ImageField(upload_to="fotos_pets")
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    estado = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    telefone = models.CharField(max_length=50)

    #Chave estrangeira de tag, relação de muitos para muitos
    tags = models.ManyToManyField(Tag)

    #Chave estrangeira de raça um para um
    raca = models.ForeignKey(Raca, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=choices_status, default='P')

    def __str__(self):
        return self.nome
