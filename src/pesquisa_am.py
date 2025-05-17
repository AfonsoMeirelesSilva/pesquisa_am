import pandas as pd

# Carregar o arquivo Excel
pesquisa_geral = pd.read_excel('PesquisaAmazonas.xlsx')

# === Corrigir espaços nos nomes das colunas ===
pesquisa_geral.columns = pesquisa_geral.columns.str.strip()


# === Definir as colunas de interesse ===
colunas_para_analisar = [
    'Estim1_pref','Espontanea',  'Estim2_pref', 'Estim3_pref', 'Estim4_pref', 'Estim5_pref', 'Estim6',
    'Estim7', 'Estim8', 'Estim9', 'Estim10', 'Estim11', 'Estim12', 'Estim13', 'Estim14', 'Rejeicao',
    'Dep_estadual_esp', 'Dep_federal_esp', 'DeputadoFederal', 'Senado_esp_1', 'Senado_esp_2',
    'Estim_senado_1_pref', 'Estim_senado_1_2_pref', 'Estim_senado_2_pref', 'Estim_senado_2_2_pref', 'Estim_senado_3_pref', 'Estim_senado_3_2_pref', 'Rejeicao_senado',
    'Como_o_a_sr_a_aval_efeito_da_sua_Cidade', 'AvaliacaoGov', 'AvaliacaoPresidente',
    'Avaliacao_saude', 'Avaliacao_seguranca', 'Avaliacao_educacao', 'Avaliacao_transporte',
    'Avaliacao_asfaltamento', 'Avaliacao_limpeza_001', 'Avaliacao_drenagem', 'Avaliacao_infraestrutura',
    'Aprova_desaprova', 'Pq_aprova', 'Por_que_o_a_sr_a_DESAPROVA', 'Problemas_Manaus'
]

# === Filtros ===
manaus = pesquisa_geral[pesquisa_geral['Municipio'].str.lower() == 'manaus']
interior = pesquisa_geral[pesquisa_geral['Municipio'].str.lower() != 'manaus']

municipios = interior['Municipio'].unique()
print(municipios) 
print(len(municipios))


 
print(municipios.len)
# === AQUI COMEÇA A PARADA ===

def calcular_percentual(planilha, nome_grupo):
    tabelas = {}

    for coluna in colunas_para_analisar:
        contagem = planilha[coluna].value_counts(dropna=True).reset_index()
        contagem.columns = [coluna, 'Quantidade']
        contagem['Percentual'] = contagem['Quantidade'] / contagem['Quantidade'].sum()
        contagem['Grupo'] = nome_grupo
        tabelas[coluna] = contagem
    return tabelas

def calcular_percentual_interior(planilha, nome_grupo):
    tabelas = {}

    for coluna in colunas_para_analisar:
        contagem = planilha[coluna].value_counts(dropna=True).reset_index()
        contagem.columns = [coluna, 'Quantidade']
        print(contagem)
        print(contagem['Quantidade'].sum())
        contagem['Percentual'] = contagem['Quantidade'] / contagem['Quantidade'].sum()
        contagem['Grupo'] = nome_grupo
        tabelas[coluna] = contagem
    return tabelas

tabelas_interior = calcular_percentual_interior(interior, 'Interior')
tabelas_manaus = calcular_percentual(manaus, 'Manaus')

tabelas_amazonas = {}
for coluna in colunas_para_analisar:
    interior_df = tabelas_interior[coluna]
    print(interior_df)
    manaus_df = tabelas_manaus[coluna]
    
    combinado = pd.merge(
        interior_df[[coluna, 'Percentual']],
        manaus_df[[coluna, 'Percentual']],
        how='outer',
        on=coluna,
        suffixes=('_Interior', '_Manaus')
    )
        
    combinado = combinado.fillna(0)   
    combinado['Percentual_Amazonas'] = (combinado['Percentual_Manaus'] * 0.53) + (combinado['Percentual_Interior'] * 0.47)
    
    tabelas_amazonas[coluna] = combinado
    
# === Salvar no Excel (uma aba para cada variável) ===
print(tabelas_amazonas.items())
with pd.ExcelWriter('Resultado_Percentuais_Amazonas.xlsx') as writer:
    for coluna, tabela in tabelas_amazonas.items():
        
        tabela.to_excel(writer, sheet_name=coluna[:30], index=False)
print('=)')