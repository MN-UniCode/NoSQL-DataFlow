import requests
import pandas as pd
from config.config import API_KEY
import Aggregates.Book as AB
import Aggregates.Author as AA
 
url = "https://api.hardcover.app/v1/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
}

query = """
query MyQuery {
  books(limit: 500) {
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
    contributions {
      author_id
    }
    cached_tags
  }
}
"""

# Sending the request
response = requests.post(url, json={"query": query}, headers=headers)
if response.status_code == 200:
    AB.generate_books_csv(response)
    AA.generate_author_csv(response)
else:
    print(f"Error: {response.status_code}, {response.text}")
