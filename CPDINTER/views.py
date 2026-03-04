from django.shortcuts import render, redirect, get_object_or_404
from .models import CpdinterFornecedor, CpdinterNotasFornecedor, CpdinterNotasMensaisForn
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError
from .forms import NotasMensaisForm
from django.db.models import F, Q
from django.urls import reverse
from django.db.models import Sum
import plotly.express as px
import pandas as pd
from django.db import models
from django.core.paginator import Paginator



def index(request):
    if request.method == 'POST':
        for_cnpj = request.POST['for_cnpj']
        for_cnpj = for_cnpj.zfill(14)
        for_nm_fornecedor = request.POST['for_nm_fornecedor']
        for_flag_multifilial = request.POST['for_flag_multifilial']

        fornecedor = CpdinterFornecedor(
            for_cnpj=for_cnpj,
            for_nm_fornecedor=for_nm_fornecedor,
            for_flag_multifilial=for_flag_multifilial,
            )
        fornecedor.save()
        return redirect('index')

    return render(request, 'pages/index.html')


@csrf_exempt
def verificar_cnpj(request):
    if request.method == 'POST':
        for_cnpj = request.POST.get('for_cnpj')

        if CpdinterFornecedor.objects.filter(for_cnpj=for_cnpj).exists():
            return JsonResponse({'cnpj_exists': True})

    return JsonResponse({'cnpj_exists': False})


def notas(request):
    cnpj = request.GET.get('cnpj')
    for_cnpj = request.GET.get('for_cnpj', None)
    
    if for_cnpj is not None:
        try:
            cnpj = int(for_cnpj)
        except ValueError:
            return render(request, 'erro.html', {'mensagem': 'CNPJ inválido'})

    # Obtém informações sobre o fornecedor pelo CNPJ.
    fornecedor = CpdinterFornecedor.objects.get(for_cnpj=cnpj)

    # Obtém o próximo ID sequencial
    ultimo_registro = CpdinterNotasFornecedor.objects.filter(for_cnpj=cnpj).order_by('-for_id_sequencial').first()
    if ultimo_registro:
        proximo_id_sequencial = ultimo_registro.for_id_sequencial + 1
    else:
        proximo_id_sequencial = 1

    if request.method == 'POST':
        for_id_sequencial = request.POST['for_id_sequencial']
        for_desc_nota = request.POST['for_desc_nota']
        for_cd_loja = request.POST['for_cd_loja']
        for_dia_vencimento = request.POST['for_dia_vencimento']
        for_dia_entrega = request.POST['for_dia_entrega']

        if CpdinterNotasFornecedor.objects.filter(for_cnpj=cnpj, for_id_sequencial=for_id_sequencial).exists():
            mensagem = 'Já existe uma nota com o mesmo ID.'
        else:
            CpdinterNotasFornecedor.objects.create(
                for_cnpj=fornecedor,
                for_id_sequencial=for_id_sequencial,
                for_desc_nota=for_desc_nota,
                for_cd_loja=for_cd_loja,
                for_dia_vencimento=for_dia_vencimento,
                for_dia_entrega=for_dia_entrega,
            )
            mensagem = 'Nota do fornecedor cadastrada com sucesso.'
            # Atualiza o próximo ID sequencial após criar um novo registro
            proximo_id_sequencial = int(for_id_sequencial) + 1

        # SEMPRE recarrega todos os dados após o POST
        notas_fornecedor = CpdinterNotasFornecedor.objects.filter(for_cnpj=cnpj).order_by('-for_id_sequencial')
        paginator = Paginator(notas_fornecedor, 10)
        page_number = request.GET.get('page', 1)  # Usa página 1 como padrão
        page_obj = paginator.get_page(page_number)

        return render(request, 'pages/notas.html', {
            'cnpj': cnpj,
            'page_obj': page_obj,
            'notas_fornecedor': page_obj.object_list,
            'mensagem': mensagem,
            'proximo_id_sequencial': proximo_id_sequencial
        })

    # GET request - carrega dados normais
    notas_fornecedor = CpdinterNotasFornecedor.objects.filter(for_cnpj=cnpj).order_by('-for_id_sequencial')
    paginator = Paginator(notas_fornecedor, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'pages/notas.html', {
        'cnpj': cnpj,
        'page_obj': page_obj,
        'notas_fornecedor': page_obj.object_list,
        'proximo_id_sequencial': proximo_id_sequencial
    })


