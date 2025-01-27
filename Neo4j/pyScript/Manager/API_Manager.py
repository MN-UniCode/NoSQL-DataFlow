import time
import requests
import os
import re
import pandas as pd
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

book_data = {
    "bookId": None,
    "title": None,
    "publicationYear": None,
    "description": None,
    "language": None,
    "genres" : [],
    "authors" : []
}

query_books = """
query MyQuery {
  books(limit: 10, offset: 100, where: {description: {_is_null: false}}) {
    id
    release_year
    title
    description
    cached_tags
    contributions {
      author {
        born_date
        id
        name
        location
      }
    }
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
    data = make_request_with_retries(query_books)
    
    df = pd.DataFrame(book_data)
    
    if data:
        books = data.get("data", {}).get("books")
        
        if books:
            for book in books:

                author_data = {
                    "authorId": None,
                    "name": None,
                    "birthdate": None,
                    "nationality": None
                }

                author_list = []
                genres_list = []
                id = book.get("id", None)
                if book.get("description", None) is not None:
                    description = re.sub(r'[^a-zA-Z0-9 ]', '', book.get("description"))
                else:
                    description = book.get("description", None)
                release_year = book.get("release_year", None)
                title = book.get("title", None)

                contibutions = book.get("contributions", None)
                if contibutions:
                    for contribution in contibutions:
                        author = contribution.get("author", None)
                        if author:
                            author_data["authorId"] = author.get("id", None)
                            author_data["name"] = author.get("name", None)
                            author_data["nationality"] = author.get("location", None)
                            author_data["birthdate"] = author.get("born_date", None)
                            author_list.append(author_data)
                
                cached_tags = book.get("cached_tags")
                if cached_tags:
                    genres = cached_tags.get("Genre")
                    for genre in genres:
                        if(genre.get("tag")):
                            genres_list.append(genre.get("tag"))
                df.loc[len(df)] = [id, title, release_year, description, "English",genres_list, author_list]

    return df


def create_file(df, filename):

    for i in range(0, N_TYPE_OF_FILE):
        full_path = os.path.join(os.getcwd(), RELATIVE_PATH[i], filename[i])
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if i == CSV:
            df.to_csv(full_path, index=False, na_rep= None)
        else:
             df.to_json(full_path, orient='records', indent=4, index=False)