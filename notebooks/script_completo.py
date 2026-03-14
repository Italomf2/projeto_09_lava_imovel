import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

perfil_compradores = r"C:\MBA_DC_13\mba_ia_unifor_13\praticas\projeto_final\projeto_09\data\projeto_09_compradores_perfil.csv"

preços_bairro = r"C:\MBA_DC_13\mba_ia_unifor_13\praticas\projeto_final\projeto_09\data\projeto_09_historico_precos_bairro.csv"

mercado_imobiliario = r"C:\MBA_DC_13\mba_ia_unifor_13\praticas\projeto_final\projeto_09\data\projeto_09_mercado_imobiliario.csv"

df_compradores = pd.read_csv(perfil_compradores, delimiter=',')

print('\n Exibindo perfil de compradores\n')
print(df_compradores.head())

df_preços_bairros = pd.read_csv(preços_bairro, delimiter=',')

print('\n Exibindo preços dos bairros\n')
print(df_preços_bairros.head())

df_mercado_imobiliario = pd.read_csv(mercado_imobiliario, delimiter=',')

# substituindo nulos por 0 e tranformando campo em inteiro
df_mercado_imobiliario["dias_no_mercado"] = (df_mercado_imobiliario["dias_no_mercado"].fillna(0).astype(int))

df_mercado_imobiliario["CNPJ OK"] = df_mercado_imobiliario["comprador_cnpj"]

# verifica se nao é nulo, caso nao seja retorna SIM
df_mercado_imobiliario["comprador_cnpj"] = df_mercado_imobiliario["comprador_cnpj"].notna().map({True: "sim", False: "nao"})

print('\n Exibindo mercado imobiliario\n')
print(df_mercado_imobiliario.head())

df_consolidado = pd.merge(df_compradores,df_mercado_imobiliario, on='comprador_id', how = 'inner')

print(df_consolidado.head())
#agrupa bairro-preço e traz a media de preço por bairro
media_por_bairro = df_preços_bairros.groupby("bairro")["preco_m2_referencia"].mean().reset_index()
#transforma preço para float
media_por_bairro["preco_m2_referencia"] = media_por_bairro["preco_m2_referencia"].astype(float)
#cruza base de compradores com a media de preço por bairro
df_master = pd.merge(df_consolidado, media_por_bairro, on="bairro", how="left")

print("Colunas:", df_master.columns)
print(df_master.head())

df_master['variação'] = (df_master['preco_m2'] / df_master['preco_m2_referencia']) - 1

df_master['é suspeito?'] = np.where(df_master['variação'] >= 0.40,'SIM','NÃO')

df_suspeitos_sobrepreco = df_master[['transacao_id', 'comprador_id', 'bairro', 'variação','é suspeito?','profissao']]

print(df_suspeitos_sobrepreco.head(10))

print("1. Transações com Sobrepreço:")

dados_grafico = pd.crosstab(df_master['profissao'], df_master['é suspeito?'])

