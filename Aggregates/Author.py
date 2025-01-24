import pandas as pd

def find_all_author_id(df):
    id_author = []
    for author in df["authors"]:
        for authorId in author:
            id_author.append(authorId["author_id"])
    return id_author

def find_books_by_id(df, author_id=96097):
    id_book = []
    book_relase = []
    genre = []
    i = 0
    for author in df["authors"]:
        for authorId in author:
            if author_id == authorId["author_id"]:
                id_book.append(df.iloc[i]["id"])
                book_relase.append(df.iloc[i]["release_year"])
                genre.append(df.iloc[i]["genre"])
        i += 1
    
    return list(zip(id_book, book_relase, genre))

def generate_author_csv(response):

    # Create the pandas dataframe for books
    book_data = {
        "id": None,
        "description": None,
        "release_year": None,
        "title": None,
        "publisherId" : None,
        "reviews": [],
        "authors" : [],
        "genre" : []
    }

    df = pd.DataFrame(book_data)

    # Parsed JSON response 
    data = response.json()  
    
    # Extract the books informations
    books = data.get("data", {}).get("books", [])
    # Get book and add the iformation to the dataframe
    for book in books:
        id = book.get("id", None)
        description = book.get("description", None)
        release_year = book.get("release_year", None)
        title = book.get("title", None)
        recommendations = book.get("recommendations", None)
        authors = book.get("contributions", None)

        # Add the userId to reviews in according to Cassandra schema
        for i in range(0, len(recommendations)-1):
            recommendations[i]["userId"] = None

        # Extract the genre
        cached_tags = book.get("cached_tags", None)
        tag_list = cached_tags.get("Genre", None)
        genre = []
        if (tag_list):
            for element in tag_list:
                genre.append(element["tag"])
        else:
            genre = None
        
        # add the new row to df
        df.loc[len(df)] = [id, description, release_year, title, 1, recommendations, authors, genre]

    # Create dataframes for the authors
    authors_data = {
        "authorId" : None,
        "books" : []
    }

    df_authors = pd.DataFrame(authors_data)

    # I have to extract the author id form the books
    author_id = set(find_all_author_id(df))

    # For each autho, find all the books that he wrote
    for id in author_id:
        author_book = []
        for bookId, year, genre in find_books_by_id(df, id):
                author_book.append({"bookId" : bookId, "relaseYear" : year, "genre" : genre})
        # Add to the dataframe the new row
        df_authors.loc[len(df_authors)] = [id, author_book]

    df_authors.to_csv("author.csv", index=False)
    df_authors.to_json("author.json", orient='records', indent=4, index=False)


