import pandas as pd
import re
import Neo4j.pyScript.Manager.API_Manager as Manager

author_data = {
    "authorId": None,
    "name": None,
    "birthdate": None,
    "nationality": None
}

df =pd.DataFrame(author_data, index=[0])
df.drop(0, inplace=True)

def generate_author_file():
    
    books_df = Manager.retrieve_books()
    books_df.drop(columns=['genres', 'bookId', 'title', 'publicationYear', 'language', 'description'], inplace=True)
    for authors in books_df['authors']:
        for author in authors:
            df.loc[len(df)] = [author['authorId'], author['name'], author['birthdate'], author['nationality']]
    
    Manager.create_file(df, ["authors.csv", "authors.json"])
            