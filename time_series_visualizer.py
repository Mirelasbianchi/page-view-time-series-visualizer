# ===============================
# Bibliotecas necessárias
# ===============================
import pandas as pd               # Manipulação de dados
import matplotlib.pyplot as plt   # Visualização de dados (gráficos básicos)
import seaborn as sns             # Visualização mais estilizada (baseado no matplotlib)

# ===============================
# Importar e preparar os dados
# ===============================
# Lê o arquivo CSV com os dados de visualizações do fórum
# - parse_dates=['date']: converte a coluna 'date' em tipo datetime
# - index_col='date': define a coluna 'date' como índice (útil para séries temporais)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# ===============================
# Remover outliers
# ===============================
# Calcula limites inferior (2,5%) e superior (97,5%) com base nos quantis
lower = df['value'].quantile(0.025)
upper = df['value'].quantile(0.975)

# Filtra o DataFrame mantendo apenas os valores dentro desses limites
df = df[(df['value'] >= lower) & (df['value'] <= upper)]


# ===============================
# Função 1: Line Plot
# ===============================
def draw_line_plot():
    # Cria a figura e os eixos
    fig, ax = plt.subplots(figsize=(12,6))
    
    # Gráfico de linha com datas no eixo X e visualizações no eixo Y
    ax.plot(df.index, df['value'], color='red')
    
    # Adiciona título e rótulos
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    
    # Salva a figura em arquivo PNG
    fig.savefig("line_plot.png")
    
    # Retorna a figura (útil para testes automáticos)
    return fig


# ===============================
# Função 2: Bar Plot
# ===============================
def draw_bar_plot():
    # Copia o DataFrame original
    df_bar = df.copy()
    
    # Cria colunas auxiliares para ano e mês
    df_bar['year'] = df_bar.index.year
    df_bar['month'] = df_bar.index.month
    
    # Agrupa por ano e mês e calcula a média das visualizações
    df_grouped = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    
    # Cria gráfico de barras com anos no eixo X e meses como grupos
    fig = df_grouped.plot(kind='bar', figsize=(12,6)).figure
    
    # Personaliza rótulos e legenda
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(
        title='Months',
        labels=['Jan','Feb','Mar','Apr','May','Jun',
                'Jul','Aug','Sep','Oct','Nov','Dec']
    )
    
    # Salva a figura em arquivo PNG
    fig.savefig("bar_plot.png")
    
    return fig


# ===============================
# Função 3: Box Plots
# ===============================
def draw_box_plot():
    # Copia o DataFrame original
    df_box = df.copy()
    
    # Cria colunas auxiliares para ano e mês (abreviado, ex: Jan, Feb, etc.)
    df_box['year'] = df_box.index.year
    df_box['month'] = df_box.index.strftime('%b')
    
    # Define a ordem correta dos meses (para evitar ordem alfabética)
    months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Cria figura com dois gráficos lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(15,6))
    
    # Primeiro boxplot: tendência ao longo dos anos
    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    # Segundo boxplot: sazonalidade ao longo dos meses
    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1], order=months_order)
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")
    
    # Salva a figura em arquivo PNG
    fig.savefig("box_plot.png")
    
    return fig
