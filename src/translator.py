# import google.generativeai as genai
# import os
# from google.colab import userdata  #Used to securely store API Key

# import bigframes.dataframe
from vertexai.preview.language_models import ChatModel, InputOutputTextPair
# from google.cloud import aiplatform
# from google.auth.credentials import Credentials
# from google.oauth2 import service_account

# PROJECT_ID = "nodebb-417218"

# aiplatform.init(
#   # your Google Cloud Project ID or number
#   # environment default used is not set
#   project=PROJECT_ID,

#   # credentials
#   # credentials=credentials,
# )

# GOOGLE_API_KEY=userdata.get('GOOGLE_API_KEY')
# GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# genai.configure(api_key=GOOGLE_API_KEY)

# LLM Settings

# def extract(string):
#     # Criteria that the LLM response must match
#     def lengthForm(s : str): (len(s) >= 10)
#     def tupleForm(s : str): (s[0] == '(' and s[-1] == ')')
#     def boolForm(s : str): (s[1:6] == "False" or s[1:6] == "True,")
#     def badForm(s : str): not (s == "(False, '-')")
#     criteria = [
#         lengthForm(string), tupleForm(string), boolForm(string), badForm(string)
#     ]
#     if False in criteria:
#         return (True, "<LangError>: Post text LLM response is malformed")

#     # Extraction if the LLM response is well-formatted
#     boolVal = False if string[1:6] == "False" else True
#     text = string[8:-2] if boolVal else string[9:-2]
#     return (boolVal, text)

def fullExtract(string):
  def lengthForm(s : str): (len(s) >= 10)
  def tupleForm(s : str): (s[0] == '(' and s[-1] == ')')
  def boolForm(s : str): (s[1:6] == "False" or s[1:6] == "True,")
  def badForm(s : str): not (s == "(False, '-')")
  criteria = [lengthForm(string), tupleForm(string), boolForm(string), badForm(string)]

  # boolVal, translation = (response.candidates[0], response.candidates[1])

  if False in criteria:
    return (True, "<LangError>: Post text LLM response is malformed")

  def extract(s : str):
    boolVal = False if s[1:6] == "False" else True
    text = s[8:-2] if boolVal else s[9:-2]
    return (boolVal, text)

  return extract(string)

context3 = ("You are now going to function as a detailed translator. When given a input of text, you will ultimately return a Python"
            " tuple with two entries. Let the input text be represented through variable t. If the input text is in English, then return"
            " (True, t). Otherwise, I want you to identify what language t is in. If t is text in a known language, then let return"
            " (False, p) where p is the English translation of t. If t is not in an identifiable language, return (False, '-').")

# If the input text is in English, then return (True, input_text). If the input text is not in english, but is in a known language, return 
# (False, translation of input text). If it is not able to indentify the language or the translation return (True, error)
def query_llm_robust(post: str) -> tuple[bool, str]:
  '''
  TODO: Implement this
  '''
  chat_model = ChatModel.from_pretrained("chat-bison@001")

  parameters = {
    "temperature": 0.7,  # Temperature controls the degree of randomness in token selection.
    "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
  }
  chat = chat_model.start_chat(context=context3)
  response = chat.send_message(post, **parameters)
  string = response.text

  def lengthForm(s : str): (len(s) >= 10)
  def tupleForm(s : str): (s[0] == '(' and s[-1] == ')')
  def boolForm(s : str): (s[1:6] == "False" or s[1:6] == "True,")
  def badForm(s : str): not (s == "(False, '-')")
  criteria = [lengthForm(string), tupleForm(string), boolForm(string), badForm(string)]

  # boolVal, translation = (response.candidates[0], response.candidates[1])

  if False in criteria:
    return (True, "<LangError>: Post text LLM response is malformed")

  def extract(s : str):
    boolVal = False if s[1:6] == "False" else True
    text = s[8:-2] if boolVal else s[9:-2]
    return (boolVal, text)

  print(string)
  return extract(string)

def translate_content(content: str) -> tuple[bool, str]:
    return fullExtract(query_llm_robust(content))