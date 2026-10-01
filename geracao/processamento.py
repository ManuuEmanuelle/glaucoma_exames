import os
import json
import re

from .leitura import carregar_json_exame
from .gerador import gerar_laudo


def extrair_numero_paciente(nome):
    numeros = re.findall(r"\d+", nome)
    return int(numeros[0]) if numeros else 0


def processar_exames(exames_json_folder, output_folder, modelo):

    os.makedirs(output_folder, exist_ok=True)

    arquivos_json = [arquivo for arquivo in os.listdir(exames_json_folder) if arquivo.endswith(".json")]

    arquivos_json.sort(key=extrair_numero_paciente)

    tempos_path = os.path.join(output_folder,"tempos_laudos.json")

    if os.path.exists(tempos_path):

        with open(tempos_path, "r", encoding="utf-8") as f:
            tempos = json.load(f)
    else:
        tempos = {}

    for arquivo in arquivos_json:

        paciente = arquivo.replace(".json", "")

        paciente_folder = os.path.join(output_folder,paciente)

        os.makedirs(paciente_folder, exist_ok=True)

        laudo_path = os.path.join(paciente_folder,"laudo.txt")

        if os.path.exists(laudo_path):
            print(f"[{modelo}] {paciente}: laudo já existe.")
            continue

        dados_exame = carregar_json_exame(exames_json_folder,paciente)

        laudo, tempo = gerar_laudo(dados_exame,modelo)

        tempos[paciente] = tempo

        with open(laudo_path, "w", encoding="utf-8") as f:
            f.write(laudo)

        with open(tempos_path, "w", encoding="utf-8") as f:
            json.dump(tempos,f,indent=4,ensure_ascii=False)

        print(f"[{modelo}] {paciente}: concluído.")

    if tempos:

        lista_tempos = list(tempos.values())

        media = sum(lista_tempos) / len(lista_tempos)
        total = sum(lista_tempos)

        print("\n---------------------------")
        print(f"Modelo: {modelo}")
        print(f"Laudos gerados: {len(lista_tempos)}")
        print(f"Média: {media:.2f} s")
        print(f"Tempo total: {total:.2f} s")
        print("---------------------------\n")

    return tempos