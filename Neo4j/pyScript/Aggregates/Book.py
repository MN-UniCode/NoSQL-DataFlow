import pandas as pd
import re
import Neo4j.pyScript.Manager.API_Manager as Manager

# Create the pandas dataframe
book_data = {
    "bookId": None,
    "title": None,
    "publicationYear": None,
    "description": None,
    "language": None
}

df = pd.DataFrame(book_data, index=[0])
df.drop(0, inplace=True)

def generate_books_file():
    data = Manager.retrieve_books()
    if data:
        books = data.get("data", {}).get("books", [])

        # Get each book and add the information to the dataframe
        for book in books:
            # Manage atomic values
            id = book.get("id", None)
            if book.get("description", None) is not None:
                description = re.sub(r'[^a-zA-Z0-9 ]', '', book.get("description"))
            else:
                description = book.get("description", None)
            release_year = book.get("release_year", None)
            title = book.get("title", None)

            df.loc[len(df)] = [id, title, release_year, description, "English"]
            # print(f"recommendations: {recommendations}")

    Manager.create_file(df, ["books.csv", "books.json"])