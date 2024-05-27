from django.db import models
from django.urls import reverse


# Create your models here.
class Genre(models.Model):
    """Model representing a book genre."""

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a book genre (e.g. Science Fiction, French Poetry, etc.)",
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("genre-detail", args=[str(self.id)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower("name"),
                name="genre_name_case_insensitive_unique",
                violation_error_message="Genre already exists (case insensitive match)",
            )
        ]


class Language(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                models.functions.Lower("name"),
                name="language_name_case_insensitive_unique",
                violation_error_message="Language already exists (case insensitive match)",
            )
        ]

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.RESTRICT, null=True)
    summary = models.CharField(max_length=1000)
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        unique=True,
        help_text='13 character  <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
    )
    genres = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    language = models.ForeignKey(Language, on_delete=models.RESTRICT, null=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])


class BookInstance(models.Model):
    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On Loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    due_back = models.DateField(null=True, blank=True)
    status = models.CharField(
        choices=LOAN_STATUS,
        max_length=1,
        blank=True,
        default="m",
        help_text="Book Availability",
    )
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)

    class Meta:
        ordering = ["due_back"]

    def __str__(self) -> str:
        return f"{self.id} ({self.book.title})"


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
