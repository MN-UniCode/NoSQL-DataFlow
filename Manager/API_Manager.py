import requests
import pandas as pd
from config.config import API_KEY
 
url = "https://api.hardcover.app/v1/graphql"
headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY  # Replace with your API key
}

query = """
query MyQuery {
  books(limit: 10) {
    id
    description
    release_year
    title
    recommendations {
      score
      id
      context
      updated_at
    }
  }
}
"""

# Create the pandas dataframe
book_data = {
    "id": None,  # To be updated dynamically
    "description": None,  # To be updated dynamically
    "release_year": None,  # To be updated dynamically
    "title": None,  # To be updated dynamically
    "reviews": []
}

df = pd.DataFrame(book_data)

# Sending the request
response = requests.post(url, json={"query": query}, headers=headers)

# Checking the response
if response.status_code == 200:
    data = response.json()  # Parsed JSON response
    
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
            recommendations[i]["userId"] = None
        
        df.loc[len(df)] = [id, description, release_year, title, recommendations]
        #print(f"recommendations: {recommendations}")
else:
    print(f"Error: {response.status_code}, {response.text}")


print(df)