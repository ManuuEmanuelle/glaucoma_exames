import os
import json
import numpy as np


def calcular_medias(resultados):

    medias = {}

    modelos = sorted(
        set(resultado["modelo"] for resultado in resultados)
    )

    for modelo in modelos:

        resultados_modelo = [
            resultado
            for resultado in resultados
            if resultado["modelo"] == modelo
        ]

        if not resultados_modelo:
            continue

        bleus = []
        rouge1 = []
        rougeL = []
        similaridades = []

        # Notas do LLM-as-a-Judge
        notas_juiz = {}

        for resultado in resultados_modelo:

            metricas = resultado["metricas"]

            # BLEU
            if metricas.get("bleu") is not None:
                bleus.append(
                    metricas["bleu"]
                )

            # ROUGE-1
            if metricas.get("rouge"):
                rouge1.append(
                    metricas["rouge"]["rouge1"]["f1"]
                )

                # ROUGE-L
                rougeL.append(
                    metricas["rouge"]["rougeL"]["f1"]
                )

            # Similaridade semântica
            if metricas.get("similaridade_semantica") is not None:
                similaridades.append(
                    metricas["similaridade_semantica"]
                )

            # LLM-as-a-Judge
            juiz = metricas.get("llm_juiz")

            if juiz:

                for chave, valor in juiz.items():

                    # Considera somente valores numéricos
                    if isinstance(valor, (int, float)):

                        if chave not in notas_juiz:
                            notas_juiz[chave] = []

                        notas_juiz[chave].append(valor)

        medias_modelo = {}

        if bleus:
            medias_modelo["bleu"] = float(
                np.mean(bleus)
            )

        if rouge1:
            medias_modelo["rouge1_f1"] = float(
                np.mean(rouge1)
            )

        if rougeL:
            medias_modelo["rougeL_f1"] = float(
                np.mean(rougeL)
            )

        if similaridades:
            medias_modelo["similaridade_semantica"] = float(
                np.mean(similaridades)
            )

        # Médias das avaliações do LLM juiz
        if notas_juiz:

            medias_modelo["llm_juiz"] = {}

            for chave, valores in notas_juiz.items():

                medias_modelo["llm_juiz"][chave] = float(
                    np.mean(valores)
                )

        medias[modelo] = medias_modelo

    return medias


def exibir_resultados(resultados):
    """
    Exibe as métricas de cada paciente e modelo.
    """

    print("\n")
    print("=" * 70)
    print("RESULTADOS DAS AVALIAÇÕES")
    print("=" * 70)

    for resultado in resultados:

        paciente = resultado["paciente"]
        modelo = resultado["modelo"]
        metricas = resultado["metricas"]

        print("\n" + "-" * 70)

        print(f"Paciente: {paciente}")
        print(f"Modelo: {modelo}")

        # BLEU
        bleu = metricas.get("bleu")

        if bleu is not None:
            print(f"BLEU: {bleu:.4f}")

        # ROUGE
        rouge = metricas.get("rouge")

        if rouge:

            print(
                f"ROUGE-1 F1: "
                f"{rouge['rouge1']['f1']:.4f}"
            )

            print(
                f"ROUGE-L F1: "
                f"{rouge['rougeL']['f1']:.4f}"
            )

        # Similaridade
        similaridade = metricas.get(
            "similaridade_semantica"
        )

        if similaridade is not None:

            print(
                f"Similaridade semântica: "
                f"{similaridade:.4f}"
            )

        # LLM-as-a-Judge
        print("\nLLM-AS-A-JUDGE:")

        juiz = metricas.get("llm_juiz")

        if juiz is None:

            print(
                "  Avaliação não disponível."
            )

        else:

            for chave, valor in juiz.items():

                if isinstance(valor, (int, float)):

                    print(
                        f"  {chave}: {valor}"
                    )

                else:

                    print(
                        f"  {chave}: {valor}"
                    )


def exibir_medias(medias):
    """
    Exibe as médias das métricas por modelo.
    """

    print("\n")
    print("=" * 70)
    print("MÉDIAS DAS MÉTRICAS")
    print("=" * 70)

    for modelo, valores in medias.items():

        print("\n" + "-" * 70)

        print(f"Modelo: {modelo}")

        if "bleu" in valores:

            print(
                f"BLEU médio: "
                f"{valores['bleu']:.4f}"
            )

        if "rouge1_f1" in valores:

            print(
                f"ROUGE-1 F1 médio: "
                f"{valores['rouge1_f1']:.4f}"
            )

        if "rougeL_f1" in valores:

            print(
                f"ROUGE-L F1 médio: "
                f"{valores['rougeL_f1']:.4f}"
            )

        if "similaridade_semantica" in valores:

            print(
                f"Similaridade semântica média: "
                f"{valores['similaridade_semantica']:.4f}"
            )

        if "llm_juiz" in valores:

            print("\nLLM-AS-A-JUDGE:")

            for chave, valor in valores["llm_juiz"].items():

                print(
                    f"  {chave}: {valor:.2f}"
                )


def salvar_resultados(
    resultados,
    medias,
    resultados_folder
):
    """
    Salva os resultados individuais e as médias
    em arquivos JSON.
    """

    pasta_avaliacao = os.path.join(
        resultados_folder,
        "avaliacao"
    )

    os.makedirs(
        pasta_avaliacao,
        exist_ok=True
    )

    # Resultados individuais
    resultados_path = os.path.join(
        pasta_avaliacao,
        "resultados_avaliacao.json"
    )

    with open(
        resultados_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            resultados,
            f,
            indent=4,
            ensure_ascii=False
        )

    # Médias
    medias_path = os.path.join(
        pasta_avaliacao,
        "medias_metricas.json"
    )

    with open(
        medias_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            medias,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("\n")
    print("=" * 70)
    print("RESULTADOS SALVOS")
    print("=" * 70)

    print(
        f"\nResultados individuais:"
        f"\n{resultados_path}"
    )

    print(
        f"\nMédias:"
        f"\n{medias_path}"
    )