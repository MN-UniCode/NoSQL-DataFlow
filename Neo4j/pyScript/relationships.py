import pandas as pd
import Neo4j.pyScript.Manager.API_Manager as Manager

class RelationshipDataGenerator:
    def __init__(self):
        pass

    def __initialize_dataframe(self, data):
        df = pd.DataFrame(data, index=[0])
        df.drop(0, inplace=True)
        return df

    def __generate_author_book_file(self, books_df):
        author_book_data = {
            "bookId": None,
            "authorId": None
        }
        df = self.__initialize_dataframe(author_book_data)

        for _, book in books_df.iterrows():
            author_list = [author['authorId'] for author in book['authors']]
            for author_id in author_list:
                df.loc[len(df)] = [book['bookId'], author_id]

        Manager.create_file(df, ["author_book.csv", "author_book.json"])

    def __generate_genre_book_file(self, books_df):
        genre_book_data = {
            "bookId": None,
            "genreId": None
        }
        df = self.__initialize_dataframe(genre_book_data)

        for _, book in books_df.iterrows():
            genre_list = book['genres']
            for genre in genre_list:
                df.loc[len(df)] = [book['bookId'], genre]

        Manager.create_file(df, ["genre_book.csv", "genre_book.json"])

    def __generate_publisher_book_file(self, books_df):
        publisher_book_data = {
            "bookId": None,
            "publisherId": None
        }
        df = self.__initialize_dataframe(publisher_book_data)

        for _, book in books_df.iterrows():
            publisher_id = book['publisher'].get('publisherId')
            if publisher_id:
                df.loc[len(df)] = [book['bookId'], int(publisher_id)]

        Manager.create_file(df, ["publisher_book.csv", "publisher_book.json"])

    def __generate_review_book_file(self, books_df):
        review_book_data = {
            "bookId": None,
            "reviewId": None
        }
        df = self.__initialize_dataframe(review_book_data)

        for _, book in books_df.iterrows():
            review_list = [review['reviewId'] for review in book['reviews']]
            for review_id in review_list:
                df.loc[len(df)] = [book['bookId'], review_id]

        Manager.create_file(df, ["review_book.csv", "review_book.json"])

    def __generate_user_book_file(self, books_df):
        user_book_data = {
            "bookId": None,
            "userId": None
        }
        df = self.__initialize_dataframe(user_book_data)

        for _, book in books_df.iterrows():
            user_list = [user['userId'] for user in book['users']]
            for user_id in user_list:
                df.loc[len(df)] = [book['bookId'], user_id]

        Manager.create_file(df, ["user_book.csv", "user_book.json"])

    def __generate_user_review_file(self, books_df):
        user_review_data = {
            "userId": None,
            "reviewId": None
        }
        df = self.__initialize_dataframe(user_review_data)

        for _, book in books_df.iterrows():
            for review in book['reviews']:
                user_id = book['users'][0]['userId']  # Assuming the first user wrote the review
                df.loc[len(df)] = [user_id, review['reviewId']]

        Manager.create_file(df, ["user_review.csv", "user_review.json"])

    def generate_all_relationships(self, books_df):
        self.__generate_author_book_file(books_df)
        self.__generate_genre_book_file(books_df)
        self.__generate_publisher_book_file(books_df)
        self.__generate_review_book_file(books_df)
        self.__generate_user_book_file(books_df)
        self.__generate_user_review_file(books_df)
