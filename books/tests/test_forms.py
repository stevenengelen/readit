from django.test import TestCase
from books.forms import ReviewForm, BookForm
from books.factories import AuthorFactory, BookFactory
from django.core.exceptions import NON_FIELD_ERRORS

class ReviewFormTest(TestCase) :
    def test_no_review(self) :
        # first we test to see what happens when we do not fill in a review
        form = ReviewForm(data = {
            'is_favourite' : False,
            })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('review', code = 'required'))
        
    def test_review_too_short(self) :
        # next we check what happens when we fill in a review that is too short
        form = ReviewForm(data = {
            'is_favourite' : False,
            'review' : 'Too short!',
            })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('review', code = 'min_length'))

class BookFormTest(TestCase) :
    def setUp(self) :
        self.author = AuthorFactory()
        self.book = BookFactory(title = 'MyNewBook', authors = [self.author,])

    def test_custom_validation_rejects_book_that_already_exists(self) :
        # next we test if an error is raised when we try to create a book that already exists
        form = BookForm(data = {
            'title' : 'MyNewBook',
            'authors' : [self.author.pk,],
            })

        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error(NON_FIELD_ERRORS, code = 'bookexists'))

    def test_custom_validation_accepts_new_book(self) :
        new_author = AuthorFactory()
        form = BookForm(data = {
            'title' : 'MyUniqueBook',
            'authors' : [new_author.pk,],
            })

        self.assertTrue(form.is_valid())
