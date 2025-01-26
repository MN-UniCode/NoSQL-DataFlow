import time
import requests
import os
from config.config import API_KEY

N_TYPE_OF_FILE = 2
RELATIVE_PATH = ["CSV", "JSON"]
CSV = 0

url = "https://api.hardcover.app/v1/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
}

query_books = """
query MyQuery {
  books(where: {release_year: {_is_null: false}}) {
    id
    description
    release_year
    title
  }
}
"""

query_users = """
query MyQuery($offset: Int!) {
  users(
    where: {user_books: {book: {release_year: {_is_null: false}}}}
    offset: $offset
  ) {
    id
    user_books(limit: 4) {
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

query_author = """
query MyQuery($offset: Int!) {
  authors(where: {books_count: {_gt: 2}}, offset: $offset) {
    id
  }
}

"""

query_book_author = """
query MyQuery($author_id: Int!) {
  books(
    where: {contributions: {author_id: {_eq: $author_id}, book: {release_year: {_is_null: false}}}}
  ) {
    id
    release_year
    cached_tags
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

# Sending the request for users with retry logic
def retrieve_users(offset):
    return make_request_with_retries(query_users, variables={"offset": offset})

# Sending the request for publishers with retry logic
def retrieve_publisher_by_book(book_id):
    return make_request_with_retries(query_publishers, variables={"book_id": book_id})

# Sending the request for book reviews with retry logic
def retrieve_book_reviews(book_id):
    return make_request_with_retries(query_book_reviews, variables={"book_id": book_id})

def retrive_author(offset):
    return make_request_with_retries(query_author, variables={"offset": offset})

def retrieve_book_author(author_id):
    return make_request_with_retries(query_book_author, variables={"author_id": author_id})

def create_file(df, filename):

    for i in range(0, N_TYPE_OF_FILE):
        full_path = os.path.join(os.getcwd(), RELATIVE_PATH[i], filename[i])
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if i == CSV:
            df.to_csv(full_path, index=False, na_rep= None)
        else:
             df.to_json(full_path, orient='records', indent=4, index=False)