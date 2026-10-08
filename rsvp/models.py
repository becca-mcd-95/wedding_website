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

    def __str__(self):
        return self.name

class Guest(models.Model):
    household = models.ForeignKey(Household, on_delete=models.CASCADE, related_name="guests")
    first_name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    needs_own_rsvp = models.BooleanField(default=True)
    class Status(models.TextChoices):
        YES = "Y", "Yes"
        NO = "N", "No"
        NOT_REPLIED = "TBC", "Not yet replied"

    reply_status = models.CharField(
        max_length=3,
        choices=Status,  
        default=Status.NOT_REPLIED
    )

    def __str__(self):
        return f"{self.first_name} {self.surname}"