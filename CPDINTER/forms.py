from django import forms
from .models import CpdinterNotasMensaisForn


class NotasMensaisForm(forms.ModelForm):
    class Meta:
        model = CpdinterNotasMensaisForn
        fields = ['for_vl_nota', 'for_dt_entrega', 'for_dt_emissao', 
        'for_dt_vencimento', 'for_dt_envio_cadastro', 'for_dt_envio_financ', 'for_tx_observacao']
        labels = {
            'for_vl_nota': 'Valor da nota',
            'for_dt_entrega': 'Entrega',
            'for_dt_emissao': 'Emissão',
            'for_dt_vencimento': 'Vencimento',
            'for_dt_envio_cadastro': 'Envio cadastro',
            'for_dt_envio_financ': 'Envio financeiro',
            'for_tx_observacao': 'Observação',
        }
