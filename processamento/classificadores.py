import re

from .conversores import calcular_percentual

def _classificar_escala_100(campo_valor):

    if campo_valor is None: 
        return "não disponível"
    
    match = re.search(r"[\d.,]+", str(campo_valor))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor >= 95.0: 
        return "preservado"
    
    if valor >= 80.0: 
        return "leve"
    
    if valor >= 50.0: 
        return "moderado"
    
    return "avancado"


def classificar_erros_fixacao(erros_fixacao):

    percentual = calcular_percentual(erros_fixacao)

    if percentual is None: 
        return "não disponível"
    
    if percentual <= 20.0: 
        return "boa"
    
    if percentual <= 33.0: 
        return "moderada"
    
    return "ruim"

def classificar_falsos_positivos(falsos_positivos):

    percentual = calcular_percentual(falsos_positivos)

    if percentual is None: 
        return "normal"
    
    if percentual <= 15.0: 
        return "normal"
    
    if percentual <= 20.0: 
        return "atencao"
    
    return "ruim"

def classificar_falsos_negativos(falsos_negativos):

    percentual = calcular_percentual(falsos_negativos)

    if percentual is None: 
        return "normal"
    
    if percentual <= 15.0: 
        return "normal"
    
    if percentual <= 25.0: 
        return "atencao"
    
    return "ruim"

def classificar_fovea(fovea):

    if fovea is None: 
        return "não disponível"
    
    match = re.search(r"\d+", str(fovea))

    if not match: 
        return "não disponível"
    
    valor = float(match.group())

    if valor >= 30.0: 
        return "normal"
    
    if valor >= 20.0: 
        return "reduzida"
    
    return "muito reduzida"

def classificar_vfi(vfi): 
    return _classificar_escala_100(vfi)

def classificar_vqi(vqi): 
    return _classificar_escala_100(vqi)

def classificar_md(md):

    if md is None: 
        return "não disponível"
    
    match = re.search(r"[-\d.,]+", str(md))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor >= -2.0: 
        return "normal"
    
    if valor >= -6.0: 
        return "leve"
    
    if valor >= -12.0: 
        return "moderado"
    
    return "grave"

def classificar_mdh(mdh): 
    return classificar_md(mdh)

def classificar_psd(psd):

    if psd is None: 
        return "não disponível"
    
    match = re.search(r"[\d.,]+", str(psd))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor < 3.0: 
        return "normal"
    
    if valor < 4.5: 
        return "limítrofe"
    
    return "alterado"

def classificar_cpsd(cpsd):

    if cpsd is None: 
        return "não disponível ou omitido"
    
    match = re.search(r"[\d.,]+", str(cpsd))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor < 3.0: 
        return "normal"
    
    if valor < 4.5: 
        return "limítrofe"
    
    return "alterado"

def classificar_sfh(sfh):

    if sfh is None: 
        return "não disponível ou omitido"
    
    match = re.search(r"[\d.,]+", str(sfh))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor < 2.0: 
        return "normal"
    
    if valor <= 3.0: 
        return "limítrofe"
    
    return "elevado"

def classificar_ms(ms):

    if ms is None: 
        return "não disponível"
    
    match = re.search(r"[\d.,]+", str(ms))

    if not match: 
        return "não disponível"
    
    valor = float(match.group().replace(",", "."))

    if valor >= 26.0: 
        return "preservada"
    
    if valor >= 20.0: 
        return "moderadamente reduzida"
    
    return "severamente reduzida"

def classificar_ght(ght):

    if not ght: 
        return "não disponível"
    
    valor = str(ght).strip().title() 
    
    mapeamento = {
        "Within Normal Limits": "normal",
        "Borderline": "suspeito",
        "Outside Normal Limits": "anormal",
        "General Reduction Of Sensitivity": "depressao generalizada",
        "Abnormally High Sensitivity": "hipersensibilidade"
    }

    return mapeamento.get(valor, "desconhecido")



MAPEAMENTO_CLASSIFICADORES = {
    "fovea": classificar_fovea,
    "vfi": classificar_vfi,
    "md": classificar_md,
    "mdh": classificar_mdh,
    "psd": classificar_psd,
    "erros_fixacao": classificar_erros_fixacao,
    "false_pos": classificar_falsos_positivos,
    "false_neg": classificar_falsos_negativos,
    "vqi": classificar_vqi,
    "cpsd": classificar_cpsd,
    "sfh": classificar_sfh,
    "ms": classificar_ms,
    "ght": classificar_ght
}




def classificar_campos(dados):

    dados_classificados = dados.copy()

    for nome, funcao in MAPEAMENTO_CLASSIFICADORES.items():

        if nome not in dados:
            continue

        valor = dados[nome]

        classificacao = funcao(valor)

        dados_classificados[f"{nome}_classificacao"] = classificacao

    return dados_classificados
