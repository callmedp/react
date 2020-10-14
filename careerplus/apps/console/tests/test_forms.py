from django.test import TestCase, Client
from django.forms.models import inlineformset_factory

from geolocation.models import Country
from shop.models import (
    Product, ProductSkill, Skill)
from console.shop_form import (
    SkillAddForm, SkillChangeForm,
    ProductSkillForm, SkillInlineFormSet)
from shared.tests.factory.shared_factories import (
    SkillFactory, ProductFactory)


class TestConsoleSkillForm(TestCase):

    def setUp(self):
        self.client = Client()
        Country.objects.get_or_create(phone='91', name='India')
        self.valid_data = {'name': 'AddSkill', 'active': True}
        self.invalid_data = {'name': ''}
        self.skill = SkillFactory()
        self.product = ProductFactory(type_flow=2)
        self.ProductSkillFormSet = inlineformset_factory(
            Product, ProductSkill, fk_name='product',
            form=ProductSkillForm,
            can_delete=True,
            formset=SkillInlineFormSet, extra=0)
        self.inline_data = {
            'productskills-TOTAL_FORMS': 1,
            'productskills-INITIAL_FORMS': 0,
            'productskills-MIN_NUM_FORMS': 0,
            'productskills-MAX_NUM_FORMS': 15,
            'productskills-0-skill': self.skill.id,
            'productskills-0-active': True,
            'productskills-0-priority': 1
        }

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

    def test_product_skill_formset_valid(self):
        formset = self.ProductSkillFormSet(
            self.inline_data, instance=self.product,
            form_kwargs={'object': self.product},)

        self.assertEqual(formset.is_valid(), True)

    def test_product_skill_formset_invalid(self):
        self.inline_data['productskills-0-priority'] = ''
        formset = self.ProductSkillFormSet(
            self.inline_data, instance=self.product,
            form_kwargs={'object': self.product},)
        self.assertEqual(formset.is_valid(), False)

        self.inline_data['productskills-0-skill'] = int(Skill.objects.all().order_by('id').last().pk) + 1
        self.inline_data['productskills-0-priority'] = 1
        formset = self.ProductSkillFormSet(
            self.inline_data, instance=self.product,
            form_kwargs={'object': self.product},)
        self.assertFalse(formset.is_valid())