import pandas as pd
from Manager.API_Manager import retrieve_books
from Manager.API_Manager import retrieve_publisher_by_book

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
    rev = book.get("recommendations", None)
    reviews = []
    for entry in rev:
        new_rev = {
            "reviewId" : entry.get("id", None),
            "score" : entry.get("score", None),
            "date" : entry.get("updated_at", None),
            "comment" : None
            # TODO: find the correct comment (review)
        }
        reviews.append(new_rev)

    # Add the userId to reviews in according to Cassandra schema
    for i in range(0, len(reviews)-1):
        #TODO: find the correct userId
        reviews[i]["userId"] = None
    
    #TODO: find the correct publisherId
    data = retrieve_publisher_by_book(id)
    pubId = None
    if data:
        editions = data.get("data", {}).get("editions", [])
        if editions:
            pubId = editions[len(editions)-1].get("publisher_id", None)
            print(f"pubId: {pubId}, bookId: {id}")
        else:
            print(f"No editions found for bookId: {id}")

    df.loc[len(df)] = [id, title, release_year, description, "English", reviews, pubId]
    # print(f"recommendations: {recommendations}")

# Create a CSV file
df.to_csv("books.csv", index=False)
# print(df)

# Create a JSON file
df.to_json("books.json", orient='records', indent=4, index=False)