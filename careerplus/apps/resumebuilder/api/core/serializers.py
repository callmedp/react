# inter app imports
from resumebuilder.models import (Candidate, Skill, CandidateExperience, CandidateEducation, CandidateCertification,
                                  CandidateProject, CandidateReference, CandidateSocialLink, CandidateAchievement,
                                  CandidateLanguage)

# third party imports
from rest_framework import serializers


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = (
            'id', 'candidate_id', 'first_name', 'last_name', 'email', 'date_of_birth', 'number', 'gender', 'location',
            'extra_info', 'extracurricular', 'image')


class SkillSerializer(serializers.ModelSerializer):
    cc_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            return self.context['request'].user.id

        return self.instance.candidate.id

    def create(self, validated_data):
        validated_data.pop('cc_id', '')
        return super(SkillSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('cc_id', '')
        return super(SkillSerializer, self).update(instance, validated_data)

    class Meta:
        model = Skill
        fields = ('id', 'candidate_id', 'cc_id', 'name', 'proficiency')


class CandidateExperienceSerializer(serializers.ModelSerializer):
    cc_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            return self.context['request'].user.id

        return self.instance.candidate.id

    def create(self, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateExperienceSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateExperienceSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateExperience
        fields = (
            'id', 'candidate_id', 'cc_id', 'job_profile', 'company_name', 'start_date', 'end_date', 'is_working',
            'job_location', 'work_description')


class CandidateEducationSerializer(serializers.ModelSerializer):
    cc_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            return self.context['request'].user.id

        return self.instance.candidate.id

    def create(self, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateEducationSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateEducationSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateEducation
        fields = (
            'id', 'candidate_id', 'cc_id', 'specialization', 'institution_name', 'course_type', 'percentage_cgpa',
            'start_date',
            'end_date', 'is_pursuing')


class CandidateCertificationSerializer(serializers.ModelSerializer):
    cc_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            return self.context['request'].user.id

        return self.instance.candidate.id

    def create(self, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateCertificationSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateCertificationSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateCertification
        fields = ('id', 'candidate_id', 'cc_id', 'name_of_certification', 'year_of_certification')


class CandidateProjectSerializer(serializers.ModelSerializer):
    cc_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            return self.context['request'].user.id

        return self.instance.candidate.id

    def create(self, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateProjectSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateProjectSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateProject
        fields = ('id', 'candidate_id', 'cc_id', 'project_name', 'start_date', 'end_date', 'skills', 'description')


class CandidateReferenceSerializer(serializers.ModelSerializer):
    cc_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            return self.context['request'].user.id

        return self.instance.candidate.id

    def create(self, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateReferenceSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateReferenceSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateReference
        fields = ('id', 'candidate_id', 'cc_id', 'reference_name', 'about_candidate', 'reference_designation')


class CandidateSocialLinkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CandidateSocialLink
        fields = ('id', 'candidate', 'reference_name', 'about_candidate', 'reference_designation')


class CandidateLanguageSerializer(serializers.ModelSerializer):
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            return self.context['request'].user.id

        return self.instance.candidate.id

    def create(self, validated_data):
        return super(CandidateLanguageSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(CandidateLanguageSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateLanguage
        fields = ('id', 'candidate_id', 'proficiency', 'name')


class CandidateAchievementSerializer(serializers.ModelSerializer):
    cc_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        cc_id = self.initial_data.get('cc_id', '')
        if not cc_id:
            return candidate_id
        candidate = Candidate.objects.filter(candidate_id=cc_id).first()

        if not candidate:
            return candidate_id

        return candidate.id

    def create(self, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateAchievementSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('cc_id', '')
        return super(CandidateAchievementSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateAchievement
        fields = ('id', 'candidate_id', 'cc_id', 'title', 'date', 'summary')
