from django.db import models
from django.conf import settings


class Community(models.Model):
    name = models.CharField(max_length=120)
    tagline = models.CharField(max_length=160, blank=True)
    description = models.CharField(max_length=180)
    about = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    contact_email = models.EmailField(blank=True)
    website_url = models.URLField(blank=True)
    verified = models.BooleanField(default=False)
    funded_recently = models.BooleanField(default=False)
    sponsors_count = models.PositiveIntegerField(default=0)
    last_active = models.DateTimeField(null=True, blank=True)
    logo_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["location"]),
        ]

    def __str__(self) -> str:
        return self.name


class Sponsor(models.Model):
    name = models.CharField(max_length=120)
    logo_url = models.URLField(blank=True)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.name


class Sponsorship(models.Model):
    CONTRIBUTION_CHOICES = [
        ("cash", "Cash"),
        ("kind", "In-Kind"),
        ("grant", "Grant"),
    ]
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="sponsorships")
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name="sponsorships")
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    contribution_type = models.CharField(max_length=16, choices=CONTRIBUTION_CHOICES, default="cash")
    date = models.DateField()

    def __str__(self) -> str:
        return f"{self.sponsor} → {self.community} ({self.amount})"


class Event(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=160)
    date = models.DateField()
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.title} ({self.date})"


class CommunityLeader(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='leaders')

    class Meta:
        unique_together = ("user", "community")

    def __str__(self) -> str:
        return f"{self.user} → {self.community}"
