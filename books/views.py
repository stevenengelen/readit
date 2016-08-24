from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Book
from .models import Author
from django.views.generic import View, DetailView
from django.db.models import Count
from .forms import ReviewForm, BookForm
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView

# Create your views here.

def list_books(request) :
    """
    List the books that have reviews."
    """

    books = Book.objects.exclude(date_reviewed__isnull = True).prefetch_related('authors')

    context = { 'books' : books, }

    return render(request, "list.html", context)

class AuthorList(View) :
    def get(self, request) :
        authors = Author.objects.annotate(published_books = Count('books')).filter(published_books__gt = 0)
        context = { 'authors' : authors }
        return render(request, 'authors.html', context)

class BookDetail(DetailView) :
    model = Book
    template_name = 'book.html'

class AuthorDetail(DetailView) :
    model = Author
    template_name = 'author.html'


class ReviewList(View) :
    """
    List all of the books that we want to review.
    """
    def get(self, request) :
        books = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')
                      
        context = {
            'books': books,
            'form' : BookForm,
        }
                               
        return render(request, "list-to-review.html", context)

    def post(self, request) :
        form = BookForm(request.POST)
        book = Book.objects.filter(date_reviewed__isnull=True).prefetch_related('authors')

        if form.is_valid() :
            # we only need to call the save method on the form
            form.save()
            return redirect('review-books')

        context = {
                'book' : book,
                'form' : form,
                }

        return render(request, "list-to-review.html", context)

@login_required
def review_book(request, pk) :
    """
    Review an individual book
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST' :
        # If there is a POST in the request, we process the filled in form
        form = ReviewForm(request.POST)

        if form.is_valid() :
            # Here we write the data from our form in the model
            book.is_favourite = form.cleaned_data['is_favourite']
            print(form.cleaned_data['is_favourite'])
            book.review = form.cleaned_data['review']
            book.reviewed_by = request.user
            book.save()

            # We then redirect tot the review books page, since this review is done
            return redirect('review-books')
    # If there is no POST in the request, we just display the form, because it hasn't been filled in (yet)
    form = ReviewForm
                                         
    context = {
        'book': book,
        'form' : form,
    }
                                             
    return render(request, "review-book.html", context)

class CreateAuthor(CreateView) :
    # we inherit from CreateView, for a model based generic form
    # we need to define which model, which fields in this model, which template and to which url we are solving in case of succes
    model = Author
    fields = ['name',]
    template_name = "create-author.html"

    def get_success_url(self) :
        return reverse('review-books')

