import time
import requests
import pandas as pd
from config.config import API_KEY

url = "https://api.hardcover.app/v1/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
}

query_books = """
query MyQuery {
  books(limit: 500) {
    id
    description
    release_year
    title
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

query_publishers = """
query MyQuery($book_id: Int!) {
  editions(where: {book_id: {_eq: $book_id}}) {
    publisher_id
    book_id
  }
}
"""

query_book_reviews = """
query MyQuery($book_id: Int!) {
  user_book_reads(where: {user_book: {book_id: {_eq: $book_id}}}) {
    user_book {
      review
      rating
      date_added
      id
      user_id
    }
  }
}
"""

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

# Sending the request for users with retry logic
def retrieve_users():
    return make_request_with_retries(query_users)

# Sending the request for publishers with retry logic
def retrieve_publisher_by_book(book_id):
    return make_request_with_retries(query_publishers, variables={"book_id": book_id})

# Sending the request for book reviews with retry logic
def retrieve_book_reviews(book_id):
    return make_request_with_retries(query_book_reviews, variables={"book_id": book_id})
