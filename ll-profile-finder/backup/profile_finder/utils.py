
import os
import json
from profile_finder.config import MODEL_NAME_GPT_4
from profile_finder.config import MODEL_NAME_MISTRAL_LARGE
from profile_finder.config import MODEL_NAME_LLAMA_3_70B
from profile_finder.config import OUTPUT_JSON_MODEL
from profile_finder.config import OUTPUT_JSON_SYSTEM_PROMPT
from profile_finder.config import OUTPUT_JSON_USER_PROMPT
from profile_finder.config import OUTPUT_JSON_OUTPUT
from profile_finder.config import OUTPUT_PATH
from profile_finder.config import OUTPUT_FILENAME


def is_gpt_model(selected_model: str) -> bool:
    """Helper function to determine whether the user selected a GPT model

    Args:
        selected_model (str): user input

    Returns:
        bool: whether or not a GPT model is selected
    """
    if MODEL_NAME_GPT_4.split("-")[0] in selected_model:
        return True
    else:
        return False
    

def is_mistral_model(selected_model: str) -> bool:
    """Helper function to determine whether the user selected a Mistral model

    Args:
        selected_model (str): user input

    Returns:
        bool: whether or not a Mistral model is selected
    """
    if MODEL_NAME_MISTRAL_LARGE.split("-")[0] in selected_model:
        return True
    else:
        return False
    

def is_llama_model(selected_model: str) -> bool:
    """Helper function to determine whether the user selected a Llama model

    Args:
        selected_model (str): user input

    Returns:
        bool: whether or not a Llama model is selected
    """
    if MODEL_NAME_LLAMA_3_70B.split("-")[0] in selected_model:
        return True
    else:
        return False


def save_model_output(
    model: str,
    system_prompt: str,
    user_prompt: str,
    answer: str,
    save_output: bool,
) -> str | None:
    """Helper function to save the model output if needed.

    Args:
        model (str): model name
        system_prompt (str): system prompt
        user_prompt (str): user prompt (input)
        answer (str): model response
        save_output (bool): whether to save or not
    
    Returns:
        str | None: filename if output is saved, or None otherwise
    """
    # define the variables to be included in the JSON file
    data = {
        OUTPUT_JSON_MODEL: model,
        OUTPUT_JSON_SYSTEM_PROMPT: system_prompt,
        OUTPUT_JSON_USER_PROMPT: user_prompt,
        OUTPUT_JSON_OUTPUT: answer,
    }
    # save to file is necessary
    if save_output:
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH)
        
        file_count = len(
            [
                f for f in os.listdir(OUTPUT_PATH)
                if os.path.isfile(os.path.join(OUTPUT_PATH, f))
            ]
        )
        # save to JSON
        output_file = f'{OUTPUT_FILENAME}_{file_count + 1}.json'
        with open(OUTPUT_PATH + "/" + output_file, 'w') as file:
            json.dump(data, file)
    else:
        output_file = None
    
    return output_file
