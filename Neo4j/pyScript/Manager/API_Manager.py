import time
import requests
import os
from config.config import API_KEY

url = "https://api.hardcover.app/v1/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
}

N_TYPE_OF_FILE = 2
RELATIVE_PATH = ["Neo4j/CSV", "Neo4j/JSON"]
CSV = 0

url = "https://api.hardcover.app/v1/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
}

query_books = """
query MyQuery {
  books(limit: 10, offset: 50, where: {description: {_is_null: false}}) {
    id
    release_year
    title
    description
  }
}
"""

# Sending the request for books
# Helper function to handle retries and exponential backoff for API requests
def make_request_with_retries(query, variables=None, max_retries=5):
    retries = 0

    while retries < max_retries:
        response = requests.post(
            url,
            json={"query": query, "variables": variables},
            headers=headers,
        )
        
        if response.status_code == 200:
            return response.json()
        
        elif response.status_code == 429:
            print("Received 429 error. Retrying...")
            retry_after = response.headers.get("Retry-After")
            
            if retry_after:
                time.sleep(int(retry_after))  # Wait for the specified time in Retry-After header
            else:
                time.sleep(2 ** retries)  # Exponential backoff
            
            retries += 1
        
        else:
            print(f"Error: {response.status_code}, {response.text}")
            break
    
    print("Max retries reached.")
    return None

# Sending the request for books with retry logic
def retrieve_books():
    return make_request_with_retries(query_books)

def retrieve_users():
    return make_request_with_retries(query_books)

# Sending the request for publishers with retry logic
def retrieve_publisher():
    return make_request_with_retries(query_books)

# Sending the request for book reviews with retry logic
def retrieve_genre():
    return make_request_with_retries(query_books)

def retrive_author():
    return make_request_with_retries(query_books)

def retrieve_review():
    return make_request_with_retries(query_books)

def create_file(df, filename):

    for i in range(0, N_TYPE_OF_FILE):
        full_path = os.path.join(os.getcwd(), RELATIVE_PATH[i], filename[i])
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if i == CSV:
            df.to_csv(full_path, index=False, na_rep= None)
        else:
             df.to_json(full_path, orient='records', indent=4, index=False)