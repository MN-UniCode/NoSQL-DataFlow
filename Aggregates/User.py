import pandas as pd
from Manager.API_Manager import retrieve_users

# Create the pandas dataframe
user_data = {
    "userId": None,
    "books": []
}

df = pd.DataFrame(user_data)

data = retrieve_users()

# Extract the users informations
users = data.get("data", {}).get("users", [])

# Get each user and add the information to the dataframe
for user in users:
    userId = user.get("id", None)
    user_books = user.get("user_books", None)
    books = []
    if user_books:
        for book_entry in user_books:
            book = book_entry.get("book", None)
            book_info = {}

            # Manage atomic values
            book_info["bookId"] = book.get("id", None)
            book_info["title"] = book.get("title", None)
            book_info["publicationYear"] = book.get("release_year", None)
            book_info["description"] = book.get("description", None)
            book_info["language"] = "English"

            # Manage genres (nested values)
            tags = book.get("cached_tags", None)
            book.pop("cached_tags")
            genre_tags = tags.get("Genre", None)
            genres = []
            if genre_tags:
                for genre in genre_tags:
                    new = {
                        "name" : genre.get("tag", None)
                    }
                    genres.append(new)
            book_info["genres"] = genres

            # Create the books object
            books.append(book_info)

    df.loc[len(df)] = [userId, books]

    # Create a CSV file
    df.to_csv("users.csv", index=False)
    # print(df)
    
    # Create a JSON file
    df.to_json("users.json", orient='records', indent=4, index=False)
    # print(df)