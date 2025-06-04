from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import QuizResult
from gamification.services import award_points_and_check_badges

@receiver(post_save, sender=QuizResult)
def handle_quiz_completion(sender, instance, created, **kwargs):
    if created:
        profile = instance.user.profile
        award_points_and_check_badges(profile, points=10, reason="Completed a quiz")
