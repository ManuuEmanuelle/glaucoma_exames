import os

from avaliacao.metricas import calcular_metricas


def carregar_txt(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()


def avaliar_laudo(
    paciente,
    modelo,
    laudo_referencia_path,
    laudo_gerado_path
):

    laudo_referencia = carregar_txt(
        laudo_referencia_path
    )

    laudo_gerado = carregar_txt(
        laudo_gerado_path
    )

    metricas = calcular_metricas(
        laudo_referencia,
        laudo_gerado
    )

    return {
        "paciente": paciente,
        "modelo": modelo,
        "metricas": metricas
    }


def avaliar_laudos(
    referencia_folder,
    resultados_folder,
    modelos
):

    resultados = []

    for modelo in modelos:

        modelo_folder = os.path.join(
            resultados_folder,
            modelo
        )

        if not os.path.exists(modelo_folder):
            print(
                f"[{modelo}] Pasta de resultados não encontrada."
            )
            continue

        pacientes = [
            pasta
            for pasta in os.listdir(modelo_folder)
            if os.path.isdir(
                os.path.join(modelo_folder, pasta)
            )
        ]

        pacientes.sort(
            key=lambda x: int(
                "".join(
                    filtro
                    for filtro in x
                    if filtro.isdigit()
                ) or 0
            )
        )

        for paciente in pacientes:

            laudo_referencia_path = os.path.join(
                referencia_folder,
                paciente,
                "laudo.txt"
            )

            laudo_gerado_path = os.path.join(
                modelo_folder,
                paciente,
                "laudo.txt"
            )

            if not os.path.exists(
                laudo_referencia_path
            ):
                print(
                    f"[{modelo}] {paciente}: "
                    "laudo de referência não encontrado."
                )
                continue

            if not os.path.exists(
                laudo_gerado_path
            ):
                print(
                    f"[{modelo}] {paciente}: "
                    "laudo gerado não encontrado."
                )
                continue

            print(
                f"[{modelo}] {paciente}: avaliando..."
            )

            resultado = avaliar_laudo(
                paciente,
                modelo,
                laudo_referencia_path,
                laudo_gerado_path
            )

            resultados.append(resultado)

    return resultados