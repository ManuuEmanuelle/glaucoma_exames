import os
import json

from avaliacao.metricas import calcular_metricas


def carregar_txt(path):


    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def extrair_numero_paciente(nome):

    numeros = "".join(caractere for caractere in nome if caractere.isdigit())

    return int(numeros) if numeros else 0


def salvar_resultados_parciais(resultados,resultados_folder):

    pasta_avaliacao = os.path.join(resultados_folder,"avaliacao")

    os.makedirs(pasta_avaliacao,exist_ok=True)

    caminho = os.path.join(pasta_avaliacao,"resultados_avaliacao.json")

    with open(caminho,"w",encoding="utf-8") as f:

        json.dump(resultados,f,indent=4,ensure_ascii=False)


def avaliar_laudo(paciente,modelo,laudo_referencia_path,laudo_gerado_path):


    laudo_referencia = carregar_txt(laudo_referencia_path)

    laudo_gerado = carregar_txt(laudo_gerado_path)

    metricas = calcular_metricas(laudo_referencia,laudo_gerado)

    return {
        "paciente": paciente,
        "modelo": modelo,
        "metricas": metricas
    }


def avaliar_laudos(referencia_folder,resultados_folder,modelos):

    resultados = []

    caminho_resultados = os.path.join(resultados_folder,"avaliacao","resultados_avaliacao.json")

    if os.path.exists(caminho_resultados):

        with open(caminho_resultados,"r",encoding="utf-8") as f:

            resultados = json.load(f)

    avaliados = {(resultado["paciente"],resultado["modelo"]) for resultado in resultados}

    for modelo in modelos:

        modelo_folder = os.path.join(resultados_folder,modelo)

        if not os.path.exists(modelo_folder):

            print(f"[{modelo}] Pasta de resultados não encontrada.")

            continue

        pacientes = [pasta for pasta in os.listdir(modelo_folder) if os.path.isdir(os.path.join(modelo_folder, pasta))]

        pacientes.sort(key=extrair_numero_paciente)

        for paciente in pacientes:

            if (paciente, modelo) in avaliados:

                print(
                    f"[{modelo}] {paciente}: "
                    "avaliação já realizada."
                )

                continue

            laudo_referencia_path = os.path.join(referencia_folder,f"{paciente}_laudo.txt")

            laudo_gerado_path = os.path.join(modelo_folder,paciente,"laudo.txt")

            if not os.path.exists(laudo_referencia_path):

                print(
                    f"[{modelo}] {paciente}: "
                    "laudo de referência não encontrado."
                )

                continue

            if not os.path.exists(laudo_gerado_path):

                print(
                    f"[{modelo}] {paciente}: "
                    "laudo gerado não encontrado."
                )

                continue

            print(f"[{modelo}] {paciente}: avaliando...")

            resultado = avaliar_laudo(paciente,modelo,laudo_referencia_path,laudo_gerado_path)

            resultados.append(resultado)

            avaliados.add((paciente, modelo))

            salvar_resultados_parciais(resultados,resultados_folder)

            print(
                f"[{modelo}] {paciente}: "
                "avaliação salva."
            )

    return resultados