from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class GamificationPoint(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='points')
    reason = models.CharField(max_length=255)
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.profile.username} +{self.points} for {self.reason}"

class LeaderboardEntry(models.Model):
    profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.profile.username} - {self.total_score} pts"


from django.db import models

class Badge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to="badges/", blank=True, null=True)

    def __str__(self):
        return self.title


class BadgeCriterion(models.Model):
    FIELD_CHOICES = [
        ("total_score", "Total Score"),
        ("quizzes_completed", "Quizzes Completed"),
        # Add more as needed
    ]
    OPERATOR_CHOICES = [
        (">", ">"),
        (">=", "≥"),
        ("==", "="),
        ("<", "<"),
        ("<=", "≤"),
    ]

    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="criteria")
    field = models.CharField(max_length=50, choices=FIELD_CHOICES)
    operator = models.CharField(max_length=5, choices=OPERATOR_CHOICES)
    value = models.IntegerField()

    def __str__(self):
        return f"{self.field} {self.operator} {self.value}"


class UserBadge(models.Model):
    profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('profile', 'badge')

    def __str__(self):
        return f"{self.profile.user.username} earned {self.badge.title}"
