import os
import re

from .conversores import converter_valor, calcular_percentual

CAMPOS_HUMPHREY = {
    "olho": {
        "regex": r"Eye:\s*(\w+)", 
        "tipo": "str"},
    "estrategia": {
        "regex": r"Strategy:\s*([^\n\r]+)", 
        "tipo": "str"},
    "fovea": {
        "regex": r"Fovea\s*:\s*([-\d.,]+)", 
        "tipo": "float"},
    "erros_fixacao": {
        "regex": r"Fixation\s+Losses:\s*(\d+/\d+)", 
        "tipo": "str"},
    "false_pos": {
        "regex": r"False\s+POS\s+Errors:\s*([\d.,]+%)", 
        "tipo": "str"},
    "false_neg": {
        "regex": r"False\s+NEG\s+Errors:\s*([\d.,]+%)", 
        "tipo": "str"},
    "vfi": {
        "regex": r"VFI:\s*([\d.]+)", 
        "tipo": "float"},
    "md": {
        "regex": r"MD:\s*([-\d.,]+)", 
        "tipo": "float"},
    "psd": {
        "regex": r"PSD:\s*([-\d.]+)", 
        "tipo": "float"},
    "ght": {
        "regex": r"GHT:\s*([^\n\r]+)", 
        "tipo": "str"}
}

CAMPOS_OPTOPOL = {
    "olho": {
        "regex": r"Olho:\s*(.*)", 
        "tipo": "str"},
    "erros_fixacao": {
        "regex": r"Erros\s+Fix\.\s*camera:\s*(\d+)", 
        "tipo": "int"},
    "false_pos": {
        "regex": r"FPOS:\s*(\d+/\d+)", 
        "tipo": "str"},
    "false_neg": {
        "regex": r"FNEG:\s*(\d+/\d+)", 
        "tipo": "str"},
    "fovea": {
        "regex": r"Fovea:\s*([-\d.,]+)", 
        "tipo": "float"},
    "estrategia": {
        "regex": r"Estratégia:\s*([^\n\r]+)", 
        "tipo": "str"},
    "ght": {
        "regex": r"GHT:\s*([^\n\r]+)", 
        "tipo": "str"},
    "vqi": {
        "regex": r"VQi:\s*([\d.,]+)", 
        "tipo": "float"},
    "md": {
        "regex": r"MDh:\s*([-\d.,]+)", 
        "tipo": "float"},
    "psd": {
        "regex": r"PSD:\s*([-\d.,]+)", 
        "tipo": "float"},
    "cpsd": {
        "regex": r"CPSD:\s*([-\d.,]+)", 
        "tipo": "float"},
    "sfh": {
        "regex": r"SFh:\s*([-\d.,]+)", 
        "tipo": "float"},
    "ms": {
        "regex": r"MS:\s*([-\d.,]+)", 
        "tipo": "float"}
}

def detectar_tipo_exame(texto):

    texto = texto.lower().replace("\n", " ")

    if re.search(r'center\s*24-2\s*threshold', texto): 
        return "humphrey"
    
    if re.search(r'c\s*-?\s*24.*avan', texto): 
        return "optopol"
    
    return "desconhecido"

def extrair_campos(texto, campos):
 
    dados = {}

    for nome, config in campos.items():

        match = re.search(
            config["regex"],
            texto
        )

        if not match:
            continue

        valor = match.group(1)

        valor = converter_valor(
            valor,
            config["tipo"]
        )

        dados[nome] = valor

    return dados


def extrair_humphrey(texto):

    dados = extrair_campos(texto, CAMPOS_HUMPHREY)

    if dados.get("olho") == "Right": 
        dados["olho"] = "OD"

    elif dados.get("olho") == "Left": 
        dados["olho"] = "OE"

    return dados

def extrair_optopol(texto):
    return extrair_campos(texto, CAMPOS_OPTOPOL)

def estruturar_exame(texto):

    tipo = detectar_tipo_exame(texto)

    if tipo == "humphrey": 
        dados = extrair_humphrey(texto)

    elif tipo == "optopol": 
        dados = extrair_optopol(texto)

    else: 
        dados = {"texto_bruto": texto}

    dados["tipo"] = tipo

    return dados


def extrair_texto_laudo(doc, laudos_texto_folder, paciente):

    num_paginas = len(doc)

    text = doc[num_paginas-1].get_text()

    text_path = os.path.join(laudos_texto_folder, f"{paciente}_laudo.txt")

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text)

def extrair_texto_exame(doc, paginas_exame):

    exames = []

    for i, pagina in enumerate(paginas_exame, start=1):

        text = doc[pagina - 1].get_text().replace("：", ":").replace("％", "%")

        dados = estruturar_exame(text)

        exames.append({"exame": i, "dados": dados})

    return exames
