import Cassandra.pyScript.Aggregates.Author as Author
import Cassandra.pyScript.Aggregates.Book as Book
import Cassandra.pyScript.Aggregates.User as User

select = -1
while select < 0 or select > 2:
    select = int(input("Do you want to extract Books(0), Users(1) or Authors(2)?\n"))
if select == 0:
    Book.generate_books_file()
elif select ==1:
    User.generate_users_file()
else:
    Author.generate_author_file()