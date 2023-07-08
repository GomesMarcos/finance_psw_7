from datetime import timedelta
from io import BytesIO

from django.conf import settings
from django.contrib import messages
from django.contrib.messages import constants
from django.http import FileResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.timezone import now
from weasyprint import HTML

from core.utils import validate_fields
from perfil.models import Categoria, Conta

from .models import Valores


def get_valores_from_request(request):
    valor = request.POST.get('valor')
    categoria_id = request.POST.get('categoria')
    conta_id = request.POST.get('conta')
    descricao = request.POST.get('descricao')
    data = request.POST.get('data')
    tipo = request.POST.get('tipo')

    return Valores(
        valor=valor,
        categoria_id=categoria_id,
        descricao=descricao,
        data=data,
        conta_id=conta_id,
        tipo=tipo,
    )


def format_value(valores):
    valores.valor = float(valores.valor)
    if valores.valor < 0 and valores.tipo == 'E' or valores.valor > 0 and valores.tipo == 'S':
        return valores.valor * -1
    return valores.valor


def novo_valor(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        context = {'contas': contas, 'categorias': categorias}
        return render(request, 'novo_valor.html', context)

    elif request.method == 'POST':
        valores = get_valores_from_request(request)
        valores.valor = format_value(valores)

        if not validate_fields(valores):
            messages.add_message(request, constants.ERROR, "Preencha todos os campos.")
            return redirect('/extrato/novo_valor/')

    try:
        conta = Conta.objects.get(id=valores.conta_id)
        conta.valor += valores.valor
        if conta.valor > 0:
            conta.save()
            valores.save()
            messages.add_message(request, constants.SUCCESS, f"{conta} atualizada com sucesso.")
            message = "Entrada" if valores.tipo == "E" else "Saída"
            messages.add_message(request, constants.SUCCESS, f"{message} cadastrada com sucesso.")
        else:
            messages.add_message(request, constants.ERROR, f"Saldo insuficiente em {conta}.")
    except Conta.DoesNotExist:
        messages.add_message(request, constants.ERROR, "Conta inválida")
    except Exception as e:
        messages.add_message(request, constants.ERROR, f"Ocorreu um erro não esperado: {e.args[0]}")
    finally:
        return render(request, 'novo_valor.html')


def view_extrato(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    valores = Valores.objects.filter(data__month=now().month)
    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')
    periodo_get = int(request.GET.get('periodo', 1))

    if conta_get:
        valores.filter(conta__id=conta_get)

    if categoria_get:
        valores.filter(categoria__id=categoria_get)

    if periodo_get:
        get_last_month_valores(valores) if periodo_get == 1 \
            else valores.filter(data=now() - timedelta(days=periodo_get))

    return render(request, 'view_extrato.html', {
        'valores': valores,
        'contas': contas,
        'categorias': categorias
    })


def get_last_month_valores(valores):
    if now().day == 1:
        return valores.filter(data=now())
    return valores.filter(data=now() - timedelta(days=now().day - 1))


def exportar_pdf(request):
    valores = Valores.objects.filter(data__month=now().month)
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()

    path_template = str(settings.BASE_DIR / 'templates/partial/extrato.html')
    path_output = BytesIO()

    template_render = render_to_string(path_template, {
        'valores': valores,
        'contas': contas,
        'categorias': categorias
    })
    HTML(string=template_render).write_pdf(path_output)

    # setting pointer to initial position
    path_output.seek(0)

    return FileResponse(path_output, filename="extrato.pdf")