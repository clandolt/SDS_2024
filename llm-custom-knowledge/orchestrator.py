from openai import AzureOpenAI
import os


# gets the API Key from environment variable AZURE_OPENAI_API_KEY
client = AzureOpenAI(
    azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
    api_version=os.environ.get("AZURE_OPENAI_VERSION", "2023-07-01-preview"),
)

acceptance = """Identify if the below defined set of information is present in the conversation.
            Infromation to check in the conversation:

                1. location of travel
                2. mode of travel (travel by bus, train, flight, etc.)

            End of infromation to check

            There are only two ways to answer:
                1. Either you only return "complete" and nothing else but the string -> "complete"
                2. Reply in a polite manner which infromation [mode of travel or duration] is missing in a full sentence and ask to include the missing one
            """

consideration = "complete"

def controller(offer, acceptance, model: str = "gpt-4"):
    prompt = [{"role": "system", "content": acceptance}, {"role": "user", "content": offer},]

    response = client.chat.completions.create(
        model=model,
        messages=prompt,
        temperature=0.01,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )

    identified_consideration = response.choices[0].message.content
    return identified_consideration

