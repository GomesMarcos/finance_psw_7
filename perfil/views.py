from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import redirect, render

from .models import Categoria, Conta


def home(request):
    contas = Conta.objects.all()
    total_contas = sum(conta.valor for conta in contas)
    return render(request, 'home.html', {
        'contas': contas,
        'total_contas': total_contas,
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
