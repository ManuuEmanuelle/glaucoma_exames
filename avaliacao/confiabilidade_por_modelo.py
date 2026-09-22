from collections import defaultdict


def calcular_media_confiabilidade(
    resultados
):

    valores = defaultdict(list)

    for resultado in resultados:

        modelo = resultado["modelo"]

        confiabilidade = (
            resultado
            ["avaliacoes"]
            ["confiabilidade_laudo_gerado"]
            ["confiabilidade"]
        )

        if isinstance(
            confiabilidade,
            str
        ):

            confiabilidade = (
                confiabilidade
                .replace("%", "")
            )

        confiabilidade = float(
            confiabilidade
        )

        valores[modelo].append(
            confiabilidade
        )

    medias = {}

    for modelo, notas in valores.items():

        medias[modelo] = (
            sum(notas) / len(notas)
        )

    return medias