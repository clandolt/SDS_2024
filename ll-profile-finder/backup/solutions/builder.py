"""Functions retrieving the contents of biographies"""
import random
import pandas
import tiktoken
import profile_finder.config as config


def parse_skills(skillset: str) -> list[str]:
    """Helper function to parse user input for skillset.

    Args:
        skillset (str): comma separated values

    Returns:
        list[str]: list of skills
    """
    return [x.strip() for x in skillset.split(",") if x != ""]


def build_context_from_table(
    path: str,
    has_capacity: bool = False,
    selected_capacity: int = config.CONSULTANT_FULL_CAPACITY,
    required_cert: str = "None",
    required_skills: list[str] = [],
) -> tuple[str, int]:
    """Build context from TSV file with biographies.

    Args:
        path (str): path to biographies
        has_capacity (bool, optional): whether to consider profiles with available capacity only. Default to False
        selected_capacity (int, optional): selected capacity to filter by. Defaults to config.CONSULTANT_FULL_CAPACITY,
        required_cert (str, optional): the name of the required certification for the project (client's requirement). Defaults to "None"
        required_skills (str, optional):  list of required technical skills. Defaults to []

    Returns:
        str: biographies in a particular format
    """
    data = pandas.read_csv(path, sep="\t")
    data.fillna('', inplace=True)

    biography_count = 0
    current_context_length = 0
    biographies_context_format = ""
    for i in range(data.shape[0]):
        if has_capacity: 
            if int(data.loc[i, config.CONSULTANT_ATTR_CAPACITY]) < selected_capacity: 
                biographies_context_format = add_biography_based_on_cert_and_skills(
                    biographies_context_format,
                    required_cert,
                    required_skills,
                    data.iloc[i,:],
                )
            else:
                pass       
        else:
            # consider all profiles regardless of available capacity
            biographies_context_format = add_biography_based_on_cert_and_skills(
                biographies_context_format,
                required_cert,
                required_skills,
                data.iloc[i,:],
            )

        if len(biographies_context_format) > current_context_length:
            biography_count += 1
            current_context_length = len(biographies_context_format)

    return biographies_context_format, biography_count


def add_biography_based_on_cert_and_skills(
    context: str,
    required_cert: str,
    required_skills: list[str],
    bio: pandas.Series,
) -> str:
    """Implement logic of in-place adding a biography based on the required certification and skillset.

    Args:
        context (str): accumulated context
        required_cert (str): required certification provided by the user
        required_skills (list[str]): list of required skills
        bio (pandas.Series): current biography
    """
    if len(required_skills) == 0:
        # no skills required
        return add_biography_based_on_required_cert(
            context,
            required_cert,
            bio,
        )
    else:
        if any([
            skill.lower() in str(bio[config.CONSULTANT_ATTR_TECH_EXPERTISE]).lower()
            for skill in required_skills
        ]):
            # consider only those profiles with at least one required skill
            return add_biography_based_on_required_cert(
                context,
                required_cert,
                bio,
            )
        else:
            return context


def add_biography_based_on_required_cert(
    context: str,
    required_cert: str,
    bio: pandas.Series,
) -> str:
    """Implement logic of in-place adding a biography based on the required certification.

    Args:
        context (str): accumulated context
        required_cert (str): required certification provided by the user
        bio (pandas.Series): current biography
    """
    if required_cert != config.STRING_NONE:
        if required_cert in bio[config.CONSULTANT_ATTR_CERTIFICATION]:
            # consider only those profiles having the required certificate
            return add_biography_to_context(context, bio)
        else:
            return context
    else:
        # add profile since no certification is required
        return add_biography_to_context(context, bio)


def add_biography_to_context(context: str, bio: pandas.Series) -> str:
    """Add current biography to the common biography context.

    Args:
        context (str): accumulated context
        bio (pandas.Series): current bio

    Returns:
        str: context extended with the current bio
    """
    return (
        context
        + "\n\n\n" 
        + config.BIO_SEPARATOR_STRING 
        + bio[config.CONSULTANT_ATTR_NAME]
        + "\n" 
        + config.CONTEXT_TITLE_SHORT_BIOGRAPHY
        + "\n"
        + bio[config.CONSULTANT_ATTR_SHORT_BIO]
        + config.CONTEXT_TITLE_WORK_EXPERIENCE
        + "\n"
        + bio[config.CONSULTANT_ATTR_PAST_EXPERIENCE]
        + "\n"
        + bio[config.CONSULTANT_ATTR_D_ONE_EXPERIENCE]
    )


def process_profiles_simulation(
    biography_count: int,
    k: int,
    n: int,
) -> int:
    """Simulate the number of times the biographies will be sent to the model (to estimate the price).

    Args:
        biography_count (int): total amount of biographies
        k (int): best of k strategy
        n (int): top N selection
    
    Returns:
        total_views (int): number of biographies sent
    """
    profiles = list(range(1, biography_count + 1))
    total_views = 0
    while len(profiles) > k:
        current_batch = profiles[:k]
        total_views += len(current_batch)
        selected_profiles = random.sample(current_batch, n)
        profiles = profiles[k:] + selected_profiles
    total_views += len(profiles)
    return total_views


def print_stats_pricing(biographies: str, count: int) -> str:
    """Estimate the pricing of a single prompt with all the biographies.

    Args:
        biographies (str): biography texts

    Returns:
        str: info message with the pricing
    """
    total_views = process_profiles_simulation(
        count,
        config.STRATEGY_BEST_OF_K,
        config.STRATEGY_TOP_N
    )
    enc = tiktoken.encoding_for_model(config.TIKTOKEN_MODEL_NAME)
    tokens = enc.encode(biographies) 
    token_count = int(len(tokens) * total_views / count)

    ans = f"Using {count} biographies "
    ans += f"and {config.SELECTED_MODEL}.\n\n"
    ans += f"This converts to a total of around ~{token_count} tokens "
    ans += f"for an approximate price of ${round(token_count * config.PRICE_INPUT[config.SELECTED_MODEL], 6)} (without including the system prompt)."
    
    return ans
