import json
import time

from geracao.modelos import groq_client
from avaliacao.prompt_llm_juiz import PROMPT_JUIZ_TEMPLATE
from groq import RateLimitError



MODELO_JUIZ = "openai/gpt-oss-120b"

def avaliar_com_llm_juiz(dados_referencia, laudo_texto):

    prompt = PROMPT_JUIZ_TEMPLATE.format(dados_referencia=dados_referencia,laudo_texto=laudo_texto)

    tentativa = 1

    while True:

        try:

            print(
                f"    Avaliando com LLM juiz "
                f"(tentativa {tentativa})..."
            )

            resposta = groq_client.chat.completions.create(
                model=MODELO_JUIZ,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                response_format={
                    "type": "json_object"
                }
            )

            conteudo = resposta.choices[0].message.content

            resultado = json.loads(conteudo)

            print("    Avaliação do LLM juiz concluída.")

            return resultado

        except RateLimitError as e:

            espera = 120

            print("\n    Limite de tokens atingido.")
            print(
                f"    Aguardando {espera} segundos "
                "antes de tentar novamente..."
            )

            time.sleep(espera)

            tentativa += 1

        except json.JSONDecodeError as e:

            print(
                f"\n    Erro ao interpretar resposta "
                f"do LLM juiz: {e}"
            )

            return None

        except Exception as e:

            print(
                f"\n    Erro ao avaliar pelo LLM juiz: {e}"
            )

            return None