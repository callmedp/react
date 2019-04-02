# inter app imports
from resumebuilder.models import (User, Skill, UserExperience, UserEducation, UserCertification,
                                  UserProject, UserReference, UserSocialLink, UserAchievement)

# third party imports
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'candidate_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'number', 'gender', 'location',
            'extra_info',
            'image')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'user', 'name', 'proficiency')


class UserExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExperience
        fields = ('id', 'user', 'job_profile', 'company_name', 'start_date', 'end_date', 'is_working', 'job_location',
                  'work_description')


class UserEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEducation
        fields = ('id', 'user', 'specialization', 'institution_name', 'course_type', 'percentage_cgpa', 'start_date',
                  'end_date', 'is_pursuing')


class UserCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCertification
        fields = ('id', 'user', 'name_of_certification', 'year_of_certification')


class UserProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = ('id', 'user', 'project_name', 'start_date', 'end_date', 'skills')


class UserReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReference
        fields = ('id', 'user', 'reference_name', 'about_user', 'reference_designation')


class UserSocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSocialLink
        fields = ('id', 'user', 'reference_name', 'about_user', 'reference_designation')


class UserAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAchievement
        fields = ('id', 'user', 'title', 'date', 'summary')
