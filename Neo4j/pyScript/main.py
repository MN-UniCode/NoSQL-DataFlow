import Neo4j.pyScript.Aggregates.Author as Author
import Neo4j.pyScript.Aggregates.Book as Book
import Neo4j.pyScript.Aggregates.User as User
import Neo4j.pyScript.Aggregates.Genere as Genre
import Neo4j.pyScript.Manager.API_Manager as Manager

books_df = Manager.retrieve_books()
Book.generate_books_file(books_df)
Genre.generate_genre_file(books_df)
Author.generate_author_file(books_df)

"""
select = -1
while select < 0 or select > 5:
    select = int(input("Do you want to extract Books(0), Users(1), Authors(2), Reviews(3), Genres(4) or Publishers(5)?\n"))
if select == 0:
    Book.generate_books_file()
elif select ==1:
    User.generate_users_file()
elif select == 2:
    Author.generate_author_file()
elif select == 4:
    Genre.generate_genre_file()
"""