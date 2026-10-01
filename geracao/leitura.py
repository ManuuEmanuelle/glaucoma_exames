import os
import json

def carregar_json_exame(exames_json_folder,paciente):

    json_path = os.path.join(exames_json_folder,f"{paciente}.json")

    with open(json_path,"r",encoding="utf-8") as f:

        return json.load(f)