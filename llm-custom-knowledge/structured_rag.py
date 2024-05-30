import sqlite3
import torch
import re
import pandas as pd  
import sqlite3
import warnings
import sqlparse
from IPython.display import display, Markdown
from transformers import AutoTokenizer, AutoModelForCausalLM


warnings.filterwarnings("ignore")

model_name = "defog/llama-3-sqlcoder-8b"
tokenizer = AutoTokenizer.from_pretrained(model_name)
text2sql_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    trust_remote_code=True,
    load_in_4bit=True,
    device_map="auto",
    use_cache=True,
)

CREATE_TABLE_STATEMENT = """
  create table routes (
    route_id integer primary key,
    origin_city varchar(50),
    destination_city varchar(50),
    distance_km decimal(10,2),
    travel_time_ferry decimal(10,2),
    travel_time_plane decimal(10,2),
    travel_time_sailboat decimal(10,2),
    travel_time_speedboat decimal(10,2),
    price_chf_ferry decimal(10,2),
    price_chf_plane decimal(10,2),
    price_chf_sailboat decimal(10,2),
    price_chf_speedboat decimal(10,2)
  );
  """
ROUTES_DATA = [
    (1, 'Athens', 'Crete', 320.0, 8.0, 1.0, 12.0, 5.0, 45.0, 65.0, 225.0, 750.0),
    (2, 'Athens', 'Evia', 80.0, 1.5, 0.5, 6.0, 1.5, 11.25, 16.25, 56.25, 187.5),
    (3, 'Athens', 'Lesbos', 460.0, 10.0, 1.5, 48.0, 6.0, 64.6875, 93.4375, 323.4375, 1078.125),
    (4, 'Athens', 'Rhodes', 490.0, 12.0, 1.5, 72.0, 7.0, 68.90625, 99.53125, 344.53125, 1148.4375),
    (5, 'Athens', 'Chíos', 440.0, 7.0, 1.5, 42.0, 6.0, 61.875, 89.375, 309.375, 1031.25),
    (6, 'Athens', 'Kefalonia', 295.0, 7.0, 1.5, 24.0, 5.0, 41.484375, 59.921875, 207.421875, 691.40625),
    (7, 'Athens', 'Corfu', 218.0, 7.0, 1.0, 72.0, 7.0, 30.65625, 44.28125, 153.28125, 510.9375),
    (8, 'Athens', 'Lemnos', 321.0, 10.0, 1.5, 42.0, 7.0, 45.140625, 65.203125, 225.703125, 752.34375),
    (9, 'Athens', 'Samos', 330.0, 9.0, 1.5, 48.0, 7.0, 46.40625, 67.03125, 232.03125, 773.4375),
    (10, 'Athens', 'Naxos', 228.0, 5.0, 1.25, 28.0, 4.0, 32.0625, 46.3125, 160.3125, 534.375),
    (11, 'Athens', 'Zakynthos', 295.0, 7.0, 1.5, 22.0, 5.0, 41.484375, 59.921875, 207.421875, 691.40625),
    (12, 'Athens', 'Thassos', 430.0, 10.0, 1.5, 42.0, 7.0, 60.46875, 87.34375, 302.34375, 1007.8125),
    (13, 'Athens', 'Andros', 182.0, 2.0, 0.5, 9.0, 3.0, 25.59375, 36.96875, 127.96875, 426.5625),
    (14, 'Athens', 'Lefkada', 295.0, 7.0, 1.5, 24.0, 6.0, 41.484375, 59.921875, 207.421875, 691.40625),
    (15, 'Athens', 'Karpathos', 326.0, 23.0, 1.5, 70.0, 7.0, 45.84375, 66.21875, 229.21875, 764.0625),
    (16, 'Athens', 'Kos', 430.0, 12.0, 1.5, 72.0, 9.0, 60.46875, 87.34375, 302.34375, 1007.8125),
    (17, 'Athens', 'Kythira', 230.0, 7.0, 1.5, 24.0, 5.0, 32.34375, 46.71875, 161.71875, 539.0625),
    (18, 'Athens', 'Icaria', 225.0, 7.0, 1.5, 22.0, 5.0, 31.640625, 45.703125, 158.203125, 527.34375),
    (19, 'Athens', 'Skyros', 225.0, 4.0, 1.5, 14.0, 5.0, 31.640625, 45.703125, 158.203125, 527.34375),
    (20, 'Athens', 'Paros', 194.0, 4.0, 1.0, 10.0, 4.0, 27.28125, 39.40625, 136.40625, 454.6875),
    (21, 'Athens', 'Tinos', 200.0, 4.0, 1.5, 10.0, 3.0, 28.125, 40.625, 140.625, 468.75),
    (22, 'Athens', 'Samothrace', 580.0, 12.0, 1.5, 72.0, 7.0, 81.5625, 117.8125, 407.8125, 1359.375),
    (23, 'Athens', 'Milos', 210.0, 4.0, 0.5, 15.0, 4.0, 29.53125, 42.65625, 147.65625, 492.1875),
    (24, 'Athens', 'Kea', 82.0, 1.5, 0.5, 6.0, 1.5, 11.53125, 16.65625, 57.65625, 192.1875),
    (25, 'Athens', 'Amorgos', 218.0, 7.0, 1.5, 48.0, 5.0, 30.65625, 44.28125, 153.28125, 510.9375),
    (26, 'Athens', 'Kalymnos', 400.0, 7.0, 1.5, 48.0, 6.0, 56.25, 81.25, 281.25, 937.5),
    (27, 'Athens', 'Ios', 215.0, 7.0, 1.5, 38.0, 5.0, 30.234375, 43.671875, 151.171875, 503.90625),
    (28, 'Athens', 'Kythnos', 155.0, 3.0, 0.5, 10.0, 2.0, 21.796875, 31.484375, 108.984375, 363.28125),
    (29, 'Athens', 'Astypalaia', 270.0, 9.0, 2.5, 45.0, 7.0, 37.96875, 54.84375, 189.84375, 632.8125),
    (30, 'Athens', 'Ithaca', 295.0, 7.0, 1.5, 36.0, 6.0, 41.484375, 59.921875, 207.421875, 691.40625),
    (31, 'Athens', 'Salamis', 15.0, 1.0, 0.5, 4.0, 0.5, 2.109375, 3.046875, 10.546875, 35.15625),
    (32, 'Athens', 'Skopelos', 225.0, 6.0, 2.5, 24.0, 6.0, 31.640625, 45.703125, 158.203125, 527.34375),
    (33, 'Athens', 'Mykonos', 230.0, 5.0, 0.5, 12.0, 4.0, 32.34375, 46.71875, 161.71875, 539.0625),
    (34, 'Athens', 'Syros', 125.0, 4.0, 1.0, 12.0, 2.5, 17.578125, 25.390625, 87.890625, 292.96875),
    (35, 'Athens', 'Aegina', 40.0, 1.5, 0.5, 4.0, 1.0, 5.625, 8.125, 28.125, 93.75),
    (36, 'Athens', 'Santorini', 230.0, 8.0, 1.5, 30.0, 7.0, 32.34375, 46.71875, 161.71875, 539.0625),
    (37, 'Athens', 'Serifos', 95.0, 4.0, 0.5, 12.0, 2.5, 13.359375, 19.296875, 66.796875, 222.65625),
    (38, 'Athens', 'Sifnos', 122.0, 5.0, 1.5, 12.0, 2.5, 17.15625, 24.78125, 85.78125, 285.9375),
    (39, 'Athens', 'Kasos', 389.0, 18.0, 5.0, 44.0, 7.0, 54.703125, 79.015625, 273.515625, 911.71875),
    (40, 'Athens', 'Alonniso', 220.0, 6.0, 1.5, 42.0, 4.0, 30.9375, 44.6875, 154.6875, 515.625)
  ]
