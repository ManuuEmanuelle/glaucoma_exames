from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from avaliacao.llm_judge import avaliar_com_llm_juiz

modelo_semantico = SentenceTransformer("all-MiniLM-L6-v2")

def calcular_bleu(referencia, gerado):
    referencia_tokens = referencia.split()
    gerado_tokens = gerado.split()

    score = sentence_bleu([referencia_tokens], gerado_tokens)
    return score

def calcular_rouge(referencia, gerado):

    scorer = rouge_scorer.RougeScorer(["rouge1", "rougeL"],use_stemmer=True)

    scores = scorer.score(referencia, gerado)

    return {
        "rouge1": {
            "precision": scores["rouge1"].precision,
            "recall": scores["rouge1"].recall,
            "f1": scores["rouge1"].fmeasure
        },
        "rougeL": {
            "precision": scores["rougeL"].precision,
            "recall": scores["rougeL"].recall,
            "f1": scores["rougeL"].fmeasure
        }
    }

def calcular_similaridade_semantica(referencia, gerado):

    embedding_referencia = modelo_semantico.encode([referencia])
    embedding_gerado = modelo_semantico.encode([gerado])

    similaridade = cosine_similarity(embedding_referencia,embedding_gerado)[0][0]

    return float(similaridade)

def calcular_metricas(referencia, gerado):

    bleu = calcular_bleu(referencia, gerado)

    rouge = calcular_rouge(referencia,gerado)

    similaridade = calcular_similaridade_semantica(referencia,gerado)

    avaliacao_juiz = avaliar_com_llm_juiz(dados_referencia=referencia,laudo_texto=gerado)

    return {
        "bleu": float(bleu),
        "rouge": rouge,
        "similaridade_semantica": similaridade,
        "llm_juiz": avaliacao_juiz
    }