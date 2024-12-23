# -*- coding: utf-8 -*-
"""Untitled23.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XOfimbP_tN7eLPv4sGx2ttIl9AbZxRt6
"""

!pip install openai --quiet
!pip install langchain --quiet
!pip install cohere --quiet
!pip install tiktoken --quiet
!pip install wikipedia
!pip install serp
!pip install google-search-results
!pip install arxiv
!pip install langchain_experimental
!pip install langchain_community --quiet

import os

os.environ['COHERE_API_KEY'] = "tmMUFWVR0IkJOwL6C0P1GEXcG5pFlvmpfiMQoSfo"

#Better way
#from google.colab import userdata
#os.environ['OPENAI_API_KEY'] = userdata.get("OPENAI_API_KEY")
#os.environ['COHERE_API_KEY'] = userdata.get("COHERE_API_KEY")

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI, Cohere
from langchain.chat_models import ChatOpenAI

from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.agents import AgentType

from google.colab import files
import pandas as pd

# Step 1: Upload the file
uploaded = files.upload()

# Step 2: Get the file name
file_name = list(uploaded.keys())[0]

# Step 3: Load the CSV into a pandas DataFrame
df = pd.read_csv(file_name)

# Display the first few rows of the DataFrame
df.head()

#from langchain.agents import create_csv_agent, AgentType # This line is causing the error
from langchain_experimental.agents.agent_toolkits import create_csv_agent # This is the corrected import
from langchain.agents import AgentType # Keep this line as it is
from langchain.llms import Cohere


# Step 1: Initialize Cohere LLM
COHERE_API_KEY = "tmMUFWVR0IkJOwL6C0P1GEXcG5pFlvmpfiMQoSfo"  # Replace with your actual Cohere API key
llm = Cohere(cohere_api_key=COHERE_API_KEY, model="command-xlarge-nightly", temperature=0)

# Step 2: Path to your CSV file
csv_file_path = "order12.csv"

# Step 3: Create CSV Agent
agent = create_csv_agent(
    llm=llm,
    path=csv_file_path,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    allow_dangerous_code=True,  # Required for executing Pandas-related queries
    verbose=True  # Enables detailed output for debugging
)

# Step 4: Query the CSV Agent
query = "What are the column names in the dataset?"
result = agent.run(query)

# Step 5: Print the result
print(result)

result=agent.run("What is the total Payable Amt per Product Name?")
print(result)

from flask import Flask, request, jsonify, render_template
import os
import pandas as pd
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.agents import AgentType
# Changed import from langchain_community.llms to langchain.llms
from langchain.llms import Cohere

app = Flask(__name__)

# Set your Cohere API key
COHERE_API_KEY = "tmMUFWVR0IkJOwL6C0P1GEXcG5pFlvmpfiMQoSfo"
os.environ['COHERE_API_KEY'] = COHERE_API_KEY

# Initialize the Cohere LLM
llm = Cohere(cohere_api_key="tmMUFWVR0IkJOwL6C0P1GEXcG5pFlvmpfiMQoSfo", model="command-xlarge-nightly", temperature=0)

# Path to the static file
STATIC_FILE_PATH = os.path.join("uploads", "order12.csv")

# Ensure the uploads directory exists
os.makedirs("uploads", exist_ok=True)

@app.route('/')
def home():
    return render_template("index.html")  # Ensure index.html exists in a 'templates' folder

@app.route('/setup', methods=['POST'])
def setup_agent():
    """
    Prepares the agent by loading the static file `order12.csv`.
    """
    try:
        if not os.path.exists(STATIC_FILE_PATH):
            return jsonify({"error": f"Static file '{STATIC_FILE_PATH}' not found. Please upload it."})

        # Create the CSV agent
        global agent
        agent = create_csv_agent(
            llm=llm,
            path=STATIC_FILE_PATH,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            allow_dangerous_code=True,
            verbose=True
        )
        return jsonify({"message": f"Agent set up successfully with file '{STATIC_FILE_PATH}'!"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/query', methods=['POST'])
def query_csv():
    """
    Query the loaded `order12.csv` file.
    """
    # Check if the agent is initialized
    if 'agent' not in globals():
        return jsonify({"error": "Agent not set up. Please set up the agent first by calling the '/setup' endpoint."})

    # Get the query from the request
    query = request.json.get('query', '')
    if not query:
        return jsonify({"error": "Query is required"})

    # Execute the query
    try:
        result = agent.run(query)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    # Save the static file (order12.csv) into the uploads folder for the first run
    STATIC_FILE_CONTENT = """Product Name,Payable Amt
    Product A,500
    Product B,300
    Product C,700"""
    if not os.path.exists(STATIC_FILE_PATH):
        with open(STATIC_FILE_PATH, 'w') as file:
            file.write(STATIC_FILE_CONTENT)

    app.run(debug=True, host="0.0.0.0", port=5000)



from flask import Flask, request, jsonify
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import Cohere
from langchain.agents import AgentType
import os

# Initialize Flask app
app = Flask(__name__)

# Load API key from environment variable
COHERE_API_KEY = os.environ.get('COHERE_API_KEY', 'tmMUFWVR0IkJOwL6C0P1GEXcG5pFlvmpfiMQoSfo')

# Initialize Cohere LLM
llm = Cohere(cohere_api_key=COHERE_API_KEY, model="command-xlarge-nightly", temperature=0)

# Path to your CSV file
CSV_FILE_PATH = "order12.csv"  # Ensure this file exists in the same directory as app.py

# Create CSV Agent
agent = create_csv_agent(
    llm=llm,
    path=CSV_FILE_PATH,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    allow_dangerous_code=True,
    verbose=True
)

@app.route('/query', methods=['POST'])
def query_csv_agent():
    # Get query from request
    data = request.json
    query = data.get('query', '')

    if not query:
        return jsonify({'error': 'Query not provided'}), 400

    # Run query through the agent
    try:
        result = agent.run(query)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

!python app.py

!curl -X POST http://127.0.0.1:5000/query \
-H "Content-Type: application/json" \
-d '{"query": "What are the column names in the dataset?"}'

# Install specific version if the conflict still exists
!pip install opentelemetry-exporter-prometheus==0.49b2
import os
os.kill(os.getpid(), 9)



from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.llms import Cohere
from langchain.serve import LangServe, Runnable, document

COHERE_API_KEY = "tmMUFWVR0IkJOwL6C0P1GEXcG5pFlvmpfiMQoSfo"  # Replace with your actual Cohere API key
llm = Cohere(cohere_api_key=COHERE_API_KEY, model="command-xlarge-nightly", temperature=0)

csv_file_path = "order12.csv"  # Make sure this file is in the same directory as your notebook or provide the correct path

agent = create_csv_agent(
    llm=llm,
    path=csv_file_path,
    verbose=True
)

@document
class CSVAgentRunnable(Runnable):
    def __init__(self, agent):
        self.agent = agent

    def invoke(self, input: str) -> str:
        return self.agent.run(input)

app = LangServe()
app.add_runnable(CSVAgentRunnable(agent), name="csv_agent")

import uvicorn
uvicorn.run(app, host="127.0.0.1", port=8000)

