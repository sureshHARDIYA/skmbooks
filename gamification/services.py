from django.db.models import Sum
from .models import GamificationPoint, Badge, UserBadge, LeaderboardEntry
import operator

OPERATOR_MAP = {
    ">=": operator.ge,
    "<=": operator.le,
    "==": operator.eq,
    ">": operator.gt,
    "<": operator.lt,
}

def award_points_and_check_badges(profile, points, reason):
    # 1. Add GamificationPoint log
    GamificationPoint.objects.create(profile=profile, points=points, reason=reason)
    # 2. Update profile score
    profile.total_score += points
    profile.save()

    # 3. Update leaderboard total
    leaderboard, _ = LeaderboardEntry.objects.get_or_create(profile=profile)
    leaderboard.total_points += points
    leaderboard.save()

    # 3. Check and award badges
    check_and_award_badges(profile)


def check_and_award_badges(profile):
    context = {
        "total_score": profile.total_score,
        "quizzes_completed": profile.quizzes_completed,
    }

    earned_badge_ids = UserBadge.objects.filter(profile=profile).values_list('badge_id', flat=True)

    for badge in Badge.objects.exclude(id__in=earned_badge_ids).prefetch_related("criteria"):
        passed = True
        for criterion in badge.criteria.all():
            profile_value = context.get(criterion.field)
            compare_fn = OPERATOR_MAP.get(criterion.operator)
            if profile_value is None or compare_fn is None or not compare_fn(profile_value, criterion.value):
                passed = False
                break
        if passed:
            UserBadge.objects.create(profile=profile, badge=badge) # Add more badge conditions here
