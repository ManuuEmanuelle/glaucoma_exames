import os
import fitz

from .extracao import extrair_texto_exame, extrair_texto_laudo

from .classificadores import classificar_campos

from .arquivos import salvar_json_exames


def processar_pdf(pdf_path,paciente,paginas_exame,exames_json_folder,laudos_texto_folder):

    doc = fitz.open(pdf_path)

    exames = extrair_texto_exame(doc,paginas_exame)

    for exame in exames:

        dados = exame["dados"]

        dados_classificados = classificar_campos(dados)

        exame["dados"] = dados_classificados

    salvar_json_exames(exames,paciente,exames_json_folder)

    extrair_texto_laudo(doc,laudos_texto_folder,paciente)

    doc.close()


def processar_pdfs(pdf_folder,exames_json_folder,laudos_texto_folder):

    os.makedirs(exames_json_folder,exist_ok=True)

    os.makedirs(laudos_texto_folder,exist_ok=True)

    arquivos_pdf = [arquivo for arquivo in os.listdir(pdf_folder) if arquivo.lower().endswith(".pdf")]

    arquivos_pdf.sort()

    for i, arquivo in enumerate(arquivos_pdf,start=1):

        paciente = f"paciente_{i}"

        json_path = os.path.join(exames_json_folder,f"{paciente}.json")

        if os.path.exists(json_path):

            print(f"{paciente}: PDF já processado.")

            continue

        pdf_path = os.path.join(pdf_folder,arquivo)

        doc = fitz.open(pdf_path)

        num_paginas = len(doc)

        doc.close()

        if num_paginas == 3:
            paginas_exame = [0, 1]

        elif num_paginas == 2:
            paginas_exame = [0]

        else:

            print(
                f"PDF inválido: {arquivo} "
                f"({num_paginas} páginas)"
            )

            continue

        processar_pdf(pdf_path,paciente,paginas_exame,exames_json_folder,laudos_texto_folder)

        print(
            f"{paciente} processado com "
            f"{len(paginas_exame)} exame(s)"
        )