# Detecção e Geração Automatizada de Laudos de Campimetria

Projeto de pesquisa para **processamento de exames de campimetria computadorizada e geração automatizada de laudos oftalmológicos utilizando modelos de linguagem (LLMs)**, com foco na análise de informações relacionadas ao glaucoma.

O projeto realiza o processamento dos exames, extração e estruturação dos dados, geração dos laudos por diferentes modelos de linguagem e avaliação automática dos resultados.

## Objetivos

O projeto tem como principais objetivos:

- Processar exames de campimetria computadorizada armazenados em arquivos PDF;
- Extrair informações textuais e estruturadas dos exames;
- Identificar e organizar dados de diferentes estratégias de campimetria;
- Gerar laudos oftalmológicos utilizando modelos de linguagem;
- Comparar os laudos gerados com laudos de referência;
- Avaliar a qualidade dos textos gerados utilizando métricas automáticas;
- Utilizar uma LLM como avaliadora dos laudos gerados.

## Pipeline

O funcionamento do projeto é dividido em três etapas principais:

```text
PDF dos exames
      │
      ▼
Processamento e extração
      │
      ▼
Dados estruturados em JSON
      │
      ▼
Geração dos laudos
      │
      ├── Gemini 2.5 Flash
      │
      └── GPT-OSS-20B
      │
      ▼
Laudos gerados
      │
      ▼
Avaliação
      │
      ├── BLEU
      ├── ROUGE-1
      ├── ROUGE-L
      ├── Similaridade semântica
      └── LLM-as-a-Judge
      │
      ▼
Resultados em JSON
```

## Estrutura do projeto

```text
glaucoma_exames/
│
├── dados/
│   ├── pdfs/
│   ├── exames_json/
│   └── laudos_texto/
│
├── resultados/
│   ├── gemini/
│   ├── gpt/
│   └── avaliacao/
│
├── processamento/
│   ├── __init__.py
│   ├── arquivos.py
│   ├── classificadores.py
│   ├── conversores.py
│   ├── extracao.py
│   └── processamento_exames.py
│
├── geracao/
│   ├── __init__.py
│   ├── gerador.py
│   ├── leitura.py
│   ├── modelos.py
│   ├── processamento.py
│   └── prompt_laudo.py
│
├── avaliacao/
│   ├── __init__.py
│   ├── metricas.py
│   ├── avaliar_laudos.py
│   ├── llm_juiz.py
│   ├── prompt_llm_juiz.py
│   └── resultados.py
│
├── .env
├── .gitignore
├── main.py
└── README.md
```

## Tecnologias

- Python
- PyMuPDF (`fitz`)
- Google Generative AI
- Groq
- NLTK
- ROUGE Score
- Sentence Transformers
- Scikit-learn
- NumPy
- python-dotenv

## Modelos utilizados

### Geração dos laudos

Atualmente são utilizados dois modelos para geração dos laudos:

- **Gemini 2.5 Flash**
- **GPT-OSS-20B**

O projeto também possui experimentos anteriores com outros modelos, como o Llama, que não faz parte da execução atual do pipeline.

### LLM-as-a-Judge

Para a avaliação dos laudos é utilizado o:

- **GPT-OSS-120B**

O modelo atua exclusivamente como avaliador, comparando o laudo gerado com o laudo de referência.

## Avaliação

Os laudos gerados são comparados aos laudos de referência utilizando diferentes abordagens.

### BLEU

Avalia a sobreposição de n-gramas entre o texto de referência e o texto gerado.

### ROUGE

São utilizadas as métricas:

- ROUGE-1
- ROUGE-L

Para ambas são considerados:

- Precision
- Recall
- F1-score

### Similaridade semântica

A similaridade semântica é calculada utilizando embeddings produzidos pelo modelo:

```text
all-MiniLM-L6-v2
```

A comparação é realizada por similaridade de cosseno.

### LLM-as-a-Judge

Uma LLM é utilizada para avaliar o laudo gerado considerando critérios definidos no prompt de avaliação.

A avaliação considera aspectos como:

- fidelidade ao conteúdo clínico;
- preservação do significado das informações;
- cumprimento das restrições estabelecidas;
- adequação do formato do laudo;
- confiabilidade técnica.

As notas atribuídas pelo juiz são utilizadas para produzir uma avaliação quantitativa dos resultados.

## Organização dos resultados

Após a execução do pipeline, os laudos gerados são organizados por modelo:

```text
resultados/
├── gemini/
│   ├── paciente_1/
│   │   └── laudo.txt
│   ├── paciente_2/
│   │   └── laudo.txt
│   └── ...
│
├── gpt/
│   ├── paciente_1/
│   │   └── laudo.txt
│   ├── paciente_2/
│   │   └── laudo.txt
│   └── ...
│
└── avaliacao/
    ├── resultados_avaliacao.json
    └── medias_metricas.json
```

O arquivo `resultados_avaliacao.json` contém as métricas obtidas para cada paciente e modelo.

O arquivo `medias_metricas.json` contém as médias das métricas calculadas para cada modelo.

## Configuração

### 1. Clonar o repositório

```bash
git clone URL_DO_REPOSITORIO
cd glaucoma_exames
```

### 2. Criar o ambiente virtual

```bash
python3 -m venv venv
```

Ative o ambiente:

**Linux/macOS:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 3. Instalar as dependências

Caso exista um `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 4. Configurar as chaves de API

Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_gemini
GROQ_API_KEY=sua_chave_groq
```

As chaves de API não devem ser adicionadas ao repositório.

## Execução

Com o ambiente virtual ativado, execute:

```bash
python main.py
```

O pipeline realizará automaticamente:

```text
1. Processamento dos PDFs
2. Geração dos laudos
3. Avaliação dos laudos
4. Exibição das métricas
5. Cálculo das médias
6. Salvamento dos resultados
```

## Dados

Os exames utilizados pelo projeto são provenientes de exames de campimetria computadorizada.

Os arquivos PDF devem ser colocados em:

```text
dados/pdfs/
```

Durante o processamento, os dados estruturados dos exames são armazenados em:

```text
dados/exames_json/
```

Os laudos de referência são armazenados em:

```text
dados/laudos_texto/
```

Os dados utilizados no projeto devem respeitar os requisitos de privacidade e proteção de dados aplicáveis à pesquisa.

## Resultados esperados

Ao final da execução, o projeto produz:

- laudos gerados pelos modelos de linguagem;
- métricas de avaliação para cada laudo;
- avaliações realizadas pelo LLM-as-a-Judge;
- médias das métricas por modelo;
- arquivos JSON contendo os resultados da avaliação.

## Observações

O projeto possui finalidade de **pesquisa e avaliação experimental de modelos de linguagem aplicados à geração de textos relacionados a exames oftalmológicos**.

Os laudos gerados automaticamente não devem ser utilizados como substitutos de avaliação ou diagnóstico médico profissional.
