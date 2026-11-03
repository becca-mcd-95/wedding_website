from django.db import models

# Create your models here.

class Household(models.Model):
    name = models.CharField(max_length=60)
    class InviteType(models.TextChoices):
        ALL_DAY = "AD", "All day"
        EVENING = "EV", "Evening"

    invite_type = models.CharField(
        max_length=2,
        choices=InviteType,
    )

    comments = models.TextField(blank=True, max_length=500)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class DietaryRequirement(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Guest(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="guests")
    first_name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    needs_own_rsvp = models.BooleanField(default=True)
    diets = models.ManyToManyField(DietaryRequirement, blank=True)
    dietary_notes = models.TextField(blank=True, max_length=300)
    needs_accommodation = models.BooleanField(default=False)

    class Status(models.TextChoices):
        YES = "Y", "Yes"
        NO = "N", "No"
        NOT_REPLIED = "TBC", "Not yet replied"

    reply_status = models.CharField(
        max_length=3,
        choices=Status,  
        default=Status.NOT_REPLIED
    )

    class Coach(models.TextChoices):
        NO = "N", "Not required"
        DOWN = "D", "Just to the reception"
        UP = "U", "Just returning from reception"
        BOTH = "B", "Both ways"

    coach = models.CharField(
        max_length=1,
        choices=Coach,
        default=Coach.NO
    )

    def __str__(self):
        return f"{self.first_name} {self.surname}"