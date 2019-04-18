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
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            user_id = self.context['request'].user.id
            candidate = Candidate.objects.filter(candidate_id=user_id).first()
            if candidate is None:
                raise serializers.ValidationError("User with given id does not exits.")
            return candidate.id
        return self.instance.candidate.id

    class Meta:
        model = Skill
        fields = ('id', 'candidate_id', 'name', 'proficiency', 'order')


class CandidateExperienceSerializer(serializers.ModelSerializer):
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            user_id = self.context['request'].user.id
            candidate = Candidate.objects.filter(candidate_id=user_id).first()
            if candidate is None:
                raise serializers.ValidationError("User with given id does not exits.")
            return candidate.id
        return self.instance.candidate.id

    def create(self, validated_data):
        return super(CandidateExperienceSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(CandidateExperienceSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateExperience
        fields = (
            'id', 'candidate_id', 'job_profile', 'company_name', 'start_date', 'end_date', 'is_working',
            'job_location', 'work_description', 'order')


class CandidateEducationSerializer(serializers.ModelSerializer):
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            user_id = self.context['request'].user.id
            candidate = Candidate.objects.filter(candidate_id=user_id).first()
            if candidate is None:
                raise serializers.ValidationError("User with given id does not exits.")
            return candidate.id
        return self.instance.candidate.id

    class Meta:
        model = CandidateEducation
        fields = (
            'id', 'candidate_id', 'specialization', 'institution_name', 'course_type', 'percentage_cgpa',
            'start_date',
            'end_date', 'is_pursuing', 'order')


class CandidateCertificationSerializer(serializers.ModelSerializer):
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            user_id = self.context['request'].user.id
            candidate = Candidate.objects.filter(candidate_id=user_id).first()
            if candidate is None:
                raise serializers.ValidationError("User with given id does not exits.")
            return candidate.id
        return self.instance.candidate.id

    def create(self, validated_data):
        return super(CandidateCertificationSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(CandidateCertificationSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateCertification
        fields = ('id', 'candidate_id', 'name_of_certification', 'year_of_certification', 'order')


class CandidateProjectSerializer(serializers.ModelSerializer):
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            user_id = self.context['request'].user.id
            candidate = Candidate.objects.filter(candidate_id=user_id).first()
            if candidate is None:
                raise serializers.ValidationError("User with given id does not exits.")
            return candidate.id
        return self.instance.candidate.id

    def create(self, validated_data):
        return super(CandidateProjectSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(CandidateProjectSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateProject
        fields = ('id', 'candidate_id', 'project_name', 'start_date', 'end_date', 'skills', 'description', 'order')


class CandidateReferenceSerializer(serializers.ModelSerializer):
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            user_id = self.context['request'].user.id
            candidate = Candidate.objects.filter(candidate_id=user_id).first()
            if candidate is None:
                raise serializers.ValidationError("User with given id does not exits.")
            return candidate.id
        return self.instance.candidate.id

    def create(self, validated_data):
        return super(CandidateReferenceSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(CandidateReferenceSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateReference
        fields = ('id', 'candidate_id', 'reference_name', 'about_candidate', 'reference_designation', 'order')


class CandidateSocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateSocialLink
        fields = ('id', 'candidate', 'reference_name', 'about_candidate', 'reference_designation')


class CandidateLanguageSerializer(serializers.ModelSerializer):
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            user_id = self.context['request'].user.id
            candidate = Candidate.objects.filter(candidate_id=user_id).first()
            if candidate is None:
                raise serializers.ValidationError("User with given id does not exits.")
            return candidate.id
        return self.instance.candidate.id

    def create(self, validated_data):
        return super(CandidateLanguageSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(CandidateLanguageSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateLanguage
        fields = ('id', 'candidate_id', 'proficiency', 'name', 'order')


class CandidateAchievementSerializer(serializers.ModelSerializer):
    candidate_id = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_candidate_id(self, candidate_id):
        if not self.instance:
            user_id = self.context['request'].user.id
            candidate = Candidate.objects.filter(candidate_id=user_id).first()
            if candidate is None:
                raise serializers.ValidationError("User with given id does not exits.")
            return candidate.id
        return self.instance.candidate.id

    def create(self, validated_data):
        return super(CandidateAchievementSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        return super(CandidateAchievementSerializer, self).update(instance, validated_data)

    class Meta:
        model = CandidateAchievement
        fields = ('id', 'candidate_id', 'title', 'date', 'summary', 'order')