# Ordena o DataFrame baseando-se na coluna 'SIM' do maior para o menor
dados_grafico = dados_grafico.sort_values(by='SIM', ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
dados_grafico.plot(kind='bar', ax=ax, color=['#1f77b4', '#d62728'], edgecolor='black')

for container in ax.containers:
    ax.bar_label(container, padding=3)

plt.title('Volume de Transações por Profissão (Suspeitos vs Não Suspeitos)', fontsize=14, pad=15)
plt.xlabel('Profissão', fontsize=12)
plt.ylabel('Quantidade de Transações', fontsize=12)
plt.xticks(rotation=45, ha='right') 
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend(title='É suspeito?')
plt.tight_layout()

plt.show()



# suspeitos_renda = df_master[(df_master['preco_total'] >= 1000000) & (df_master['renda_mensal_declarada'] < 5000)]


df_master['compra_suspeita?'] = np.where((df_master['preco_total'] >= 1000000) & (df_master['renda_mensal_declarada'] < 5000), 'SIM', 'NÃO')


print("\n2. CPFs com Renda Incompatível:")
print(df_master[['comprador_id', 'renda_mensal_declarada', 'preco_total','compra_suspeita?']])

pd.set_option('display.float_format', lambda x: '{:.2f}'.format(x))

visao_suspeitos = df_master.groupby('compra_suspeita?').agg({'renda_mensal_declarada': 'sum','preco_total': 'sum'}).reset_index()

visao_suspeitos.columns = ['SUSPEITO?', 'Soma de RENDA DECLARADA', 'Soma de preco_total']

visao_suspeitos['investimento/renda'] = (visao_suspeitos['Soma de preco_total']/visao_suspeitos['Soma de RENDA DECLARADA'])

print(visao_suspeitos)

x = visao_suspeitos['SUSPEITO?']
y = visao_suspeitos['investimento/renda']

# 2. Plotagem com o azul petróleo (mesmo estilo do prompt anterior)
plt.bar(x, y, color='#1f618d')

# 3. Adicionar valores em cima das barras
for i, valor in enumerate(y):
    plt.text(i, valor, f'{valor:.2f}', ha='center', va='bottom')

# 4. Adicionar a variação de 502% entre as barras
# Posicionamos no centro (0.5) e numa altura média
plt.annotate('Variação: 502%', 
             xy=(0.5, 300), 
             ha='center', 
             fontsize=12, 
             fontweight='bold',
             color='red',
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

plt.title('INVESTIMENTO/RENDA')
plt.show()

df_master['maior_3_aquisicoes?'] = np.where(df_master['numero_imoveis_adquiridos'] >= 3, 'SIM', 'NÃO')

visao_profissao = df_master.groupby(['profissao', 'maior_3_aquisicoes?'])['comprador_id'].nunique().unstack(fill_value=0)

print(visao_profissao)

dados_sim = visao_profissao['SIM'][visao_profissao['SIM'] > 0]

plt.figure(figsize=(8, 8))
plt.pie(dados_sim, labels=dados_sim.index, autopct='%1.1f%%', startangle=140)

plt.title('Distribuição de Profissões (Apenas > 3 aquisições)')
plt.show()

# contagem_imovel = df_master.groupby('imovel_id')['imovel_id'].transform('count')

# # 2. Se o imóvel aparecer mais que 2 vezes, recebe 'SIM', caso contrário 'NÃO'
# df_master['varias_transacoes'] = np.where(contagem_imovel > 2, 'SIM', 'NÃO')

# print(df_master[['varias_transacoes']])

df_master["varias_transacoes"] = df_master.duplicated(subset="imovel_id",keep=False)

df_master["varias_transacoes"] = df_master["varias_transacoes"].map({True: "SIM", False: "NAO"})

print("\nImóveis com várias transações:")
print(df_master[["imovel_id","preco_total","varias_transacoes"]].head())

df_varias = df_master[df_master["varias_transacoes"] == "SIM"]

df_revenda = df_varias.groupby("imovel_id")["preco_total"].agg(["min","max"]).reset_index()

df_revenda.rename(columns={"min":"valor_minimo","max":"valor_maximo"},inplace=True)

df_revenda["variacao_pct"] = ((df_revenda["valor_maximo"] - df_revenda["valor_minimo"])/df_revenda["valor_minimo"]) * 100

df_revenda["lucro_suspeito"] = np.where(df_revenda["variacao_pct"] > 50,"SIM","NAO")

print("\nImóveis revendidos com variação de preço:")
print(df_revenda.head())

suspeitos_flip = df_revenda[df_revenda["lucro_suspeito"] == "SIM"]
suspeitos_flip = suspeitos_flip.sort_values("variacao_pct",ascending=False)

print("\nImóveis com lucro acima de 50%:")
print(suspeitos_flip)

plt.figure(figsize=(10,6))

plt.bar(suspeitos_flip["imovel_id"],suspeitos_flip["variacao_pct"])

plt.title("Imóveis com lucro superior a 50%")
plt.xlabel("ID do imóvel")
plt.ylabel("Variação (%)")

plt.xticks(rotation=45)

plt.show()

# remover valores NaN da coluna CNPJ OK
df_cnpj = df_master[df_master["CNPJ OK"].notna()]

# agrupar pelo CNPJ e contar quantas transações cada um possui
cnpj_transacoes = df_cnpj.groupby("CNPJ OK")["transacao_id"].count().reset_index()

# renomear coluna para facilitar leitura
cnpj_transacoes.rename(
    columns={"transacao_id": "quantidade_transacoes"},
    inplace=True
)

# ordenar do maior para o menor
cnpj_transacoes = cnpj_transacoes.sort_values(
    by="quantidade_transacoes",
    ascending=False
)

# pegar os 5 CNPJs com mais transações
top5_cnpj = cnpj_transacoes.head(5)

# calcular total e média
total_top5 = top5_cnpj["quantidade_transacoes"].sum()

top5_cnpj["quantidade_transacoes"] = top5_cnpj["quantidade_transacoes"].astype(int)

print("\nTotal de transações dos 5 principais CNPJs:", total_top5)
print("Média por CNPJ:", total_top5 / 5)

print(top5_cnpj)

# calcular média de transações por CNPJ
media_transacoes = cnpj_transacoes["quantidade_transacoes"].mean()

print("Média de transações por CNPJ:", round(media_transacoes,2))

plt.figure(figsize=(10,6))

bars = plt.barh(
    top5_cnpj["CNPJ OK"],
    top5_cnpj["quantidade_transacoes"]
)

plt.title("Transações por CNPJs")
plt.ylabel("CNPJ")
plt.xlabel("Quantidade de transações")


for bar in bars:

    largura = bar.get_width()

    plt.text(largura + 0.2,bar.get_y() + bar.get_height()/2,f'{int(largura)}',va='center')

plt.axvline(media_transacoes,linestyle='--',label=f"Média: {media_transacoes:.1f}")

plt.legend()

plt.show()

print(df_master.columns)

df_compra_suspeita_fpgto = df_master[['transacao_id','forma_pagamento','compra_suspeita?']]

df_compra_suspeita_fpgto = df_compra_suspeita_fpgto[df_compra_suspeita_fpgto['compra_suspeita?'] == 'SIM']

df_compra_suspeita_fpgto = df_compra_suspeita_fpgto.groupby('compra_suspeita?')['transacao_id'].count().reset_index()

print(df_compra_suspeita_fpgto)

# 1. Filtramos apenas as compras suspeitas ('SIM')
df_suspeitas = df_master[df_master['compra_suspeita?'] == 'SIM']

# 2. Agrupamos por 'forma_pagamento' para contar as transações
df_plot = df_suspeitas.groupby('forma_pagamento')['transacao_id'].count().reset_index()

# --- CÁLCULO DA PORCENTAGEM ---
total_suspeitas = df_plot['transacao_id'].sum()
# Localiza o valor da contagem para 'À vista'
valor_a_vista = df_plot[df_plot['forma_pagamento'] == 'À vista']['transacao_id'].values[0]
porcentagem = (valor_a_vista / total_suspeitas) * 100
# ------------------------------

# 3. Criando o Gráfico de Barras
plt.figure(figsize=(8, 5))
barras = plt.bar(df_plot['forma_pagamento'], df_plot['transacao_id'], color='#1f77b4') # Azul mais sóbrio

# Adicionando os rótulos de dados (os números em cima de cada barra)
for barra in barras:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, yval + 1, int(yval), ha='center', va='bottom', fontsize=11, fontweight='bold')

# 4. ADICIONANDO A VARIAÇÃO/PORCENTAGEM (Destaque Central)
# Posicionamos o texto no meio do gráfico (eixo x=0.5, eixo y=metade da maior barra)
plt.text(0.5, max(df_plot['transacao_id'])/2, f'Representação À Vista: {porcentagem:.1f}%', fontsize=12, color='red', fontweight='bold', ha='center',bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=5))

