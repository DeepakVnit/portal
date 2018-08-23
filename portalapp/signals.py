from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile
from .models import User, Basic, Experience, Education, Skill, Project


@receiver(post_save, sender=User)
def create_related_profile(sender, instance, created, *args, **kwargs):
    # Notice that we're checking for `created` here. We only want to do this
    # the first time the `User` instance is created. If the save that caused
    # this signal to be run was an update action, we know the user already
    # has a profile.
    if instance and created:
        instance.profile = Profile.objects.create(user=instance)
        instance.profile.userprofilebasicInfo = Basic.objects.create(profile=instance.profile)
        instance.profile.Experience = Experience.objects.create(profile=instance.profile)
        instance.profile.Education = Education.objects.create(profile=instance.profile)
        instance.profile.Skills = Skill.objects.create(profile=instance.profile)
        instance.profile.projects = Project.objects.create(profile=instance.profile)
