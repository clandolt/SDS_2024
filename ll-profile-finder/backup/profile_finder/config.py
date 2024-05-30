"""Configurations and constants"""

STRATEGY_BEST_OF_K = 20
STRATEGY_TOP_N = 5  
SAVE_OUTPUT_TO_JSON = True

SYSTEM_PROMPT_JSON_RANK = "rank"
SYSTEM_PROMPT_JSON_REASONS = "reasons"

SYSTEM_PROMPT = """
    You are a helpful assistant designed to output JSON files. 
    You are here to help find the top """ + str(STRATEGY_TOP_N) + """ most relevant profiles for a project based on people's biographies. 
    The JSON output should follow this template and only this template for the most relevant profiles: 
    {First Name Family Name: {""" + f"\"{SYSTEM_PROMPT_JSON_RANK}\"" + """: 1, """ + f"\"{SYSTEM_PROMPT_JSON_REASONS}\"" + """: "3 sentences explanation"}, 
    First Name Family Name: {""" + f"\"{SYSTEM_PROMPT_JSON_RANK}\"" + """: 2, """ + f"\"{SYSTEM_PROMPT_JSON_REASONS}\"" + """: "3 sentences explanation"}}.
    For each person's profile, the explanation should be based on the project description and its specific requirements.
    
    Make sure that you strictly follow the format of JSON you are given.
    Make sure to keep the reasons very concise, as we are prioritizing time over details.
    Make sure that the JSON format is machine readable, as we need to have the correct number of brackets.
    Make sure that the name of the person is surrounded by quotes and replaced with the actual name.
"""
SYSTEM_PROMPT = SYSTEM_PROMPT + "\nHere are all the biographies:"

MODEL_NAME_GPT_4 = "gpt-4"
MODEL_NAME_GPT_35 = "gpt-35-turbo"
MODEL_NAME_MISTRAL_LARGE = "mistral-large"
MODEL_NAME_MISTRAL_SMALL = "mistral-small"
MODEL_NAME_LLAMA_3_70B = "llama-3-70B"
MODEL_NAME_LLAMA_3_8B = "llama-3-8B"


SELECTED_MODEL = MODEL_NAME_GPT_35 
MODEL_SET = [
    MODEL_NAME_GPT_4,
    MODEL_NAME_GPT_35,
    MODEL_NAME_MISTRAL_LARGE,
    MODEL_NAME_MISTRAL_SMALL,
    MODEL_NAME_LLAMA_3_70B,
    MODEL_NAME_LLAMA_3_8B,
]

PRICE_INPUT = { # in USD
    MODEL_NAME_GPT_4: 0.00001,
    MODEL_NAME_GPT_35: 0.000001,
    MODEL_NAME_MISTRAL_LARGE: 0.000004,
    MODEL_NAME_MISTRAL_SMALL: 0.000001,
    MODEL_NAME_LLAMA_3_70B: 0.00000378,
    MODEL_NAME_LLAMA_3_8B: 0.00000037,
}

PRICE_OUTPUT= { # in USD
    MODEL_NAME_GPT_4: 0.00003,
    MODEL_NAME_GPT_35: 0.000002,
    MODEL_NAME_MISTRAL_LARGE: 0.000012,
    MODEL_NAME_MISTRAL_SMALL: 0.000003,
    MODEL_NAME_LLAMA_3_70B: 0.00001134,
    MODEL_NAME_LLAMA_3_8B: 0.0000011,
}

# sources
# https://openai.com/api/pricing/
# https://mistral.ai/technology/#models
# https://ai.azure.com/explore/models/

TIKTOKEN_MODEL_NAME = 'gpt-3.5-turbo'

TOTAL_BIO = 50  #  all available bios

OPENAI_HTTPS_ENDPOINT = 'https://d-academy-aoai-france.openai.azure.com/'
MISTRAL_LARGE_HTTPS_ENDPOINT = 'https://Mistral-large-uugfv-serverless.francecentral.inference.ai.azure.com'
MISTRAL_SMALL_HTTPS_ENDPOINT = 'https://Mistral-small-glxak-serverless.eastus2.inference.ai.azure.com'
LLAMA_3_70B_HTTPS_ENDPOINT = 'https://Meta-Llama-3-70B-Instruct-pptld-serverless.eastus2.inference.ai.azure.com'
LLAMA_3_8B_HTTPS_ENDPOINT = 'https://Meta-Llama-3-8B-Instruct-zjocd-serverless.eastus2.inference.ai.azure.com'