INSERT_STATEMENT = """
  INSERT INTO routes (
    route_id,
    origin_city,
    destination_city,
    distance_km,
    travel_time_ferry,
    travel_time_plane,
    travel_time_sailboat,
    travel_time_speedboat,
    price_chf_ferry,
    price_chf_plane,
    price_chf_sailboat,
    price_chf_speedboat
  )
  VALUES (
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?,
    ?
  )
  """
  

def add_mockup_data_to_memory(conn: sqlite3.Connection) -> None:
  """Function to add mockup data to memory."""
  cursor = conn.cursor()
  cursor.execute(CREATE_TABLE_STATEMENT)
  routes_data = ROUTES_DATA
  cursor.executemany(INSERT_STATEMENT, routes_data,)
  conn.commit()

def add_available_islands() -> list:
  """Returns the list of available islands."""
  islands = [
    "Crete",
    "Evia",
    "Lesbos",
    "Rhodes",
    "Chíos",
    "Kefalonia",
    "Corfu",
    "Lemnos",
    "Samos",
    "Naxos",
    "Zakynthos",
    "Thassos",
    "Andros",
    "Lefkada",
    "Karpathos",
    "Kos",
    "Kythira",
    "Icaria",
    "Skyros",
    "Paros",
    "Tinos",
    "Samothrace",
    "Milos",
    "Kea",
    "Amorgos",
    "Kalymnos",
    "Ios",
    "Kythnos",
    "Astypalaia",
    "Ithaca",
    "Salamis",
    "Skopelos",
    "Mykonos",
    "Syros",
    "Aegina",
    "Santorini",
    "Serifos",
    "Sifnos",
    "Kasos",
    "Alonniso"
]

