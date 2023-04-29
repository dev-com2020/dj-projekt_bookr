from django.contrib import auth
from django.db import models


# Create your models here.

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    website = models.URLField(help_text="Publisher's website")
    email = models.EmailField(help_text="Publisher's email address")

    def __str__(self):
        return self.name


class Book(models.Model):
    """Opublikowana książka."""
    title = models.CharField(max_length=70,
                             help_text="Tytuł książki.")
    publication_date = models.DateField(
        verbose_name="Data publikacji książki.")
    isbn = models.CharField(max_length=20,
                            verbose_name="Numer ISBN książki.")
    publisher = models.ForeignKey(Publisher,
                                  on_delete=models.CASCADE)
    contributors = models.ManyToManyField('Contributor',
                                          through="BookContributor")

    def __str__(self):
        return "{} ({})".format(self.title, self.isbn)


class Contributor(models.Model):
    """Współtwórca książki, np. autor, redaktor, współautor."""
    first_names = models.CharField(max_length=50,
                                   help_text="Imię lub imiona współtwórcy.")
    last_names = models.CharField(max_length=50,
                                  help_text="Nazwisko lub nawiska współtwórcy.")
    email = models.EmailField(help_text="E-mail współtwórcy.")

    def __str__(self):
        return self.first_names


class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(verbose_name="Rola, jaką współtwórca odegrał podczas tworzenia tej książki.",
                            choices=ContributionRole.choices, max_length=20)


class Review(models.Model):
    content = models.TextField(help_text="Tekst recenzji.")
    rating = models.IntegerField(help_text="Ocena użytkownika.")
    date_created = models.DateTimeField(auto_now_add=True,
                                        help_text="Data i czas utworzenia recenzji.")
    date_edited = models.DateTimeField(null=True,
                                       help_text="Data i czas ostatniej edycji recenzji.")
    creator = models.ForeignKey(auth.get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             help_text="Recenzowana książka.")
