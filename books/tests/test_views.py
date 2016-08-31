from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from books.views import list_books
from books.factories import AuthorFactory, BookFactory, ReviewFactory

class TestListBooks(TestCase) :
    def test_list_books_url(self) :
        # we test if the root url returns the correct view
        url = resolve('/')
        self.assertEqual(url.func, list_books)

    def test_list_books_template(self) :
        # we test is we are using the correct template
        # get the reverse, being the url of our list_books view to feed that into the get
        # method to get the response
        response = self.client.get(reverse(list_books))
        self.assertTemplateUsed(response, 'list.html')

    def test_list_books_returns_books_with_reviews(self) :
        # this view only returns books with a review
        # so we test another thing, we make a set of reviewed books and a set of
        # not reviewed books and test.
        author = AuthorFactory()
        books_with_reviews = ReviewFactory.create_batch(2, authors = [author, ])
        books_without_reviews = BookFactory.create_batch(4, authors = [author, ])

        response = self.client.get(reverse(list_books))
        books = list(response.context['books'])

        self.assertEqual(books_with_reviews, books)
        self.assertNotEqual(books_without_reviews, books)
