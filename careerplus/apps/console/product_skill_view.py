from django.views.generic import (DetailView, View, TemplateView, )

from shop.models import (ProductSkill, Skill)

from users.mixins import UserGroupMixin


class ProductSkillAddView(UserGroupMixin, TemplateView):
    group_names = ['FINANCE', 'PRODUCT']
    model = Skill
    template_name = 'console/shop/product_skill.html'
