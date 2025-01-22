import requests
 
# Define your API key and endpoint
api_key = "YOUR_API_KEY"  # Replace with your NYT Books API key
endpoint = "https://api.nytimes.com/svc/books/v3/lists/full-overview.json"
 
# Define parameters (optional: specify a published date)
params = {
    "api-key": api_key,
    # Uncomment the line below and specify a date if you want data for a specific date
    # "published_date": "2025-01-01"  # Format: YYYY-MM-DD
}
 
# Make the GET request to the NYT Books API
response = requests.get(endpoint, params=params)
 
# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Extract and print the list of books
    for list_info in data["results"]["lists"]:
        print(f"List Name: {list_info['list_name']}")
        for book in list_info["books"]:
            print(f"  Title: {book['title']}")
            print(f"  Author: {book['author']}")
            print(f"  Publisher: {book['publisher']}")
            print(f"  Description: {book['description']}")
            print("-" * 40)
else:
    print(f"Error: {response.status_code} - {response.text}")