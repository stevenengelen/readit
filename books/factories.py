import factory
from .models import Author, Book
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

class AuthorFactory(factory.django.DjangoModelFactory) :
    """
    Creates an author.
    """
    class Meta :
        model = Author
    # 'name' is the name of the provider that provides fake names.
    name = factory.Faker('name')
    
class UserFactory(factory.django.DjangoModelFactory) :
    """
    Creates a standard user.
    """
    class Meta :
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = first_name
    # make_password is a django build in function, it generates (hashes) a password for you.
    password = make_password('test')

class BookFactory(factory.django.DjangoModelFactory) :
    """
    Creates a book without a review.
    """
    class Meta :
        model = Book

    title = factory.Faker('word')

    @factory.post_generation
    def authors(self, create, extracted, **kwargs) :
        # the wrapper because we have a many to many relationship between Book and Author
        # if we're not using the create method, then do nothing
        # if we are, then we want to pass in each of the authors to this created factory
        # those authors are represented as extracted
        if not create :
            return
        if extracted :
            for authors in extracted :
                self.authors.add(authors)

class ReviewFactory(BookFactory) :
    """
    Creates a book with a review.
    """
    review = factory.faker('text', max_nb_chars = 400)
    date_reviewed = now()
    # a foreign key is much more easier than a many to many relationship
    # this means that any time we create a ReviewFactory, we will also create a subfactory UserFactory
    reviewed_by = factory.SubFactory(UserFactory)

