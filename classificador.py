from openai import OpenAI
import pandas as pd
import time

client = OpenAI(
  api_key="CHAVE DA API"
  )

# Critérios de inclusão/exclusão
###criterios""
# Função para classificar artigo
def classificar(titulo, ano, resumo, keywords):
    prompt = f"""
Você é um pesquisador e especialista em analisar artigos científicos. De acordo com os seguintes critérios de inclusão e exclusão leia o arquivo e de forma cuidadosa inclua ou exclua os artigos:

Critérios de inclusão:
1I - Publicações científicas: Artigos científicos publicados em conferências ou revistas;
2I - Ano de publicação: Estudos publicados nos últimos 5 anos (2020-2025). considere apenas {ano} como ano de publicação;
3I - Idiomas: Inglês;
4I - Estudos que tenham o texto completo disponível;
5I - Estudos que abordam explicitamente o uso ou a aplicação de eBPF (Extended Berkeley Packet Filter) no contexto de redes móveis de quinta geração (5G), Beyond 5G (B5G), sexta geração (6G) ou redes móveis de próxima geração.
6I - Estudos cujo resumo mencione eBPF (ou tecnologias relacionadas), mas não façam referência explícita a tecnologias de rede como 5G, B5G, 6G ou NGN, serão incluídos com ressalva somente se ao menos uma dessas tecnologias de rede estiver presente nas palavras-chave.
Da mesma forma, caso o resumo mencione uma dessas tecnologias de rede, mas não cite explicitamente eBPF, o estudo também será incluído com ressalva, desde que eBPF (ou tecnologias relacionadas) esteja presente nas palavras-chave.

Critérios de exclusão:
1E - Artigos duplicados, mesmo que estejam em bases diferentes. Mantenha apenas um;
2E - Estudos que não abordam explicitamente eBPF, 5G, 6G, B5G ou redes móveis de próxima geração;
3E - Publicação que não sejam de caráter científico: Artigos de opinião e blogs;
4E - Artigos que não sejam completos (full paper);
5E - Artigos com mais de 5 anos de publicação. Considere apenas o ano de publicação especificado;
6E - Artigos com idiomas que não seja Inglês;
7E - Artigos sem abstract.
8E - Exclusão em caso de ausência de correlação entre resumo e palavras-chave:
Estudos cujo resumo não mencione eBPF (ou tecnologias relacionadas) nem tecnologias de rede (5G, B5G, 6G ou NGN) serão excluídos, mesmo que essas tecnologias apareçam apenas nas palavras-chave.
Apenas será feita uma inclusão com ressalva se houver uma correlação cruzada mínima, ou seja:
- eBPF no resumo e uma tecnologia de rede nas palavras-chave, ou
- uma tecnologia de rede no resumo e eBPF nas palavras-chave.

Título: {titulo}
Ano de publicação: {ano}
Resumo: {resumo}
Palavras-chave: {keywords}


Se o artigo deve ser excluído, responda com:  
Resposta: NÃO
Justificativa: (responda com o código correspondente a exclusão)

Se o artigo deve ser incluído, responda com:  
Resposta: SIM  
Justificativa: (explique brevemente)
"""
    
    completion = client.chat.completions.create(
      model="gpt-4.1-mini",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )

    texto = completion.choices[0].message.content.strip()
    return texto

df = pd.read_csv("C:/Users/joses/Desktop/mapeamento/artigos.csv", sep=";")

respostas = []
justificativas = []

for index, row in df.iterrows():
    try:
        resultado = classificar(row['title'], row['year'], row['abstract'], row['keywords'])

        if "SIM" in resultado.upper():
            respostas.append("SIM")
            justificativa = resultado.split("Justificativa:")[1].strip() if "Justificativa:" in resultado else ""
            justificativas.append(justificativa)
        else:
            respostas.append("NÃO")
            justificativa = resultado.split("Justificativa:")[1].strip() if "Justificativa:" in resultado else ""
            justificativas.append(justificativa)
        
        time.sleep(1.2)  # controle de taxa
    except Exception as e:
        print(f"Erro na linha {index}: {e}")
        respostas.append("ERRO")
        justificativas.append("")

# Adicionando os resultados ao DataFrame
df['Incluir'] = respostas
df['Justificativa'] = justificativas

# Salvando o novo CSV
df.to_csv("C:/Users/joses/Desktop/mapeamento/final.csv", sep=";", index=False)