MODEL_CREDS = {
    MODEL_NAME_GPT_4: (OPENAI_HTTPS_ENDPOINT, '76a2272f259d4e68b1d2f1d8009937d7'),
    MODEL_NAME_GPT_35: (OPENAI_HTTPS_ENDPOINT, '76a2272f259d4e68b1d2f1d8009937d7'),
    MODEL_NAME_MISTRAL_LARGE: (MISTRAL_LARGE_HTTPS_ENDPOINT, 'fBdaiUqQRzf0dG8pAR0XASvu2W345QkF'),
    MODEL_NAME_MISTRAL_SMALL: (MISTRAL_SMALL_HTTPS_ENDPOINT, 'KHagsLVFKTOFtPMrdSduNm1twcsTj39L'),
    MODEL_NAME_LLAMA_3_70B: (LLAMA_3_70B_HTTPS_ENDPOINT, '1S8gNJhn8oYrbVd08IP03FG2LJS0GaO6'),
    MODEL_NAME_LLAMA_3_8B: (LLAMA_3_8B_HTTPS_ENDPOINT, 'THmRWnGXtCrJMe8lOlKf5cbbaGN1XFny'),
}

DATA_PATH = 'data-tables/Consultants.tsv'
OUTPUT_PATH = 'output'
OUTPUT_FILENAME = 'answer'

CONSULTANT_ATTR_CAPACITY = "Capacity"
CONSULTANT_ATTR_NAME = "Name"
CONSULTANT_ATTR_TECH_EXPERTISE = "Technical expertise"
CONSULTANT_ATTR_CERTIFICATION = "Certifications"
CONSULTANT_ATTR_SHORT_BIO = "Short bio"
CONSULTANT_ATTR_PAST_EXPERIENCE = "Past experience"
CONSULTANT_ATTR_D_ONE_EXPERIENCE = "D ONE project experience"

CONTEXT_TITLE_SHORT_BIOGRAPHY = "Short biography"
CONTEXT_TITLE_WORK_EXPERIENCE = "Work experience"

CONSULTANT_FULL_CAPACITY = 100
CONSULTANT_CAPACITY_RANGE = [x for x in range(0, 101, 10)]

BIO_SEPARATOR_STRING = "Person name: "

STRING_NONE = "None"

ALL_CERTIFICATES = (
    STRING_NONE,
    "AWS Certified Data Analytics Specialty",
    "AWS Certified Developer - Associate",
    "AWS Certified Machine Learning",
    "AWS Certified Machine Learning – Specialty",
    "AWS Certified Solutions Architect – Associate",
    "Analyzing and Visualizing Data with Microsoft Power BI",
    "Certified Data Vault 2.0 Practitioner",
    "Certified SNYPR Content Developer",
    "Coursera Machine Learning Engineering For Production Specialization",
    "Databricks Certified Associate Developer for Apache Spark 3.0",
    "Databricks Certified Associate developer for Apache Spark 3.0 - Python",
    "Databricks Certified Data Engineer Associate",
    "Databricks Certified Data Engineer Associated",
    "Databricks Certified Machine Learning Associate",
    "Databricks Certified Machine Learning Professional",
    "Dataiku ML Practitioner",
    "Docker Certified Associate",
    "Exam DA-100: Analyzing Data with Microsoft Power BI",
    "GCP Associate Cloud Engineer",
    "GCP Professional Cloud Architect",
    "GCP Professional Data Engineer",
    "IMD Leadership essentials",
    "Leadership Toolkit for Managers",
    "Leading SAFe / SAFe Agilist",
    "Microsoft Certified: Azure AI Fundamentals",
    "Microsoft Certified: Azure Data Engineer Associate",
    "Microsoft Certified: Azure Data Fundamentals",
    "Microsoft Certified: Azure Data Scientist Associate",
    "Microsoft Certified: Azure Fundamentals",
    "Microsoft Certified: Azure Solutions Architect Expert",
    "Microsoft Certified: Power BI Data Analyst Associate",
    "Neo4j Certified Professional",
    "Palantir Foundry Data Engineer Associate",
    "Professional Data Engineer",
    "Professional Scrum Master™ I (PSM I)",
    "SAFe Product Owner/Product Manager",
    "Scrum Master",
    "Snowflake: SnowPro Core Certification",
    "Tableau Certified Associate Consultant",
    "Tableau Desktop Certified Associate",
    "Tableau Desktop Certified Professional",
    "Tableau Partner Sales Accreditation Exam",
    "TensorFlow Developer Certificate",
)

OUTPUT_JSON_MODEL = "model"
OUTPUT_JSON_SYSTEM_PROMPT = "system_prompt"
OUTPUT_JSON_USER_PROMPT = "user_prompt"
OUTPUT_JSON_OUTPUT = "output"
