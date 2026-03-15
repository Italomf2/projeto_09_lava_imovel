[![Assista a apresentação do projeto](https://youtu.be/OxZnKPmyvBs)


# Projeto 09 — Operação Lava-Imóvel: Lavagem de Dinheiro Imobiliário

> **Disciplina:** Programação para Ciência de Dados
> **Curso:** MBA em Ciência de Dados — UNIFOR
> **Professor:** Cássio Pinheiro
> **Formato:** Datathon Investigativo
> **Trabalho:** Em duplas ou trios (formação livre)
> **Classificação:** Grupo A — Investigativo (padrões ocultos para descobrir)

---

## Briefing da Operação

O Ministério Público recebeu informações de inteligência financeira sobre **possíveis operações de lavagem de dinheiro** no mercado imobiliário de Fortaleza. O esquema envolveria: compra de imóveis a preços inflados por **CPFs com renda incompatível**, uso de **CNPJs de fachada** como intermediários, e **revenda rápida** (flip) com lucros artificiais. Tudo para transformar dinheiro ilícito em ativos aparentemente legítimos.

Você recebeu dados de 3.500 transações imobiliárias, perfis de compradores e o histórico de preços por bairro. Encontre os suspeitos.

---

## Datasets Fornecidos

### 1. `data/projeto_09_mercado_imobiliario.csv`
3.500+ transações imobiliárias (2022-2024).

| Coluna | Descrição |
|--------|-----------|
| `transacao_id` | Identificador da transação |
| `imovel_id` | Identificador do imóvel |
| `bairro` | Bairro do imóvel |
| `tipo_imovel` | Tipo (Apartamento, Casa, Cobertura, Flat/Studio) |
| `area_m2` | Área em m² |
| `quartos` | Número de quartos |
| `condicao` | Condição (Novo, Usado) |
| `preco_total` | Preço total da transação (R$) |
| `preco_m2` | Preço por m² (R$) |
| `comprador_id` | CPF do comprador |
| `comprador_cnpj` | CNPJ associado (se houver) |
| `forma_pagamento` | Forma de pagamento (Financiamento, À vista) |
| `ano_transacao` | Ano da transação |
| `mes_transacao` | Mês da transação |
| `dias_no_mercado` | Dias que o imóvel ficou no mercado |

### 2. `data/projeto_09_compradores_perfil.csv`
Perfil dos compradores.

| Coluna | Descrição |
|--------|-----------|
| `comprador_id` | CPF do comprador |
| `renda_mensal_declarada` | Renda mensal declarada (R$) |
| `idade` | Idade |
| `estado_civil` | Estado civil |
| `profissao` | Profissão |
| `numero_imoveis_adquiridos` | Número de imóveis adquiridos |
| `possui_restricao_credito` | Se tem restrição de crédito (0/1) |
| `pep` | Pessoa Exposta Politicamente (0/1) |

### 3. `data/projeto_09_historico_precos_bairro.csv`
Histórico de preços de referência por bairro.

| Coluna | Descrição |
|--------|-----------|
| `bairro` | Bairro |
| `ano` | Ano |
| `trimestre` | Trimestre |
| `preco_m2_referencia` | Preço de referência por m² (R$) |
| `numero_transacoes` | Número de transações no período |
| `variacao_trimestral_pct` | Variação trimestral (%) |

---

## Missão

Investigue os dados e responda:

1. **Quais transações têm preço 40-60% acima do valor de referência do bairro?** Cruze o preço por m² com o histórico de referência. Quem comprou esses imóveis?
2. **Existem compradores com renda incompatível com o valor dos imóveis?** Identifique CPFs que compraram imóveis de R$ 1M+ com renda declarada < R$ 5.000.
3. **Há CPFs que compraram múltiplos imóveis?** Quantos compradores adquiriram 3 ou mais imóveis? Qual o perfil deles?
4. **Existem imóveis revendidos em menos de 6 meses com lucro > 50%?** Identifique `imovel_id` que aparece mais de uma vez nas transações com diferença curta de tempo.
5. **Os CNPJs envolvidos nas transações suspeitas estão conectados?** Há algum padrão (poucos CNPJs repetidos em muitas transações suspeitas)?
6. **Pagamentos "à vista" são mais frequentes nas transações suspeitas?** Compare a forma de pagamento entre transações normais e suspeitas.
7. **Monte o dossiê final:** Liste os CPFs e CNPJs suspeitos com as evidências encontradas.

---

## Pistas Iniciais

- Cruze `preco_m2` das transações com `preco_m2_referencia` do mesmo bairro/trimestre — diferenças de 40-60% são suspeitas
- CPFs na faixa **CPF-09001 a CPF-09020** merecem atenção
- Procure `imovel_id` que aparece **mais de uma vez** — é o mesmo imóvel sendo revendido
- Filtre transações **"À vista"** com valor > R$ 800.000 — quem paga tanto em cash?
- No perfil de compradores, procure **renda < R$ 5.000** com **múltiplos imóveis** — isso não bate

---

## Desafio de Dados Reais

Enriqueça sua investigação com dados públicos reais:

| Fonte | URL | O que buscar |
|-------|-----|-------------|
| **FipeZap** | https://fipezap.zapimoveis.com.br/ | Índice de preços imobiliários reais por cidade e bairro |
| **VivaReal / ZAP Imóveis** | https://www.vivareal.com.br/ | Preços de referência do mercado imobiliário de Fortaleza |

**Perguntas de cruzamento:**
- O preço médio por m² dos bairros no dataset é compatível com os valores reais do FipeZap?
- A proporção de pagamentos "à vista" encontrada é realista para o mercado imobiliário brasileiro?

---

## Técnicas Esperadas

| Módulo | Técnicas |
|--------|----------|
| **M1 — Python** | Funções para cálculo de sobrepreço e flags de suspeita, manipulação de datas, tratamento de nulos |
| **M2 — Pandas/NumPy** | `merge` entre 3 datasets, `groupby` por comprador/bairro, detecção de duplicatas por `imovel_id`, cálculos de razões (renda vs. preço), `pivot_table` |
| **M3 — Visualização** | Scatter de preço vs. referência (com destaque de outliers), regplot, jointplot, heatmap de preço por bairro, barplots de forma de pagamento, histograma de renda dos suspeitos |

---

## Estrutura do Projeto

```
projeto_09/
├── README.md          ← Este arquivo
├── data/              ← 3 datasets do projeto
├── notebooks/         ← Notebook(s) Jupyter com a investigação
├── scripts/           ← Scripts Python auxiliares (se necessário)
└── docs/              ← Documentação adicional, apresentação
```

## Entregáveis

1. **Notebook Python (.ipynb)** em `notebooks/` contendo:
   - Importação e inspeção dos 3 datasets
   - Limpeza e transformação (nulos, tipos, duplicatas, outliers)
   - Cruzamento entre datasets (merge/join)
   - Análise investigativa com estatísticas descritivas
   - Mínimo de **8 visualizações** (mix de Matplotlib e Seaborn)
   - Respostas à missão com **evidências nos dados**
   - Células Markdown narrando a investigação (storytelling)
   - Conclusões: quem são os suspeitos e quais as evidências

2. **Apresentação oral** (5-7 minutos) — arquivo em `docs/`

## Critérios de Avaliação

| Critério | Peso | O que será observado |
|----------|------|----------------------|
| **Limpeza e transformação dos dados** | 20% | Tratamento de nulos, duplicatas, tipos incorretos, outliers. Justificativa das decisões. |
| **Profundidade da investigação** | 25% | Cruzamento entre os 3 datasets. Respostas fundamentadas à missão. Descoberta de padrões ocultos. |
| **Qualidade e variedade das visualizações** | 20% | Mínimo 8 gráficos. Pelo menos 3 tipos diferentes. Títulos, rótulos, legendas. |
| **Storytelling investigativo** | 20% | Narrativa coerente. Evidências visuais. Conclusões defendidas com dados. Apresentação oral. |
| **Organização do código e boas práticas** | 15% | Código limpo. Funções quando apropriado. Notebook autoexplicativo. |

### Bonificações
- **Enriquecimento com dados reais** (integração de fonte pública): **+1.0 ponto**
- Uso criativo de feature engineering: **+0.5 ponto**
- Visualização avançada além do esperado: **+0.5 ponto**
- Análise adicional não solicitada com insights valiosos: **+0.5 ponto**

### Penalizações
- Notebook sem células Markdown explicativas: **-1.0 ponto**
- Gráficos sem título, rótulos ou legendas: **-0.5 ponto por gráfico**
- Código copiado sem adaptação (entre grupos): **nota zero para ambos**
- Entrega após o prazo: **-2.0 pontos por dia**

---

*Prof. Cássio Pinheiro — MBA Ciência de Dados — UNIFOR — 2026*
