import json

from django.contrib.messages import constants
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from core.settings import MESSAGE_TAGS
from perfil.models import Categoria


def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias': categorias})


@csrf_exempt
def update_valor_categoria(request, id):
    try:
        novo_valor = float(json.load(request)['novo_valor'])
        if novo_valor < 0.01:
            message = 'Erro: Valor precisa ser positivo.'
            class_name_list = f'{MESSAGE_TAGS[constants.ERROR]} alert d-flex'
            status = 400
            return JsonResponse({
                'status': status,
                'message': message,
                'class_name_list': class_name_list
            })

        categoria = Categoria.objects.get(id=id)
        if novo_valor == categoria.valor_planejamento:

            message = f'Categoria "{categoria}" já possui o valor: R${novo_valor}'
            status = 409
            class_name_list = f'{MESSAGE_TAGS[constants.WARNING]} alert d-flex'
        else:
            categoria.valor_planejamento = novo_valor
            categoria.save()
            message = f'Categoria "{categoria}" atualizada com o valor: R${novo_valor}'
            status = 200
            class_name_list = f'{MESSAGE_TAGS[constants.SUCCESS]} alert d-flex'

        return JsonResponse({
            'status': status,
            'message': message,
            'class_name_list': class_name_list
        })
    except KeyError as e:
        message = f'Erro:{e.args[0]}'
        class_name_list = f'{MESSAGE_TAGS[constants.ERROR]} alert d-flex'
        status = 400
        return JsonResponse({
            'status': status,
            'message': message,
            'class_name_list': class_name_list
        })
