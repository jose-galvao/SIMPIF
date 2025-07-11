# SIMPIF 2025

Esse repositório contém os arquivos com a lista de artigos e o código em Python utilizados no artigo **Uso eBPF em Redes 5G: Um Estudo de Mapeamento Sistemático Assistido por IA**.

O arquivo `LISTA-FINAL-ARTIGOS.csv` estão inclusos todos os artigos que foram selecionados para fazer parte dos resultados da pesquisa. Os campos presentes são:
`base`: Base de dado de origem do artigo;
`title`: Título do artigo;
`year`: Ano de publicação do artigo;
`author`: Autores do artigo.

## Como utilizar o `classificador.py`?

### 1- Instale as bibliotecas necessárias

```
pip install openai pandas
```

### 2- Gere sua chave de API da OpenAI

1. Acesse [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys)
2. Clique em **"Create new secret key"**
3. Copie a chave gerada (começa com `sk-...`)

No bloco de código abaixo você deve colar a chave gerada. 

```
client = OpenAI(
api_key="CHAVE DA API"
)
```

### 3- Modelo do ChatGPT

A OpenAI sempre adiciona novos modelos mais complexos e mais robustos que podem ser utilizados. Para alterar o modelo e testar modelos mais recentes do ChatGPT, basta alterar a seguinte linha com o modelo desejado:

```
model="gpt-4.1-mini"
```
O modelo utilizado para claissificação dos artigos desse trabalho foi o gpt-4.1-mini.

### 4- Arquivo CSV

Na linha de código abaixo deve ser indicado o caminho que está o arquivo CSV com os artigos que o ChatGPT vai classificar:

``` 
df = pd.read_csv("artigos.csv", sep=";")
```
As colunas obrigatórias no CSV para o funcionamento correto do código são: `title`, `year`, `abstract` e `keywords`.

Após a classificação será criado duas novas colunas `Incluir` e `Justificativa`. A pasta onde o novo arquivo CSV será salvo deve ser indicado na linha abaixo.

```
df.to_csv("final.csv", sep=";", index=False)
```

### Observações
Esse código pode ser utilizado para pesquisas em outros contextos. Sendo necessário modificar o conteúdo da variável `prompt` para o contexto da sua pesquisa.


