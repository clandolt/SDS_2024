class ModelCost:
    def __init__(
        self,
        name: str,
        currency: str,
        token_cost_per_prompt: float,
        token_cost_per_completion: float,
    ) -> None:
        self.name = name
        self.currency = currency
        self.token_cost_per_prompt = token_cost_per_prompt
        self.token_cost_per_completion = token_cost_per_completion

    def __str__(self) -> str:
        return self.name


GPT35 = ModelCost(
    name="gpt3.5-turbo",
    currency="CHF",
    token_cost_per_prompt=0.0014 / 1000,
    token_cost_per_completion=0.0019 / 1000,
)
GPT4 = ModelCost(
    name="gpt4",
    currency="CHF",
    token_cost_per_prompt=0.028 / 1000,
    token_cost_per_completion=0.055 / 1000,
)
DefaultModel = ModelCost("default", "CHF (max, approx.)", 0.055 / 1000, 0.109 / 1000)

model_instances = {"gpt-35-turbo": GPT35, "gpt-4": GPT4, "gpt-4": GPT4}


def get_model_instance(model_name: str = None) -> ModelCost:
    model_instance = model_instances.get(model_name, DefaultModel)
    return model_instance