def mensais(request):
    for_id_sequencial = request.GET.get('for_id_sequencial')
    for_cnpj = request.GET.get('for_cnpj')
    notas_mensais = CpdinterNotasMensaisForn.objects.filter(
                        for_id_sequencial=int(for_id_sequencial),
                        for_cnpj__for_cnpj=for_cnpj
                    ).order_by('for_nr_nota')
    try:
        fornecedor = CpdinterNotasFornecedor.objects.filter(for_cnpj=for_cnpj).first()
    except CpdinterNotasFornecedor.DoesNotExist:
        fornecedor = None

    try:
        fornecedores = CpdinterNotasFornecedor.objects.filter(for_id_sequencial=for_id_sequencial).first()
    except CpdinterNotasFornecedor.DoesNotExist:
        fornecedores = None

    if request.method == 'POST':
        for_nr_nota = request.POST['for_nr_nota']
        for_vl_nota = request.POST['for_vl_nota']
        for_dt_entrega = request.POST['for_dt_entrega']
        for_dt_emissao = request.POST['for_dt_emissao']
        for_dt_vencimento = request.POST['for_dt_vencimento']
        for_dt_envio_cadastro = request.POST['for_dt_envio_cadastro']
        for_dt_envio_financ = request.POST['for_dt_envio_financ']
        for_tx_observacao = request.POST['for_tx_observacao']

        for_dt_entrega = for_dt_entrega.strip() if for_dt_entrega else None
        for_dt_emissao = for_dt_emissao.strip() if for_dt_emissao else None
        for_dt_vencimento = for_dt_vencimento.strip() if for_dt_vencimento else None
        for_dt_envio_cadastro = for_dt_envio_cadastro.strip() if for_dt_envio_cadastro else None
        for_dt_envio_financ = for_dt_envio_financ.strip() if for_dt_envio_financ else None

        try:
            CpdinterNotasMensaisForn.objects.create(
                for_cnpj=fornecedor,
                for_id_sequencial=for_id_sequencial,
                for_nr_nota=for_nr_nota,
                for_vl_nota=for_vl_nota,
                for_dt_entrega=for_dt_entrega,
                for_dt_emissao=for_dt_emissao,
                for_dt_vencimento=for_dt_vencimento,
                for_dt_envio_cadastro=for_dt_envio_cadastro,
                for_dt_envio_financ=for_dt_envio_financ,
                for_tx_observacao=for_tx_observacao,
            )

        except ValidationError as e:

            pass

    return render(request, 'pages/mensais.html', {'for_id_sequencial': for_id_sequencial, 'for_cnpj': for_cnpj, 'notas_mensais': notas_mensais})


def notas_fornecedor(request):
    notas_mensais = CpdinterNotasMensaisForn.objects.all().order_by('-for_dt_envio_cadastro')
    fornecedores = CpdinterFornecedor.objects.all()

    if request.GET.get('data_inicio') and request.GET.get('data_fim'):
        data_inicio = datetime.strptime(request.GET['data_inicio'], '%Y-%m-%d')
        data_fim = datetime.strptime(request.GET['data_fim'], '%Y-%m-%d')

        notas_mensais = notas_mensais.filter(for_dt_vencimento__gte=data_inicio, for_dt_vencimento__lte=data_fim)

    if request.GET.get('data_emissao_inicio') and request.GET.get('data_emissao_fim'):
        data_emissao_inicio = datetime.strptime(request.GET['data_emissao_inicio'], '%Y-%m-%d')
        data_emissao_fim = datetime.strptime(request.GET['data_emissao_fim'], '%Y-%m-%d')

        notas_mensais = notas_mensais.filter(for_dt_emissao__gte=data_emissao_inicio, for_dt_emissao__lte=data_emissao_fim)

    return render(
        request,
        'pages/notas_fornecedor.html',
        {'notas_mensais': notas_mensais, 'fornecedores': fornecedores}
    )



