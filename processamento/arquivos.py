import os
import json


def salvar_json_exames(exames, paciente, exames_json_folder):

    os.makedirs(exames_json_folder, exist_ok=True)

    dados = {
        paciente: {
            "exames": exames
        }
    }

    json_path = os.path.join(
        exames_json_folder,
        f"{paciente}.json"
    )

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
