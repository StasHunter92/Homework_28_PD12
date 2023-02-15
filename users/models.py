from django.db import models


# ----------------------------------------------------------------------------------------------------------------------
# Create location model
class Location(models.Model):
    name: str = models.CharField(max_length=100)
    lat: float = models.FloatField(max_length=20)
    lng: float = models.FloatField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name: str = "Локация"
        verbose_name_plural: str = "Локации"


# ----------------------------------------------------------------------------------------------------------------------
# Create user model
class User(models.Model):
    ROLE: list[tuple] = [("member", "Участник"), ("moderator", "Модератор"), ("admin", "Администратор")]

    first_name: str = models.CharField(max_length=20)
    last_name: str = models.CharField(max_length=20)
    username: str = models.CharField(max_length=20)
    password: str = models.CharField(max_length=20)
    role: str = models.CharField(max_length=20, choices=ROLE, default="member")
    age: int = models.PositiveIntegerField()
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name: str = "Пользователь"
        verbose_name_plural: str = "Пользователи"