def editar_nota(request, for_cnpj, for_id_sequencial, nota_id):
    # Buscar fornecedor
    fornecedor = get_object_or_404(
        CpdinterNotasFornecedor, 
        for_cnpj=for_cnpj,
        for_id_sequencial=for_id_sequencial
    )

    # Buscar a nota (ligação é feita pelo for_id_sequencial)
    nota = CpdinterNotasMensaisForn.objects.filter(
        for_id_sequencial=for_id_sequencial,
        for_nr_nota=nota_id
    ).first()

    if request.method == 'POST':
        form = NotasMensaisForm(request.POST, instance=nota)
        if form.is_valid():
            nova_nota = form.save(commit=False)
            nova_nota.for_id_sequencial = for_id_sequencial  # vínculo correto
            nova_nota.save()
            url = reverse('mensais')  
            return redirect(f'{url}?for_cnpj={for_cnpj}&for_id_sequencial={for_id_sequencial}')
    else:
        form = NotasMensaisForm(instance=nota)

    return render(
        request,
        'pages/editar_nota.html',
        {
            'form': form,
            'nota_id': nota_id,
            'for_cnpj': for_cnpj,
            'for_id_sequencial': for_id_sequencial
        }
    )




def registros_no_mes(request):
    # Obtém o primeiro dia e último dia do mês atual
    hoje = datetime.now()
    primeiro_dia = hoje.replace(day=1)
    
    # Corrige o cálculo do último dia do mês
    if hoje.month == 12:
        ultimo_dia = hoje.replace(year=hoje.year + 1, month=1, day=1) - timedelta(days=1)
    else:
        ultimo_dia = hoje.replace(month=hoje.month + 1, day=1) - timedelta(days=1)
    
    # Filtra os registros que têm `for_dt_envio_cadastro` no mês atual
    registros = CpdinterNotasMensaisForn.objects.filter(
        for_dt_envio_cadastro__range=(primeiro_dia, ultimo_dia)
    ).values('for_cnpj').distinct()
    
    registros_com_fornecedor = []
    soma_total = 0  # Variável para armazenar a soma total do for_vl_nota
    
    for registro in registros:
        fornecedor = CpdinterFornecedor.objects.filter(for_cnpj=registro['for_cnpj']).first()
        notas_fiscais = CpdinterNotasMensaisForn.objects.filter(
            for_cnpj=registro['for_cnpj'],
            for_dt_envio_cadastro__range=(primeiro_dia, ultimo_dia)
        )
        if fornecedor and notas_fiscais.exists():
            # Obtém a primeira nota fiscal para data
            nota_fiscal = notas_fiscais.order_by('for_dt_envio_cadastro').first()
            
            total_notas = notas_fiscais.aggregate(total=models.Sum('for_vl_nota'))['total']
            soma_total += total_notas or 0
            
            registro_com_fornecedor = {
                'for_cnpj': registro['for_cnpj'],
                'for_nm_fornecedor': fornecedor.for_nm_fornecedor,
                'for_dt_envio_cadastro': nota_fiscal.for_dt_envio_cadastro,
                'total_notas': total_notas or 0,
            }
            registros_com_fornecedor.append(registro_com_fornecedor)
    
    # Ordena os registros pelo nome do fornecedor
    registros_com_fornecedor_ordenados = sorted(registros_com_fornecedor, key=lambda x: x['for_nm_fornecedor'])
    
    context = {
        'registros': registros_com_fornecedor_ordenados,
        'soma_total': soma_total
    }
    
    return render(request, 'pages/registros.html', context)