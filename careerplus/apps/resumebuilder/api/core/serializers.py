# inter app imports
from resumebuilder.models import (Candidate, Skill, CandidateExperience, CandidateEducation, CandidateCertification,
                                  CandidateProject, CandidateReference, CandidateSocialLink, CandidateAchievement)

# third party imports
from rest_framework import serializers


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = (
            'id', 'candidate_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'number', 'gender', 'location',
            'extra_info',
            'image')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'candidate', 'name', 'proficiency')


class CandidateExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateExperience
        fields = ('id', 'candidate', 'job_profile', 'company_name', 'start_date', 'end_date', 'is_working', 'job_location',
                  'work_description')


class CandidateEducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateEducation
        fields = ('id', 'candidate', 'specialization', 'institution_name', 'course_type', 'percentage_cgpa', 'start_date',
                  'end_date', 'is_pursuing')


class CandidateCertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateCertification
        fields = ('id', 'candidate', 'name_of_certification', 'year_of_certification')


class CandidateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateProject
        fields = ('id', 'candidate', 'project_name', 'start_date', 'end_date', 'skills')


class CandidateReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateReference
        fields = ('id', 'candidate', 'reference_name', 'about_candidate', 'reference_designation')


class CandidateSocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateSocialLink
        fields = ('id', 'candidate', 'reference_name', 'about_candidate', 'reference_designation')


class CandidateAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateAchievement
        fields = ('id', 'candidate', 'title', 'date', 'summary')
