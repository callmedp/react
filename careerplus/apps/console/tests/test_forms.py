from django.test import TestCase, Client

from geolocation.models import Country
from console.shop_form import SkillAddForm, SkillChangeForm
from shared.tests.factory.shared_factories import (
    SkillFactory)


class TestConsoleSkillForm(TestCase):

    def setUp(self):
        self.client = Client()
        Country.objects.get_or_create(phone='91', name='India')
        self.valid_data = {'name': 'AddSkill', 'active': True}
        self.invalid_data = {'name': ''}
        self.skill = SkillFactory()

    def test_skill_valid_form(self):
        form = SkillAddForm(self.valid_data)
        self.assertTrue(form.is_valid())
        form = SkillChangeForm(
            {'name': self.skill.name, 'active': True},
            instance=self.skill)
        self.assertTrue(form.is_valid())

    def test_skill_invalid_form(self):
        form = SkillAddForm(self.invalid_data)
        self.assertFalse(form.is_valid())
        form = SkillAddForm({'name': self.skill.name})
        self.assertFalse(form.is_valid())

        form = SkillChangeForm(
            {'name': '', 'active': True},
            instance=self.skill)
        self.assertFalse(form.is_valid())
