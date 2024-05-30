"""Functions composing the prompt and getting the response from Mistral models"""
import json
import time
import profile_finder.config as pfc
from profile_finder.utils import save_model_output
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


def get_mistral_answer(
    user_prompt: str,
    biographies: str,
    model: str,
    save_output: bool = False
) -> tuple[dict, str | None]:
    """Compose prompt with biographies and user input, then use OpenAI API to get response from the model.

    Args:
        user_prompt (str): user input
        biographies (str): text of biographies
        model (str): selected model 
        save_output (bool, optional): whether to save output. Defaults to False

    Returns:
        tuple[dict, str | None]: model responding and output file
    """
    client = MistralClient(
        endpoint=pfc.MODEL_CREDS[pfc.SELECTED_MODEL][0],
        api_key=pfc.MODEL_CREDS[pfc.SELECTED_MODEL][1],
    )
    system_prompt = pfc.SYSTEM_PROMPT + biographies

    not_valid_json_answer = True
    start_time = time.time()

    while not_valid_json_answer:
        # get response
        response = client.chat(
            model="azureai",
            messages=[
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="user", content=user_prompt),
            ],
            response_format={"type": "json_object"}
        )
        # retrieve model's answer
        answer = response.choices[0].message.content
        # attempt to parse json
        try:
            json.loads(answer)
            not_valid_json_answer = False
            print(list(json.loads(answer).keys()))
            print('Got a correct format.')
            print(f'in {round(time.time() - start_time, 2)} seconds.\n')
        except json.JSONDecodeError:
            # model generated broken json
            print('/!\\ Got a wrong format.')
            pass
    
    output_file = save_model_output(
        model,
        system_prompt,
        user_prompt,
        answer,
        save_output,
    )
    return json.loads(answer), output_file
