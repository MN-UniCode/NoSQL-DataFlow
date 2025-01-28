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

# Book_Publisher function
def generate_publisher_book_file(books_df):
    publisher_book_data = {
        "bookId": None,
        "publisherId": None
    }
    df = pd.DataFrame(publisher_book_data, index=[0])
    df.drop(0, inplace=True)
    for index, book in books_df.iterrows():
        publisher_list = []
        if book['publisher']['publisherId']:
            publisher_list.append(int(book['publisher']['publisherId']))
        for id in publisher_list:
            df.loc[len(df)] = [book['bookId'], id]
    Manager.create_file(df, ["publisher_book.csv", "publisher_book.json"])

# Book_Review function
def generate_review_book_file(books_df):
    review_book_data = {
        "bookId": None,
        "reviewId": None
    }
    df = pd.DataFrame(review_book_data, index=[0])
    df.drop(0, inplace=True)
    for index, book in books_df.iterrows():
        review_list = []
        for reviews in book['reviews']:
            review_list.append(reviews['reviewId'])
        for id in review_list:
            df.loc[len(df)] = [book['bookId'], id]
    Manager.create_file(df, ["review_book.csv", "review_book.json"])

# Book_User function
def generate_user_book_file(books_df):
    user_book_data = {
        "bookId": None,
        "userId": None
    }
    df = pd.DataFrame(user_book_data, index=[0])
    df.drop(0, inplace=True)
    for index, book in books_df.iterrows():
        user_list = []
        for users in book['users']:
            user_list.append(users['userId'])
        for id in user_list:
            df.loc[len(df)] = [book['bookId'], id]
    Manager.create_file(df, ["user_book.csv", "user_book.json"])

# Review_User function
def generate_user_review_file(books_df):
    user_review_data = {
        "userId": None,
        "reviewId": None
    }
    df = pd.DataFrame(user_review_data, index=[0])
    df.drop(0, inplace=True)
    for index, book in books_df.iterrows():
        review_list = []
        for reviews in book['reviews']:
            review_list.append(reviews['reviewId'])
        for id in review_list:
            df.loc[len(df)] = [book['users'][0]['userId'], id]
    Manager.create_file(df, ["user_review.csv", "user_review.json"])

# Generate all relationships function
def generate_all_relationships(books_df):
    generate_author_book_file(books_df)
    generate_genre_book_file(books_df)
    generate_publisher_book_file(books_df)
    generate_user_book_file(books_df)
    generate_review_book_file(books_df)
    generate_user_review_file(books_df)