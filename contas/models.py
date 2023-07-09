from django.core.validators import MinValueValidator
from django.db import models

from perfil.models import Categoria


class ContaPagar(models.Model):
    titulo = models.CharField(max_length=50)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    descricao = models.TextField(blank=True, null=True, default=None)
    valor = models.FloatField(validators=[MinValueValidator(0.01)])
    dia_pagamento = models.IntegerField()

    def __str__(self):
        return f"{self.titulo}"


class ContaPaga(models.Model):
    conta = models.ForeignKey(ContaPagar, on_delete=models.DO_NOTHING)
    data_pagamento = models.DateField()

    def __str__(self):
        return f"{self.conta} (PAGA)"
