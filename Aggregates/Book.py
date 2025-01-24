import pandas as pd
from Manager.API_Manager import retrieve_books
from Manager.API_Manager import retrieve_publisher_by_book
from Manager.API_Manager import retrieve_book_reviews

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

data = retrieve_books()
    
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
    data_rev = retrieve_book_reviews(id)
    if data_rev:
        user_book_data = data_rev.get("data", {}).get("user_book_reads", [])
        if user_book_data:
            for entry in user_book_data:
                review_data = entry.get("user_book", [])
                if review_data.get("review", None) or review_data.get("rating", None):
                    new = {
                        "reviewiId" : review_data.get("id", None),
                        "score" : review_data.get("rating", None),
                        "comment" : review_data.get("review", None),
                        "date" : review_data.get("date_added", None),
                        "userId" : review_data.get("user_id", None)
                    }
                    reviews.append(new)
    else:
        print(f"No reviews found for bookId: {id}")
    
    #TODO: find the correct publisherId
    data = retrieve_publisher_by_book(id)
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

# Create a CSV file
df.to_csv("books.csv", index=False)
# print(df)

# Create a JSON file
df.to_json("books.json", orient='records', indent=4, index=False)