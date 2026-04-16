# Sistema de Controle de Notas Fiscais de Fornecedores

Aplicação web desenvolvida em **Django** para **cadastro, controle, lançamento e acompanhamento de notas fiscais de fornecedores**, com foco em operação administrativa e financeira de lojas.

O sistema permite cadastrar fornecedores, configurar notas base por fornecedor e loja, realizar lançamentos mensais dessas notas, consultar relatórios com filtros e exportar os dados para **Excel**.

---

## Visão geral

Este projeto foi desenvolvido para centralizar e organizar o fluxo de notas fiscais de fornecedores, oferecendo uma estrutura simples e funcional para operações internas.

A aplicação atende cenários em que a empresa precisa:

- cadastrar fornecedores por CNPJ
- definir rotinas/notas vinculadas a cada fornecedor
- associar notas a lojas específicas
- registrar lançamentos mensais
- controlar datas importantes do processo
- consultar relatórios consolidados
- exportar dados para análise externa

---

## Finalidade do sistema

A finalidade principal do sistema é fornecer um ambiente único para controle operacional de notas fiscais de fornecedores.

### Problemas que o sistema resolve

- Centraliza o cadastro de fornecedores
- Organiza notas base por fornecedor e loja
- Permite o lançamento mensal de notas fiscais
- Facilita o acompanhamento de datas de emissão, vencimento e envio interno
- Oferece relatórios consolidados com filtros
- Possibilita exportação de dados para Excel
- Apoia rotinas administrativas, fiscais e financeiras

### Público provável

O sistema parece ter sido pensado para uso por equipes como:

- administrativo
- fiscal
- cadastro
- financeiro
- operações de lojas

Especialmente em contextos com **múltiplas lojas** e necessidade de acompanhamento recorrente de notas fiscais.

---

## Funcionalidades principais

### Cadastro de fornecedores
- Cadastro de fornecedor na página inicial
- Registro de CNPJ
- Registro de nome do fornecedor
- Indicação de fornecedor multifilial
- Verificação assíncrona de existência de CNPJ

### Cadastro de notas por fornecedor
- Criação de notas base por fornecedor
- Associação de notas a uma loja
- Definição de identificador sequencial por fornecedor
- Registro de dia de entrega
- Registro de dia de vencimento
- Listagem paginada das notas cadastradas

### Lançamento mensal de notas fiscais
- Lançamento mensal por nota base
- Registro do número da nota fiscal
- Registro do valor da nota
- Registro da data de emissão
- Registro da data de vencimento
- Registro da data de envio para cadastro
- Registro da data de envio para financeiro
- Campo de observação
- Listagem dos lançamentos realizados

### Edição de notas mensais
- Edição de lançamentos mensais já cadastrados
- Atualização de informações por formulário
- Correção de dados operacionais e financeiros

### Relatórios
- Relatório geral consolidado
- Filtro por CNPJ
- Filtro por número da nota
- Filtro por nome do fornecedor
- Filtro por intervalo de vencimento
- Filtro por intervalo de emissão
- Exibição tabular de resultados

### Exportação
- Exportação de relatório para Excel
- Geração de arquivo a partir da tabela exibida
- Uso de SheetJS/XLSX no front-end

### Resumo mensal
- Relatório de registros lançados no mês
- Agrupamento por fornecedor
- Exibição de somatório financeiro mensal
- Visão resumida para acompanhamento gerencial

---

## Fluxo geral do sistema

O funcionamento principal da aplicação segue este fluxo:

1. O usuário acessa a página inicial.
2. Informa um CNPJ.
3. O sistema verifica se esse CNPJ já existe.
4. Se existir, o usuário é redirecionado para a área de notas do fornecedor.
5. Se não existir, pode realizar o cadastro do fornecedor.
6. Na área de notas, o usuário cadastra as notas base por fornecedor e loja.
7. Cada nota base possui um identificador sequencial.
8. Ao acessar uma nota base específica, o usuário entra na tela de lançamentos mensais.
9. Nessa tela, registra número da nota, valor, datas e observações.
10. O sistema permite editar lançamentos quando necessário.
11. O usuário pode consultar relatórios consolidados.
12. Os dados podem ser exportados para Excel.
13. Também existe uma visão resumida dos lançamentos do mês por fornecedor.

---

## Tecnologias utilizadas

### Back-end
- **Python**
- **Django 4.2.x**

### Banco de dados
- **SQLite**

### Front-end
- **HTML com Django Templates**
- **CSS próprio**
- **JavaScript puro**
- **jQuery via CDN**

### Exportação e manipulação de dados
- **SheetJS / XLSX** para exportação Excel
- **Plotly Express** importado no projeto
- **Pandas** importado no projeto

> Observação: Plotly e Pandas foram identificados nos imports, mas sem evidência clara de uso efetivo no fluxo principal atual.

---

## Arquitetura do projeto

O sistema segue o padrão clássico do **Django MVT (Model-View-Template)**.

### Características da arquitetura
- Estrutura simples e direta
- Um único app principal centralizando a lógica de negócio
- Regras implementadas majoritariamente em `views.py`
- Templates Django para renderização de páginas
- Validações e interações complementares em JavaScript
- Sem camadas avançadas de serviços ou repositórios

É um projeto monolítico de escopo administrativo, com foco em produtividade operacional.

---

## Estrutura do projeto

```bash
NOTAS/
├── NOTAS/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── CPDINTER/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   ├── templates/
│   │   ├── base/
│   │   └── pages/
│   └── static/
│       ├── css/
│       └── imagens/
├── db.sqlite3
├── manage.py
├── NOTAS.bat
└── 5000_NOTAS.bat
