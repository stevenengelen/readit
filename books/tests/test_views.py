from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from books.views import list_books, ReviewList
from books.factories import AuthorFactory, BookFactory, ReviewFactory, UserFactory
from books.models import Book

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

class TestReviewList(TestCase) :
    def setUp(self) :
        self.user = UserFactory(username = 'test')
        self.author = AuthorFactory()

    def test_reviews_url(self) :
        url = resolve('/review/')
        # check that the urls directs us to the right function (which is a classbased view)
        self.assertEqual(url.func.__name__, ReviewList.__name__)

    def test_authentication_control(self) :
        # check what happens when we acces the review page with an unauthenticated user
        # for this we are going to do a simple print statement to see it in the terminal
        response = self.client.get(reverse('review-books'))
        print(response.status_code)
        # it should print a redirect code, and it will redirect us to the login page (see settings.py)
        self.assertEqual(response.status_code, 302)

        # next we check what happens when we have an authenticated user
        # the response is 200, and we use the django buildin function login
        self.client.login(username = 'test', password = 'test')
        response = self.client.get(reverse('review-books'))
        self.assertEqual(response.status_code, 200)

        # finally, we want to test we are using the correct template
        self.assertTemplateUsed(response, 'list-to-review.html')

    def test_review_list_returns_books_to_review(self) :
        # Setup our data
        books_without_reviews = BookFactory.create_batch(2, authors = [self.author, ])

        self.client.login(username = 'test', password = 'test')
        response = self.client.get(reverse('review-books'))

        books = list(response.context['books'])
        self.assertEqual(books, books_without_reviews)

    def test_can_create_new_book(self) :
        self.client.login(username = 'test', password = 'test')
        response = self.client.post(
                reverse('review-books'),
                data = {
                    'title' : 'My Brand New Book',
                    'authors' : [self.author.pk,],
                    'reviewed_by' : self.user.pk,
                    },
                )

        self.assertIsNotNone(Book.objects.get(title = 'My Brand New Book'))
