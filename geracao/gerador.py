import time

from .prompt_laudo import criar_prompt_laudo
from .modelos import gerar_resposta_modelo



def gerar_laudo(dados_exame, modelo):

        prompt = criar_prompt_laudo(dados_exame)

        inicio = time.time()

        laudo = gerar_resposta_modelo(prompt,modelo)

        fim = time.time()

        tempo = fim - inicio

      

        return laudo, tempo