from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from django.utils.timezone import now

from core.utils import validate_fields
from perfil.models import Categoria

from .models import ContaPaga, ContaPagar


def definir_contas(request):
    if request.method == "GET":
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html', {'categorias': categorias})
    else:
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')

        conta = ContaPagar(titulo=titulo,
                           categoria_id=categoria,
                           descricao=descricao,
                           valor=valor,
                           dia_pagamento=dia_pagamento)

        if validate_fields(conta, ['descricao']):
            conta.save()
            messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')
        else:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/contas/definir_contas')


def ver_contas(request):
    MES_ATUAL = now().month
    DIA_ATUAL = now().day

    contas = ContaPagar.objects.all()
    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte=DIA_ATUAL + 5).filter(
        dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)

    restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_pagas).exclude(
        id__in=contas_proximas_vencimento)

    return render(
        request, 'ver_contas.html', {
            'contas_vencidas': contas_vencidas,
            'contas_proximas_vencimento': contas_proximas_vencimento,
            'restantes': restantes,
            'contas_pagas': contas_pagas
        })


def pagar(request, id):
    try:
        conta = ContaPagar.objects.get(id=id)
        conta_paga = ContaPaga.objects.create(conta=conta, data_pagamento=now())
        conta_paga.save()
        messages.add_message(request, constants.SUCCESS, f'Conta {conta} paga com sucesso')

    except ContaPagar.DoesNotExist:
        messages.add_message(request, constants.ERROR, 'Conta não encontrada')
    except Exception as e:
        messages.add_message(request, constants.ERROR,
                             f'Ocorreu um erro ao pagar a conta: {e.args[0]}')
    finally:
        return redirect('/contas/ver_contas')
