from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render
from django.utils.timezone import now

from core.utils import calcula_equilibrio_financeiro, get_total_contas
from extrato.models import Valores

from .models import Categoria, Conta


def home(request):
    contas = Conta.objects.all()
    valores = Valores.objects.filter(data__month=now().month)
    total_entradas = sum(valor.valor for valor in valores.filter(tipo='E'))
    total_saidas = sum(valor.valor for valor in valores.filter(tipo='S'))
    total_contas = sum(conta.valor for conta in contas)

    percentual_gastos_essenciais, percentual_gastos_nao_essenciais = calcula_equilibrio_financeiro(
        valores.filter(tipo='S'))

    contas_pagas, contas_vencidas, contas_proximas_vencimento, restantes = get_total_contas(
        now().month,
        now().day)

    return render(
        request, 'home.html', {
            'contas': contas,
            'total_contas': total_contas,
            'total_entradas': total_entradas,
            'total_saidas': total_saidas,
            'total_livre': total_entradas - total_saidas,
            'percentual_gastos_essenciais': percentual_gastos_essenciais,
            'percentual_gastos_nao_essenciais': percentual_gastos_nao_essenciais,
            'total_contas_pagas': contas_pagas.count(),
            'total_contas_vencidas': contas_vencidas.count(),
            'total_contas_proximas_vencimento': contas_proximas_vencimento.count(),
            'total_restantes': restantes.count(),
        })


def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    total_contas = sum(conta.valor for conta in contas)

    context = {'contas': contas, 'total_contas': total_contas, 'categorias': categorias}

    return render(request, 'gerenciar.html', context)


def deletar_banco(request, id):
    try:
        conta = Conta.objects.get(id=id)
        conta.delete()
        messages.add_message(request, constants.SUCCESS, 'Conta deletada com sucesso')

    except Categoria.DoesNotExist:
        messages.add_message(request, constants.ERROR, 'Conta não encontrada')
    finally:
        return redirect('/perfil/gerenciar/')


def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    conta = Conta(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone,
    )

    for attr, val in conta.__dict__.items():
        if attr not in ['id', 'state'] and (val is None or val == ''):
            messages.add_message(request, constants.ERROR,
                                 f"Preencha todos os campos. '{attr}' em branco.")
            return redirect('/perfil/gerenciar/')

    conta.save()

    messages.add_message(request, constants.SUCCESS, "Conta cadastrada com sucesso!")

    return redirect('/perfil/gerenciar/')


def cadastrar_categoria(request):
    categoria = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    categoria = Categoria(
        categoria=categoria,
        essencial=essencial,
    )

    for attr, val in categoria.__dict__.items():
        if attr not in ['id', 'state', 'valor_planejamento'] and (val is None or val == ''):
            messages.add_message(request, constants.ERROR,
                                 f"Preencha todos os campos. '{attr}' em branco.")
            return redirect('/perfil/gerenciar/')

    categoria.save()

    messages.add_message(request, constants.SUCCESS, "Categoria cadastrada com sucesso!")

    return redirect('/perfil/gerenciar/')


def update_categoria(request, id):

    try:
        categoria = Categoria.objects.get(id=id)
        categoria.essencial = not categoria.essencial

        categoria.save()
        messages.add_message(request, constants.SUCCESS, "Categoria atualizada com sucesso!")

    except Categoria.DoesNotExist:
        messages.add_message(request, constants.ERROR, 'Categoria não encontrada')
    finally:
        return redirect('/perfil/gerenciar/')


def dashboard(request):
    categorias = Categoria.objects.all()

    dados = {
        categoria.categoria:
            sum(valor.valor for valor in Valores.objects.filter(categoria=categoria))
        for categoria in categorias
    }
    return render(request, 'dashboard.html', {
        'labels': list(dados.keys()),
        'values': list(dados.values())
    })
