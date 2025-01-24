import pandas as pd
import os
import Manager.API_Manager as Manager

def generate_author_csv():

    # Define the dataframe
    dataFrame = {
        "authorId" : None,
        "Books" : []
    }

    df_authors =pd.DataFrame(dataFrame)

    # Init of author id list
    authorId_list = []

    # Get all the authors 
    data = Manager.retrive_author()
    authors = data.get("data", {}).get("authors", [])

    # Save the authors id in a list
    for author in authors:
        authorId_list.append(author["id"])

    # For each author, find all the books that he wrote
    for id in authorId_list:
        author_book = Manager.retrieve_book_author(id)
        books = author_book.get("data", {}).get("books")
        books_list_for_author = []
        for book in books:
            # Extract book id
            bookId = book.get("id")
            # Extract the publication year
            publicationYear = book.get("release_year")
            # Extract the genre
            cached_tags = book.get("cached_tags", None)
            tag_list = cached_tags.get("Genre", None)
            genre = []
            if (tag_list):
                for element in tag_list:
                    genre.append(element["tag"])
            else:
                genre = None
            
            books_list_for_author.append({"bookId" : bookId, "publicationYear" : publicationYear, "genre" : genre})  
  
        # Add to the dataframe the new row
        df_authors.loc[len(df_authors)] = [id, books_list_for_author]
        
    Manager.create_file(df_authors,["authors.csv", "authors.json"])