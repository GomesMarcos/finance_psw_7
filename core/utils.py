def validate_fields(instance, null_fields=None):
    null_fields = null_fields or []
    return not any((attr not in ['id', 'state'] + null_fields) and (val is None or val == '')
                   for attr, val in instance.__dict__.items())


def calcula_equilibrio_financeiro(gastos_mensais):
    gastos_essenciais = gastos_mensais.filter(categoria__essencial=True)
    gastos_nao_essenciais = gastos_mensais.filter(categoria__essencial=False)

    total_gastos_essenciais = sum(valor.valor for valor in gastos_essenciais)
    total_gastos_nao_essenciais = sum(valor.valor for valor in gastos_nao_essenciais)

    if total := total_gastos_essenciais + total_gastos_nao_essenciais:
        percentual_gastos_essenciais = total_gastos_essenciais * 100 / total
        percentual_gastos_nao_essenciais = total_gastos_nao_essenciais * 100 / total
        return percentual_gastos_essenciais, percentual_gastos_nao_essenciais

    return 0, 0


def get_total_contas(MES_ATUAL, DIA_ATUAL):
    from contas.models import ContaPaga, ContaPagar

    contas = ContaPagar.objects.all()
    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
    contas_vencidas = contas.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte=DIA_ATUAL + 5).filter(
        dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)

    restantes = contas.exclude(id__in=contas_vencidas).exclude(id__in=contas_pagas).exclude(
        id__in=contas_proximas_vencimento)

    return contas_pagas, contas_vencidas, contas_proximas_vencimento, restantes
