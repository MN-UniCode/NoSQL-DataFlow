import Neo4j.pyScript.Manager.API_Manager as Manager
from Neo4j.pyScript.nodes import GraphDataGenerator
from Neo4j.pyScript.relationships import RelationshipDataGenerator

books_df = Manager.retrieve_books()

Node = GraphDataGenerator()
Node.generate_all_nodes(books_df)

Relationship = RelationshipDataGenerator()
Relationship.generate_all_relationships(books_df)

