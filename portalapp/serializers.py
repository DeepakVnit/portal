from rest_framework import serializers

from .models import User
from .models import Profile, Basic, Experience, Education, Skill, Project
from django.contrib.auth import authenticate


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='profile.user.username')
    class Meta:
        model = Project
        fields = ('username', 'headline', 'description', 'from_date', 'to_date', 'ptype', 'extra_info')

class BasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basic
        fields = ('dob', 'phone', 'city', 'state', 'country', 'interest', 'website',)


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ('designation', 'company', 'start_date', 'end_date', )


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ('education_level', 'branch', 'institute', 'start_date', 'end_date',)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('skill', 'last_used',)


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField()
    basic = BasicSerializer(read_only=True)
    experience = ExperienceSerializer(source='experience_set', many=True, default=[])
    education = EducationSerializer(source='education_set', many=True, default=[])
    skills = SkillSerializer(source='skill_set', many=True, default=[])
    projects = ProjectSerializer(source='project_set', many=True, default=[])

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image','basic', 'experience', 'education', 'skills', 'projects')
        read_only_fields = ('username',)

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return 'https://static.productionready.io/images/smiley-cyrus.jpg' #TODO


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    profile = ProfileSerializer(write_only=True)
    bio = serializers.CharField(source='profile.bio', read_only=True)
    image = serializers.SerializerMethodField(source='mystatic/None/1.jpg')

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token', 'profile', 'bio', 'image')
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        for (key, value) in profile_data.items():
            setattr(instance.profile, key, value)

        instance.profile.save()

        return instance