# Customização visual
plt.title('Distribuição de Compras Suspeitas por Forma de Pagamento', fontsize=14, fontweight='bold')
plt.xlabel('Forma de Pagamento', fontsize=12)
plt.ylabel('Qtd Transações', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.ylim(0, max(df_plot['transacao_id']) * 1.2) # Dá folga no topo para o número não sumir

plt.tight_layout()
plt.show()


df_profi_suspeito_fpgto = df_master[['transacao_id','forma_pagamento','é suspeito?']]

df_profi_suspeito_fpgto = df_profi_suspeito_fpgto.groupby('é suspeito?')['transacao_id'].count().reset_index()

print(df_profi_suspeito_fpgto)

df_temp = df_master[df_master['é suspeito?'] == 'SIM']

# 2. Agrupamos por 'forma_pagamento' para contar as transações suspeitas
df_plot = df_temp.groupby('forma_pagamento')['transacao_id'].count().reset_index()

# --- CÁLCULO DA PORCENTAGEM ---
total_suspeitas = df_plot['transacao_id'].sum()
# Buscamos o valor de 'À vista' dentro do agrupamento
valor_a_vista = df_plot[df_plot['forma_pagamento'] == 'À vista']['transacao_id'].values[0]
porcentagem = (valor_a_vista / total_suspeitas) * 100
# ------------------------------

# 3. Criando o Gráfico de Barras
plt.figure(figsize=(8, 5))
barras = plt.bar(df_plot['forma_pagamento'], df_plot['transacao_id'], color='#1f77b4', edgecolor='black')

# Adicionando rótulos numéricos sobre as barras
for barra in barras:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, yval + 1, int(yval), 
             ha='center', va='bottom', fontsize=11, fontweight='bold')

# 4. ADICIONANDO O DESTAQUE DA PORCENTAGEM (Conforme sua imagem)
plt.text(0.5, total_suspeitas/2, f"Representação 'À vista': {porcentagem:.1f}%", 
         fontsize=12, color='red', fontweight='bold', ha='center',
         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=5))

# Customização visual final
plt.title('DISTRIBUIÇÃO DE TRANSACÕES SUSPEITAS POR PAGAMENTO', fontsize=12, fontweight='bold')
plt.ylabel('Qtd de Transações')
plt.ylim(0, max(df_plot['transacao_id']) * 1.3) # Folga no topo
plt.grid(axis='y', linestyle='--', alpha=0.3)

plt.tight_layout()
plt.show()

