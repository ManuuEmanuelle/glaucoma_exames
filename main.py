import os

from processamento.processamento_exames import processar_pdfs
from geracao.processamento import processar_exames
from avaliacao.avaliar_laudos import avaliar_laudos
from avaliacao.resultados import calcular_medias, exibir_resultados, exibir_medias,salvar_resultados


PDF_FOLDER = "./dados/pdfs"
EXAMES_JSON_FOLDER = "./dados/exames_json"
LAUDOS_TEXTO_FOLDER = "./dados/laudos_texto"
RESULTADOS_FOLDER = "./resultados"

MODELOS = ["gemini","gpt"]


def main():

    print("=" * 60)
    print("PIPELINE DE GERAÇÃO DE LAUDOS DE GLAUCOMA")
    print("=" * 60)

    print("\n[1/3] Processando exames...")

    processar_pdfs(PDF_FOLDER,EXAMES_JSON_FOLDER,LAUDOS_TEXTO_FOLDER)

    print("\n[2/3] Gerando laudos...")

    for modelo in MODELOS:

        print(f"\nModelo: {modelo}")

        output_folder = os.path.join(RESULTADOS_FOLDER,modelo)

        processar_exames(EXAMES_JSON_FOLDER,output_folder,modelo)

    print("\n[3/3] Avaliando laudos...")

    resultados = avaliar_laudos(referencia_folder=LAUDOS_TEXTO_FOLDER,resultados_folder=RESULTADOS_FOLDER,modelos=MODELOS)

    print(f"\nLaudos avaliados: {len(resultados)}")

    exibir_resultados(resultados)

    medias = calcular_medias(resultados)

    exibir_medias(medias)

    salvar_resultados(resultados,medias,RESULTADOS_FOLDER)

    print("\n" + "=" * 60)
    print("PIPELINE CONCLUÍDO")
    print("=" * 60)


if __name__ == "__main__":
    main()