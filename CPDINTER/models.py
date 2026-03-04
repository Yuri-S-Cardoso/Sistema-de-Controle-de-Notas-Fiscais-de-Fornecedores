from django.db import models

class CpdinterFornecedor(models.Model):
    for_cnpj = models.BigIntegerField(primary_key=True, unique=True)
    for_nm_fornecedor = models.CharField(max_length=70)
    for_flag_multifilial = models.CharField(max_length=1)

    class Meta:
        db_table = 'CPDINTER_FORNECEDOR'

    def __str__(self):
        return str(self.for_cnpj)

class CpdinterNotasFornecedor(models.Model):
    for_cnpj = models.ForeignKey(CpdinterFornecedor, models.DO_NOTHING, db_column='for_cnpj')
    for_id_sequencial = models.IntegerField()
    for_desc_nota = models.CharField(max_length=512)
    for_cd_loja = models.IntegerField()
    for_dia_vencimento = models.IntegerField()
    for_dia_entrega = models.IntegerField()

    class Meta:
        db_table = 'CPDINTER_NOTAS_FORNECEDOR'
        unique_together = (('for_cnpj', 'for_id_sequencial'),)

    def __str__(self):
        return f"{self.for_cnpj} - {self.for_id_sequencial}"

class CpdinterNotasMensaisForn(models.Model):
    for_cnpj = models.ForeignKey(CpdinterNotasFornecedor, models.DO_NOTHING, db_column='for_cnpj', related_name='notas_mensais')
    for_id_sequencial = models.IntegerField()
    for_nr_nota = models.BigIntegerField()
    for_vl_nota = models.DecimalField(max_digits=12, decimal_places=2)
    for_dt_entrega = models.DateField(blank=True, null=True)
    for_dt_emissao = models.DateField(blank=True, null=True)
    for_dt_vencimento = models.DateField(blank=True, null=True)
    for_dt_envio_cadastro = models.DateField(blank=True, null=True)
    for_dt_envio_financ = models.DateField(blank=True, null=True)
    for_tx_observacao = models.CharField(max_length=512, blank=True, null=True)

