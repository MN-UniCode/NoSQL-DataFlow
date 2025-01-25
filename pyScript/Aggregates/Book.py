import pandas as pd
import pyScript.Manager.API_Manager as Manager

# Create the pandas dataframe
book_data = {
    "bookId": None,
    "title": None,
    "publicationYear": None,
    "description": None,
    "language": None,
    "reviews": [],
    "publisherId" : None
}

df = pd.DataFrame(book_data)

def generate_books_file():
    data = Manager.retrieve_books()
        
    # Extract the books informations
    books = data.get("data", {}).get("books", [])

    # Get each book and add the information to the dataframe
    for book in books:
        # Manage atomic values
        id = book.get("id", None)
        description = book.get("description", None)
        release_year = book.get("release_year", None)
        title = book.get("title", None)

        # Manage reviews (nested values)
        reviews = []
        data_rev = Manager.retrieve_book_reviews(id)
        if data_rev:
            user_book_data = data_rev.get("data", {}).get("user_book_reads", [])
            if user_book_data:
                for entry in user_book_data:
                    review_data = entry.get("user_book", [])
                    if review_data.get("rating", None) and review_data.get("rating", None) != 'null' and review_data.get("rating", None) is not None:
                        new = {
                            "reviewId" : review_data.get("id", None),
                            "score" : int(review_data.get("rating", None)),
                            "comment" : review_data.get("review", None),
                            "date" : review_data.get("date_added", None),
                            "userId" : review_data.get("user_id", None)
                        }
                        reviews.append(new)
        else:
            print(f"No reviews found for bookId: {id}")
        
        # Find the correct publisherId
        data = Manager.retrieve_publisher_by_book(id)
        pubId = None
        if data:
            editions = data.get("data", {}).get("editions", [])
            if editions:
                pubId = editions[len(editions)-1].get("publisher_id", None)
                # print(f"pubId: {pubId}, bookId: {id}")
            # else:
                # print(f"No editions found for bookId: {id}")

        df.loc[len(df)] = [id, title, release_year, description, "English", reviews, pubId]
        # print(f"recommendations: {recommendations}")

    Manager.create_file(df, ["books.csv", "books.json"])