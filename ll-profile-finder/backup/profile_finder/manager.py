"""Functions implementing logic for iterative profile analysis"""
import profile_finder.config as config
import profile_finder.retriever_openai as pfro
import profile_finder.retriever_mistral as pfrm
import profile_finder.retriever_llama as pfrl
from profile_finder.utils import is_gpt_model
from profile_finder.utils import is_llama_model


def get_answer(
    prompt: str,
    biographies: str,
    save_output: bool = False,
) -> tuple[dict, str | None]:
    """ Call the correct AI provider and model
    - check the origin of the model
    - redirect the call

    Args:
        prompt (str): user input prompt 
        biographies (str): biographies as text
        save_output (bool, optional): whether to save output. Defaults to False

    Returns:
        tuple[dict, str | None]: model responding and output file
    """
    if is_gpt_model(config.SELECTED_MODEL):
        return pfro.get_open_ai_answer(
            prompt,
            biographies,
            config.SELECTED_MODEL,
            save_output,
        )

    # Challenge #5: add Mistral models: 
    # - checkout utils.py and and retriever_mistral.py,
    # - make sure the corresponding functions exist for Mistral,
    # - implement another elif condition to support Mistral models

    elif is_llama_model(config.SELECTED_MODEL):
        return pfrl.get_llama_answer(
            prompt,
            biographies,
            config.SELECTED_MODEL,
            save_output,
        )
    else:
        raise Exception(f'Model not found {config.SELECTED_MODEL}.')


def find_best_matching_profiles(
    prompt: str,
    bio_contents: str,
    save_output: bool = False,
) -> tuple[dict, str | None]:
    """Implement strategy K-by-K.
    - screen first K profiles and find best
    - append best to the end and remove others
    - iterate until the list has at most K profiles
    - find best of the K best

    Args:
        prompt (str): user input prompt 
        bio_contents (str): biographies as text
        save_output (bool, optional): whether to save output. Defaults to False

    Returns:
        tuple[dict, str | None]: _description_
    """
    bios = bio_contents.split(config.BIO_SEPARATOR_STRING)
    bios.pop(0)  # drop an empty element

    while len(bios) > config.STRATEGY_BEST_OF_K:
        print(f"{len(bios)} biographies left.")
        # take first k biographies
        k_first_profiles = config.BIO_SEPARATOR_STRING.join(bios[:config.STRATEGY_BEST_OF_K])
        # prompt model with first k biographies
        best_from_k, _ = get_answer(prompt, k_first_profiles)

        for bio in bios[:config.STRATEGY_BEST_OF_K]:
            is_bio_among_best = False
            # check if bio was picked as best matching
            for filename, _ in best_from_k.items():
                if filename in bio:
                    is_bio_among_best = True
                    break
            # remove bio its position
            bios.remove(bio)
            if is_bio_among_best:
                # append to the end of list
                bios.append(bio)
    
    print(f"{len(bios)} biographies left.")
    remaining_profiles = config.BIO_SEPARATOR_STRING.join(bios)

    return get_answer(prompt, remaining_profiles, save_output=save_output)
