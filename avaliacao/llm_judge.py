import json

from geracao.modelos import groq_client
from .prompt_llm_juiz import PROMPT_JUIZ_TEMPLATE

def avaliar_com_llm_juiz(dados_referencia, laudo_texto):
    prompt = PROMPT_JUIZ_TEMPLATE.format(
        dados_referencia=dados_referencia,
        laudo_texto=laudo_texto
    )
    
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="openai/gpt-oss-120b",
            response_format={"type": "json_object"},
            temperature=0.1,
        )
        
        conteudo_resposta = chat_completion.choices[0].message.content
        return json.loads(conteudo_resposta)
        
    except Exception as e:
        print(f"Erro ao avaliar pelo Groq: {e}")
        return None