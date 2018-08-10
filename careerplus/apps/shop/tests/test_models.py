from django.test import TestCase
from shop.models import Skill, ProductSkill


class SkillTestCase(TestCase):
    def setUp(self):
        self.skill, self.created = Skill.objects.get_or_create(
            name='Django', active=True)

    def test_skill_creation(self):
        skill = self.skill
        self.assertTrue(isinstance(skill, Skill))
        self.assertEqual(
            skill.__str__(), skill.name + ' - ' + str(skill.id))