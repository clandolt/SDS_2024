"""Functions composing the prompt and getting the response from Llama models"""
import json
import time
from openai import OpenAI
import profile_finder.config as pfc
from profile_finder.utils import save_model_output


def extract_and_balance_json(text: str) -> str:
    """Helper function to parse or fix JSON from Llama models,
    since they don't support JSON-formatted output.

    Args:
        text (str): model response

    Returns:
        str: refined response (if possible to fix)
    """
    # Find the first opening and the last closing bracket
    first_opening = text.find('{')
    last_closing = text.rfind('}')
    
    # Extract the substring between these indexes
    if first_opening != -1 and last_closing != -1:
        json_string = text[first_opening:last_closing + 1] 
    else:
        json_string = ""
    
    # Check for balancing brackets
    if json_string != "":
        # Count the brackets
        opening_count = json_string.count('{')
        closing_count = json_string.count('}')
        
        # Add missing opening or closing brackets
        if opening_count > closing_count:
            json_string += '}' * (opening_count - closing_count)
        elif closing_count > opening_count:
            json_string = '{' * (closing_count - opening_count) + json_string
        else:
            pass

    return json_string


def get_llama_answer(
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
    client = OpenAI(
        base_url=pfc.MODEL_CREDS[pfc.SELECTED_MODEL][0],
        api_key=pfc.MODEL_CREDS[pfc.SELECTED_MODEL][1]
    )
    system_prompt = pfc.SYSTEM_PROMPT + biographies
    
    not_valid_json_answer = True
    start_time = time.time()
    
    while not_valid_json_answer:
        # get response
        response = client.chat.completions.create(
            model="azureai",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],        
            max_tokens=None,
        )
        # retrieve model's answer
        answer = response.choices[0].message.content
        answer = extract_and_balance_json(answer)
      
        # attempt to parse json
        try:
            json.loads(answer)
            not_valid_json_answer = False
            print(list(json.loads(answer).keys()))
            print('Got a correct format.')
            print(f'in {round(time.time() - start_time, 2)} seconds.\n')
        except json.JSONDecodeError:
            # model generated a broken json
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