# Print para conferência no console
print(f"Total Suspeitos: {total_suspeitas}")
print(df_plot)


# df_cnpj_suspeito_fpgto = df_master[['transacao_id','forma_pagamento','CNPJ OK']]

# # df_plot = df_temp.groupby('forma_pagamento')['transacao_id'].count().reset_index()

# df_cnpj_suspeito_fpgto = df_cnpj_suspeito_fpgto.groupby('forma_pagamento')[['transacao_id','CNPJ OK']].count().reset_index()

# print(df_cnpj_suspeito_fpgto)

df_cnpj_fpgto = df_master[['transacao_id', 'forma_pagamento', 'CNPJ OK']]
df_cnpj_fpgto = df_cnpj_fpgto[df_cnpj_fpgto['CNPJ OK'].notna()]

# 2. Agrupamento por CNPJ (para ver a contagem de cada um)
# Queremos ver a barra de cada CNPJ no eixo X
df_plot = df_cnpj_fpgto.groupby('CNPJ OK')['transacao_id'].count().reset_index()

# Calculando a métrica para o destaque (À vista / Total)
total_geral = len(df_cnpj_fpgto)
total_a_vista = len(df_cnpj_fpgto[df_cnpj_fpgto['forma_pagamento'] == 'À vista'])
porcentagem = (total_a_vista / total_geral) * 100

# 3. Plotagem
plt.figure(figsize=(10, 6))
# Criando as barras (uma para cada CNPJ)
barras = plt.bar(df_plot['CNPJ OK'].astype(str), df_plot['transacao_id'], color='#2E86C1', edgecolor='black')

# Rótulos de dados (Quantidade em cima de cada barra)
for barra in barras:
    yval = barra.get_height()
    plt.text(barra.get_x() + barra.get_width()/2, yval + 0.5, int(yval), 
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# 4. DESTAQUE DOS 100% (Estilo caixa de texto centralizada)
# Usamos 'axes fraction' para fixar o texto no meio da área do gráfico
plt.text(0.5, 0.3, f"Representação 'À vista': {porcentagem:.0f}%", 
         fontsize=14, color='red', fontweight='bold', ha='center', va='center',
         transform=plt.gca().transAxes, # Faz o texto ficar fixo no meio do gráfico
         bbox=dict(facecolor='white', alpha=0.9, edgecolor='red', boxstyle='round,pad=0.8'))

# Customização do Layout
plt.title('CONTAGEM DE TRANSAÇÕES POR CNPJ (PAGAMENTO À VISTA)', fontsize=12, fontweight='bold')
plt.xlabel('CNPJ OK', fontsize=10)
plt.ylabel('Qtd Transações')
plt.xticks(rotation=45) # Rotaciona os CNPJs para não sobrepor
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.ylim(0, max(df_plot['transacao_id']) * 1.3)

plt.tight_layout()
plt.show()

df_cpf_cnpj_compras_suspeitas_renda_baixa = df_master[df_master['compra_suspeita?'] == 'SIM']

cpfs_renda_baixa_compra_alta = df_cpf_cnpj_compras_suspeitas_renda_baixa[['comprador_id']]

print(cpfs_renda_baixa_compra_alta)


df_cpf_cnpj_pagos_acima_40 = df_master[df_master['é suspeito?'] == "SIM"]

cpfs_pagos_acima_40 = df_cpf_cnpj_pagos_acima_40[['comprador_id']]
print(cpfs_pagos_acima_40)

print(type(cpfs_pagos_acima_40))


cnpj_suspeitos = df_master[df_master['CNPJ OK'].notna()]['CNPJ OK'].unique()

cnpj_suspeitos = pd.DataFrame(cnpj_suspeitos, columns=['comprador_id'])

print(type(cnpj_suspeitos))

print(cnpj_suspeitos)

cpf_cnpj_suspeitos_consolidados = pd.concat([cpfs_renda_baixa_compra_alta,cpfs_pagos_acima_40,cnpj_suspeitos],ignore_index=True)
print(cpf_cnpj_suspeitos_consolidados.head(10))

cpf_cnpj_suspeitos_consolidados = cpf_cnpj_suspeitos_consolidados.drop_duplicates()

# # 4. Exportando para CSV
# # Altere o caminho entre aspas para o diretório de sua preferência4

nome_arquivo = 'LISTA_CPFS_CNPJS_SUSPEITOS.csv'
caminho_diretorio = f'C:\MBA_DC_13\projeto_final_programacao_para_DS\projeto_09_lava_imovel\data\\{nome_arquivo}'

cpf_cnpj_suspeitos_consolidados.to_csv(caminho_diretorio, index=False, sep=';', encoding='utf-8-sig')

print(f"Arquivo exportado com sucesso para: {caminho_diretorio}")
print(f"Total de registros únicos: {len(cpf_cnpj_suspeitos_consolidados)}")