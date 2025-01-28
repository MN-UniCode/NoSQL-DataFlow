import pandas as pd
import Neo4j.pyScript.Manager.API_Manager as Manager

class GraphDataGenerator:
    def __init__(self):
        # Private DataFrames
        self.__df_author = self.__initialize_dataframe({
            "authorId": None,
            "name": None,
            "birthdate": None,
            "nationality": None
        })

        self.__genre_data = {'name': []}

        self.__df_publisher = self.__initialize_dataframe({
            "publisherId": None,
            "name": None,
            "country": None
        })

        self.__df_review = self.__initialize_dataframe({
            "reviewId": None,
            "score": None,
            "comment": None,
            "date": None
        })

        self.__df_user = self.__initialize_dataframe({
            "userId": None,
            "name": None,
            "birthdate": None,
            "nationality": None
        })

    def __initialize_dataframe(self, data):
        df = pd.DataFrame(data, index=[0])
        df.drop(0, inplace=True)
        return df

    def __generate_books_file(self, books_df):
        df = books_df.drop(columns=['genres', 'authors'])
        Manager.create_file(df, ["books.csv", "books.json"])

    def __generate_author_file(self, books_df):
        for authors in books_df['authors']:
            for author in authors:
                self.__df_author.loc[len(self.__df_author)] = [
                    author['authorId'], author['name'], author['birthdate'], author['nationality']
                ]
        Manager.create_file(self.__df_author, ["authors.csv", "authors.json"])

    def __generate_genre_file(self, books_df):
        for genres in books_df['genres']:
            for genre in genres:
                self.__genre_data['name'].append(genre)

        df = pd.DataFrame(self.__genre_data)
        Manager.create_file(df, ["genres.csv", "genres.json"])

    def __generate_publisher_file(self, books_df):
        for publishers in books_df['publisher']:
            self.__df_publisher.loc[len(self.__df_publisher)] = [
                publishers['publisherId'], publishers['name'], publishers['country']
            ]
        Manager.create_file(self.__df_publisher, ["publishers.csv", "publishers.json"])

    def __generate_review_file(self, books_df):
        for reviews in books_df['reviews']:
            for review in reviews:
                self.__df_review.loc[len(self.__df_review)] = [
                    review['reviewId'], review['score'], review['comment'], review['date']
                ]
        Manager.create_file(self.__df_review, ["reviews.csv", "reviews.json"])

    def __generate_user_file(self, books_df):
        for users in books_df['users']:
            for user in users:
                self.__df_user.loc[len(self.__df_user)] = [
                    user['userId'], user['name'], user['birthdate'], user['nationality']
                ]
        Manager.create_file(self.__df_user, ["users.csv", "users.json"])

    # Public method
    def generate_all_nodes(self, books_df):
        self.__generate_books_file(books_df)
        self.__generate_author_file(books_df)
        self.__generate_genre_file(books_df)
        self.__generate_publisher_file(books_df)
        self.__generate_review_file(books_df)
        self.__generate_user_file(books_df)
