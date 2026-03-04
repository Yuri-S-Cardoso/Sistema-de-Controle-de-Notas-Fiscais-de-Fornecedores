from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('notas/', views.notas, name='notas'),
    path('verificar_cnpj/', views.verificar_cnpj, name='verificar_cnpj'),
    path('mensais', views.mensais, name='mensais'),
    path('notas_fornecedor', views.notas_fornecedor, name='notas_fornecedor'),
    path('editar/<int:for_cnpj>/<int:for_id_sequencial>/<int:nota_id>/', views.editar_nota, name='editar_nota'),
    path('registros-no-mes/', views.registros_no_mes, name='registros_no_mes'),
]
