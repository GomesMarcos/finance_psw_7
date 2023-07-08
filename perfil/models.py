from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.db.models.aggregates import Sum
from django.utils.timezone import now

# Create your models here.


class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejamento = models.FloatField(default=0)

    def __str__(self):
        return self.categoria

    def total_gasto(self):
        from extrato.models import Valores

        valores = Valores.objects.filter(categoria__id=self.id, data__month=now().month,
                                         tipo='S').aggregate(Sum('valor'))
        return valores['valor__sum'] or 0

    def calcula_percentual_gasto_por_categoria(self):
        try:
            return abs(self.total_gasto() * 100) / self.valor_planejamento
        except:
            return 0


class Conta(models.Model):
    banco_choices = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa econômica'),
    )

    tipo_choices = (
        ('pf', 'Pessoa física'),
        ('pj', 'Pessoa jurídica'),
    )

    apelido = models.CharField(max_length=50, validators=[MinLengthValidator(1)])
    banco = models.CharField(max_length=2,
                             choices=banco_choices,
                             validators=[MinLengthValidator(1)])
    tipo = models.CharField(max_length=2, choices=tipo_choices, validators=[MinLengthValidator(1)])
    valor = models.FloatField(validators=[MinValueValidator(1)])
    icone = models.ImageField(upload_to='icones', validators=[MinLengthValidator(1)])

    def __str__(self):
        return self.apelido