TASK = """### Task
Generate a SQL query to answer [QUESTION]{question}[/QUESTION]
"""

INSTRUCTIONS = """### Instructions
- If you cannot answer the question with the database schema provided below, return 'I do not know'.
- Always return every attribute.

"""

DATABASET_SCHEMA = """### Database Schema
This query will run on a database and the database schema is represented in this string:

CREATE TABLE routes (
  route_id integer primary key,
  origin_city varchar(50),
  destination_city varchar(50),
  distance_km decimal(10,2),
  travel_time_ferry decimal(10,2),
  travel_time_plane decimal(10,2),
  travel_time_sailboat decimal(10,2),
  travel_time_speedboat decimal(10,2),
  price_chf_ferry decimal(10,2),
  price_chf_plane decimal(10,2),
  price_chf_sailboat decimal(10,2),
  price_chf_speedboat decimal(10,2)
);
-- routes.origin_city is always Athens
-- routes.destination_city is the target city of the travel. It is always written with a capital letter.
"""

ANSWER = """### Answer
Given the database schema, here is the SQL query that answers [QUESTION]{question}[/QUESTION]
[SQL]"""

database_description = TASK + INSTRUCTIONS + DATABASET_SCHEMA + ANSWER

def create_request_for_text2sql(island: str) -> str:
  """Function to create a request for an island."""
  request = "Give me the all the available travel information from Athens to " + island 
  return request

def clean_generated_sql(generated_sql: str) -> str:
  """Function to clean the generated SQL to return only relevant SQL"""
  pattern = r"SELECT[\s\S]+?;"
  match = re.search(pattern, generated_sql)
  return match.group(0)

def generate_sql_query(question: str) -> str:
  """Using the LLM we selected, we retrieve the query for the request we created."""
  updated_prompt = database_description.format(question=question)
  inputs = tokenizer(updated_prompt, return_tensors="pt").to("cuda")
  generated_ids = text2sql_model.generate(
      **inputs,
      num_return_sequences=1,
      eos_token_id=tokenizer.eos_token_id,
      pad_token_id=tokenizer.eos_token_id,
      max_new_tokens=400,
      do_sample=False,
      num_beams=1,
  )
  outputs = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)

  torch.cuda.empty_cache()
  torch.cuda.synchronize()

  generated_sql = sqlparse.format(outputs[0].split("[SQL]")[-1], reindent=True)

  return clean_generated_sql(generated_sql)

def fetch_data_from_database(sql_query: str, conn: sqlite3.Connection) -> pd.DataFrame:
  """Function to fetch data from the in memory database."""
  df = pd.read_sql_query(sql_query, conn)  
    
  return df

def parse_island_name(text):
    """
    This could be an LLM model that extracts the island name from the given text.
    For simplicity we controlled the input.
    Extracts the word following the 'Title:' in the given text.

    Parameters:
    text (str): The input text containing the title.

    Returns:
    str: The extracted word if found, else None.
    """
    # Regex pattern to extract any word after "Title:"
    pattern = r'Title:\s*([\w]+)'
    
    # Search for the pattern in the text
    match = re.search(pattern, text)
    
    # Return the extracted word if found
    if match:
        return match.group(1)
    else:
        return None

def main(island: str) -> pd.DataFrame:
  """Function for structured RAG using llama-3-sqlcoder-8b"""

  text2sql_query = create_request_for_text2sql(island=island)

  print(f"Request is: {text2sql_query}")

  sql_query = generate_sql_query(text2sql_query)

  print(f"SQL query is: {sql_query}")

  conn = sqlite3.connect('data/travel_information.sqlite')
  try:
    add_mockup_data_to_memory(conn=conn)
  except:
    pass
  available_islands = add_available_islands()

  data = fetch_data_from_database(sql_query=sql_query, conn=conn)

  return data

