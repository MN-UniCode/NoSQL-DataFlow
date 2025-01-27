import pandas as pd
import re
import Neo4j.pyScript.Manager.API_Manager as Manager

# Create the pandas dataframe
book_data = {
    "bookId": None,
    "title": None,
    "publicationYear": None,
    "description": None,
    "language": None
}

df = pd.DataFrame(book_data, index=[0])
df.drop(0, inplace=True)

def generate_books_file():
    books_df= Manager.retrieve_books()
    df = books_df.drop(columns=['genres', 'authors'])

    Manager.create_file(df, ["books.csv", "books.json"])