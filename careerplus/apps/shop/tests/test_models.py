
# third party imports

# django imports
from django.test import TestCase

# internal imports
from shop.models import Skill, ProductSkill
from shared.tests.factory.shared_factories import (
    SkillFactory, ProductFactory)


class SkillTestCase(TestCase):
    def setUp(self):
        self.skill, self.created = Skill.objects.get_or_create(
            name='Django', active=True)

    def test_skill_creation(self):
        skill = self.skill
        self.assertTrue(isinstance(skill, Skill))
        self.assertEqual(
            skill.__str__(), skill.name + ' - ' + str(skill.id))

    def test_delete(self):
        self.skill.delete()


class ProductSkillTestCase(TestCase):
    def setUp(self):
        self.skill = SkillFactory()
        self.product = ProductFactory(id=1, type_flow=2)

    def create_prdskill(self):
        return ProductSkill.objects.get_or_create(
            skill=self.skill, product=self.product,
            active=True)

    def test_prductskill_creation(self):
        pd_skill, created = self.create_prdskill()
        self.assertTrue(isinstance(pd_skill, ProductSkill))
