from django.contrib import admin
from .models import Badge, BadgeCriterion, UserBadge, LeaderboardEntry, GamificationPoint


class BadgeCriterionInline(admin.TabularInline):
    model = BadgeCriterion
    extra = 1


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "criteria_summary")
    inlines = [BadgeCriterionInline]

    def criteria_summary(self, obj):
        return " AND ".join(f"{c.field} {c.operator} {c.value}" for c in obj.criteria.all())
    criteria_summary.short_description = "Criteria"


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ("profile", "badge", "earned_at", "badge_criteria")
    search_fields = ("profile__user__username", "badge__title")
    list_filter = ("earned_at", "badge")

    def badge_criteria(self, obj):
        return ", ".join(
            f"{c.field} {c.operator} {c.value}" for c in obj.badge.criteria.all()
        )
    badge_criteria.short_description = "Award Criteria"


@admin.register(GamificationPoint)
class GamificationPointAdmin(admin.ModelAdmin):
    list_display = ("profile", "points", "reason", "created_at")
    list_filter = ("created_at",)
    search_fields = ("profile__user__username", "reason")


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ("profile", "total_score")
    ordering = ("-total_score",)
