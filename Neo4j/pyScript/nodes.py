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

# Author dataframe
author_data = {
    "authorId": None,
    "name": None,
    "birthdate": None,
    "nationality": None
}

df_author =pd.DataFrame(author_data, index=[0])
df_author.drop(0, inplace=True)

# Genre dataframe
genre_data ={ 'name' : [] }

# Publisher dataframe
publisher_data = {
    "publisherId": None,
    "name": None,
    "country": None
}

df_publisher = pd.DataFrame(publisher_data, index=[0])
df_publisher.drop(0, inplace=True)

# Review dataframe
review_data = {
    "reviewId": None,
    "score": None,
    "comment": None,
    "date": None
}

df_review = pd.DataFrame(review_data, index=[0])
df_review.drop(0, inplace=True)

# User dataframe
user_data = {
    "userId": None,
    "name": None,
    "birthdate": None,
    "nationality": None
}

df_user = pd.DataFrame(user_data, index=[0])
df_user.drop(0, inplace=True)

# Generate files functions

# Book function
def generate_books_file(books_df):
    df = books_df.drop(columns=['genres', 'authors'])

    Manager.create_file(df, ["books.csv", "books.json"])

# Author function
def generate_author_file(books_df):
    for authors in books_df['authors']:
        for author in authors:
            df_author.loc[len(df_author)] = [author['authorId'], author['name'], author['birthdate'], author['nationality']]

    Manager.create_file(df_author, ["authors.csv", "authors.json"])

# Genre function
def generate_genre_file(books_df):
    books_df['genres'] = books_df['genres']

    for genres in books_df['genres']:
        for genre in genres:
            genre_data['name'].append(genre)

    df = pd.DataFrame(genre_data)
    Manager.create_file(df, ["genres.csv", "genres.json"])

# Publisher function
def generate_publisher_file(books_df):
    for publishers in books_df['publisher']:
        # print(publishers)
        df_publisher.loc[len(df_publisher)] = [publishers['publisherId'], publishers['name'], publishers['country']]

    Manager.create_file(df_publisher, ["publishers.csv", "publishers.json"])

# Review function
def generate_review_file(books_df):
    for reviews in books_df['reviews']:
        for review in reviews:
            # print(review)
            df_review.loc[len(df_review)] = [review['reviewId'], review['score'], review['comment'], review['date']]

    Manager.create_file(df_review, ["reviews.csv", "reviews.json"])

# User function
def generate_user_file(books_df):
    for users in books_df['users']:
        for user in users:
            df_user.loc[len(df_user)] = [user['userId'], user['name'], user['birthdate'], user['nationality']]

    Manager.create_file(df_user, ["users.csv", "users.json"])

# Generate all nodes function
def generate_all_nodes(books_df):
    generate_books_file(books_df)
    generate_author_file(books_df)
    generate_genre_file(books_df)
    generate_publisher_file(books_df)
    generate_review_file(books_df) 
    generate_user_file(books_df)