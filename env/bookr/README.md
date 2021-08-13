

WEB DEVELOPEMNT WITH DJANGO

Throughout this book, we will be building a book review website named Bookr. It will allow you to add fields for publishers, contributors, books, and reviews. A publisher will publish one or more books, and each book will have one or more contributors (author, editor, co-author, and so on). Only admin users will be allowed to modify these fields. Once a user has signed up for an account on the site, they will be able to start adding reviews to a book.


DATABSE 

Book: This is the database table that holds the information about the book itself. We have already created a Book model and have migrated this to the database.
Publisher: This table holds information about the book publisher.
Contributor: This table holds information about the contributor, that is, the author, co-author, or editor.
Review: This table holds information about the review comments posted by the reviewers.