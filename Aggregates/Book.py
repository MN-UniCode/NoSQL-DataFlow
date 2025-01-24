import pandas as pd

# Create the pandas dataframe
book_data = {
    "id": None,
    "description": None,
    "release_year": None,
    "title": None,
    "publisherId" : None,
    "reviews": []
}

df = pd.DataFrame(book_data)


def generate_books_csv(response):

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

        # Add the userId to reviews in according to Cassandra schema
        for i in range(0, len(recommendations)-1):
            #TODO: find the correct userId
            recommendations[i]["userId"] = None
        
        #TODO: find the correct publisherId
        df.loc[len(df)] = [id, description, release_year, title, 1, recommendations]
        #print(f"recommendations: {recommendations}")

    df.to_csv("books.csv", index=False)
    #print(df)