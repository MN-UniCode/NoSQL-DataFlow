import pandas as pd
import Neo4j.pyScript.Manager.API_Manager as Manager

# Dataframes

# Book dataframe
book_data = {
    "bookId": None,
    "title": None,
    "publicationYear": None,
    "description": None,
    "language": None
}

df = pd.DataFrame(book_data, index=[0])
df.drop(0, inplace=True)

# Author dataframe
author_data = {
    "authorId": None,
    "name": None,
    "birthdate": None,
    "nationality": None
}

df =pd.DataFrame(author_data, index=[0])
df.drop(0, inplace=True)

# Genre dataframe
genre_data ={ 'name' : [] }

# Generate files functions

# Book function
def generate_books_file(books_df):
    df = books_df.drop(columns=['genres', 'authors'])

    Manager.create_file(df, ["books.csv", "books.json"])

# Author function
def generate_author_file(books_df):
    for authors in books_df['authors']:
        for author in authors:
            df.loc[len(df)] = [author['authorId'], author['name'], author['birthdate'], author['nationality']]

    Manager.create_file(df, ["authors.csv", "authors.json"])

# Genre function
def generate_genre_file(books_df):
    books_df['genres'] = books_df['genres']

    for genres in books_df['genres']:
        for genre in genres:
            genre_data['name'].append(genre)

    df = pd.DataFrame(genre_data)
    Manager.create_file(df, ["genres.csv", "genres.json"])

# Generate all nodes function
def generate_all_nodes(books_df):
    generate_books_file(books_df)
    generate_author_file(books_df)
    generate_genre_file(books_df)