import os #allows Python to interact with the operating system, including reading environment variables.
from dotenv import load_dotenv #(import function from package)

load_dotenv() #loads these environmental variables so python can access them

AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION =os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_API_KEY =os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT =os.getenv("AZURE_OPENAI_DEPLOYMENT")