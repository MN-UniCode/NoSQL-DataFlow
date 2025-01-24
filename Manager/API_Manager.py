import requests
import pandas as pd
import os
from config.config import API_KEY
# import Aggregates.Book as AB
import Aggregates.User as AU
 
url = "https://api.hardcover.app/v1/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
}

query_books = """
query MyQuery {
  books(limit: 100) {
    id
    description
    release_year
    title
    contributions {
      author_id
    }
    cached_tags
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
  user_book_reads(where: {user_book: {book_id: {_eq: 10}}}) {
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
query MyQuery(limit: 10) {
  authors {
    id
  }
}
"""

query_book_author = """
query MyQuery($author_id: Int!) {
  books(where: {contributions: {author_id: {_eq: $author_id}}}) {
    id
    release_year
    cached_tags
  }
}
"""

# Sending the request for books
def retrieve_books():
  response = requests.post(url, json={"query": query_books}, headers=headers)
  if response.status_code == 200:
      return response.json()
      # AB.generate_books_csv(response)
  else:
      print(f"Error: {response.status_code}, {response.text}")

# Sending the request for users
def retrieve_users():
  response = requests.post(url, json={"query": query_users}, headers=headers)
  if response.status_code == 200:
      AU.generate_users_csv(response)
  else:
      print(f"Error: {response.status_code}, {response.text}")

def retrieve_publisher_by_book(book_id):
    response = requests.post(
        url, 
        json={
        "query": query_publishers, 
        "variables": {"book_id": book_id}
        }, 
        headers=headers
        )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")

def retrieve_book_reviews(book_id):
    response = requests.post(
        url, 
        json={
        "query": query_book_reviews, 
        "variables": {"book_id": book_id}
        }, 
        headers=headers
        )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")

def retrive_author():
    response = requests.post(url, json={"query": query_author}, headers=headers)
    if response.status_code == 200:
        return response.json()
        # AB.generate_books_csv(response)
    else:
        print(f"Error: {response.status_code}, {response.text}")

def retrieve_book_author(author_id):
    response = requests.post(
        url, 
        json={
        "query": query_book_author, 
        "variables": {"author_id": author_id}
        }, 
        headers=headers
        )
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")

def create_file(df):
     # Save the file in CSV dir
    relative_path_csv = "../CSV"
    relative_path_json = "../JSON"
    
    file_name_csv = "author.csv"
    file_name_json = "author.json"

    full_path_csv = os.path.join(os.getcwd(), relative_path_csv, file_name_csv)
    full_path_json = os.path.join(os.getcwd(), relative_path_json, file_name_json)

    os.makedirs(os.path.dirname(full_path_csv), exist_ok=True)
    os.makedirs(os.path.dirname(full_path_json), exist_ok=True)

    df.to_csv(full_path_csv, index=False)
    df.to_json(full_path_json, orient='records', indent=4, index=False)