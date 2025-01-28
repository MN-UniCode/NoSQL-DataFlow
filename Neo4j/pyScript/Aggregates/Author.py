import pandas as pd
import re
import Neo4j.pyScript.Manager.API_Manager as Manager

author_data = {
    "authorId": None,
    "name": None,
    "birthdate": None,
    "nationality": None
}

df =pd.DataFrame(author_data, index=[0])
df.drop(0, inplace=True)

def generate_author_file(books_df):
    # books_df.drop(columns=['genres', 'bookId', 'title', 'publicationYear', 'language', 'description'], inplace=True)
    for authors in books_df['authors']:
        for author in authors:
            df.loc[len(df)] = [author['authorId'], author['name'], author['birthdate'], author['nationality']]
    
    Manager.create_file(df, ["authors.csv", "authors.json"])

def generate_author_book_file(books_df):
    author_book_data = {
        "bookId": None,
        "authorId": None
    }
    df = pd.DataFrame(author_book_data, index=[0])
    df.drop(0, inplace=True)
    # print(books_df)
    for index, book in books_df.iterrows():
        print(book)
        author_list = []
        for authors in book['authors']:
            author_list.append(authors['authorId'])
        for id in author_list:
            df.loc[len(df)] = [book['bookId'], id]
        
    Manager.create_file(df, ["author_book.csv", "author_book.json"])
            