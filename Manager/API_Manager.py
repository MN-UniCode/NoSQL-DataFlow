import requests
import pandas as pd
from config.config import API_KEY
import Aggregates.Book as AB
import Aggregates.User as AU
 
url = "https://api.hardcover.app/v1/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
}

query_books = """
query MyQuery {
  books(limit: 10) {
    id
    description
    release_year
    title
    recommendations {
      score
      id
      context
      updated_at
    }
  }
}
"""

query_users = """
query MyQuery {
  users(limit: 10) {
    id
    user_books {
      book_id
      book {
        id
        description
        title
        release_year
        cached_tags
      }
    }
  }
}
"""

# Sending the request for books
response = requests.post(url, json={"query": query_books}, headers=headers)
if response.status_code == 200:
    AB.generate_books_csv(response)
else:
    print(f"Error: {response.status_code}, {response.text}")

# Sending the request for users
response = requests.post(url, json={"query": query_users}, headers=headers)
if response.status_code == 200:
    AU.generate_users_csv(response)
else:
    print(f"Error: {response.status_code}, {response.text}")