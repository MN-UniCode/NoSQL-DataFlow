import pandas as pd
import Neo4j.pyScript.Manager.API_Manager as Manager

# Author_Book function
def generate_author_book_file(books_df):
    author_book_data = {
        "bookId": None,
        "authorId": None
    }
    df = pd.DataFrame(author_book_data, index=[0])
    df.drop(0, inplace=True)

    for index, book in books_df.iterrows():
        print(book)
        author_list = []
        for authors in book['authors']:
            author_list.append(authors['authorId'])
        for id in author_list:
            df.loc[len(df)] = [book['bookId'], id]
        
    Manager.create_file(df, ["author_book.csv", "author_book.json"])

# Book_Genre function
def generate_genre_book_file(books_df):
    genre_book_data = {
        "bookId": None,
        "genreId": None
    }
    df = pd.DataFrame(genre_book_data, index=[0])
    df.drop(0, inplace=True)
    for index, book in books_df.iterrows():
        genre_list = []
        for genres in book['genres']:
            genre_list.append(genres)
        for genre in genre_list:
            df.loc[len(df)] = [book['bookId'], genre]
    Manager.create_file(df, ["genre_book.csv", "genre_book.json"])

# Generate all relationships function
def generate_all_relationships(books_df):
    generate_author_book_file(books_df)
    generate_genre_book_file(books_df)