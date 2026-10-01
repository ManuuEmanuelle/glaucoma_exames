def calcular_percentual(valor):

    try:
        if valor is None:
            return None

        valor = str(valor).strip()

        if "/" in valor:

            numerador, denominador = map(int, valor.split("/"))

            if denominador == 0:
                return None

            return (
                numerador / denominador
            ) * 100

        return float(valor.replace("%", "").replace(",", "."))

    except (ValueError,ZeroDivisionError,AttributeError):
        return None


def converter_valor(valor, tipo):

    if tipo == "float":

        valor = str(valor)
        valor = valor.replace(",", ".")

        return float(valor)

    if tipo == "int":

        return int(valor)

    if tipo == "str":

        return str(valor).strip()

    return valor