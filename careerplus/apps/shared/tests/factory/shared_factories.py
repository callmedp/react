# inbuild python imports
from decimal import Decimal
import datetime
from django.utils.text import slugify

# third party imports
import factory
from django.contrib.auth.models import Group
from django.db.models.signals import post_save

# inter-app imports
from geolocation.models import Country
from shop.models import (
    Product, ProductClass, Category, ProductCategory,
    CategoryRelationship, ProductAuditHistory, Skill,
    ProductSkill, ProductCategory, Faculty)
from shop.choices import FACULTY_TEACHER
from order.models import Order, OrderItem
from users.models import User, UserProfile
from partner.models import Vendor
# local imports


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)
    id = 1
    type_level = 3
    name = factory.LazyAttributeSequence(lambda o, n: "test_category_level_%d" % o.type_level)
    active = True
    banner = ''
    career_outcomes = 'First outcome, second outcome'
    created = datetime.datetime.now()
    display_order = 1
    graph_image = ''
    heading = ''
    icon = ''
    image = ''
    image_alt = ''
    is_skill = False
    meta_desc = ''
    meta_keywords = ''
    modified = datetime.datetime.now()
    slug = slugify(name)
    title = ''
    url = ''
    video_link = ''
    description = factory.LazyAttributeSequence(
        lambda o, n: 'this category is of  level %d' % (o.type_level)
    )


class CategoryRelationShipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryRelationship
        django_get_or_create = ('related_from',)

    related_from = factory.SubFactory(CategoryFactory)
    related_to = factory.SubFactory(CategoryFactory)
    active = True


class CategoryRelationShipWithCategoryLevel1Factory(CategoryFactory):
    relation_bewteen_category = factory.RelatedFactory(CategoryRelationShipFactory,  'related_from', related_to__type_level=1, related_to__active=True)


class CountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country
        django_get_or_create = ('name', )

    name = 'India'
    code2 = 'IN'
    phone = '91'


class ProductClassFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductClass
        django_get_or_create = ('name', 'slug')

    name = 'course'
    slug = 'course'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('email', )

    name = 'ritesh'
    email = 'ritesh.bisht93@gmail.com'
    password = factory.PostGenerationMethodCall('set_password', '12345')


class VendorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Vendor
        django_get_or_create = ('name', 'cp_id', 'slug')

    name = 'careerplus'
    slug = 'careerplus'
    cp_id = 1234


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ('id', )

    about = '<p>Teest</p>'
    active = True
    aed_price = Decimal('0.00')
    archive_json = ''
    attend = ''
    avg_rating = Decimal('2.50')
    banner = ''
    buy_count = 0
    buy_shine = '<p>Test</p>'
    call_desc = ''
    cp_id = None
    cp_page_view = 0
    cpv_id = None
    created = datetime.datetime(year=2018, month=2, day=12)
    description = '<p>Test</p>'
    email_cc = ''
    fake_aed_price = Decimal('0.00')
    fake_gbp_price = Decimal('0.00')
    fake_inr_price = Decimal('0.00')
    fake_usd_price = Decimal('0.00')
    fixed_slug = False
    gbp_price = Decimal('0.00')
    heading = 'Test product_Priya'
    icon = 'product_icon/2678/1518609833_9180.jpg'
    image = 'product_image/2678/1518609833_8215.jpg'
    image_alt = 'Test product_Priya'
    image_bg = 0
    id = 2678
    inr_price = Decimal('3400.00')
    is_indexable = True
    mail_desc = ''
    meta_desc = 'Online Test Priya Services for 1-4 years. Get expert advice & tips for Test Priya at Shine Learning.'
    meta_keywords = ''
    modified = datetime.datetime(year=2018, month=2, day=12)
    name = 'Test product_Priya'
    no_review = 0
    num_jobs = 0
    prg_structure = ''
    search_keywords = ''
    slug = 'test-product_priya'
    title = 'Test Product priya'
    Ttype_flow = 1
    type_product = 0
    upc = '74836'
    url = ''
    usd_price = Decimal('0.00')
    vendor = factory.SubFactory(VendorFactory)
    video_url = ''
    visibility = True
    product_class = factory.SubFactory(ProductClassFactory)


class ProductCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductCategory
        django_get_or_create = ('product',)

    category = factory.SubFactory(CategoryFactory, type_level=2)
    product = factory.SubFactory(ProductFactory)


class ProductWithCategoryLevel2Factory(ProductFactory):
    relation = factory.RelatedFactory(ProductCategoryFactory, 'product', category__type_level=2)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
        django_get_or_create = ('id', )

    address = 'address'
    alt_email = 'ritesh.bisht93@gmail.com'
    alt_mobile = '9958680578'
    archive_json = ''
    assigned_to_id = None
    candidate_id = '5ad08b049ba566523d4fa48a'
    closed_on = None
    co_id = 123
    conv_charge = Decimal('0.00')
    country_code = '91'
    country_id = 1
    created = datetime.datetime(year=2018, month=2, day=12)
    crm_lead_id = None
    crm_sales_id = None
    currency = 0
    date_placed = datetime.datetime(year=2018, month=2, day=12)
    email = 'ritesh.bisht93@gmail.com'
    first_name = 'ritesh'
    id = 235711
    invoice = ''
    last_name = 'bisht'
    midout_sent_on = None
    mobile = '9958680578'
    modified = datetime.datetime(year=2018, month=2, day=12)
    number = 'CP235709'
    paid_by_id = None
    payment_date = datetime.datetime(year=2018, month=2, day=12)
    pincode = '110085'
    sales_user_info = ''
    site = 0
    state = 'Delhi'
    status = 1
    tax_config = '{"sgst" = 9.0, "igst" = 0, "cgst" = 9.0}'
    total_excl_tax = Decimal('6400.00')
    total_incl_tax = Decimal('7552.00')
    wc_cat = 21
    wc_follow_up = None
    wc_status = 41
    wc_sub_cat = 41
    welcome_call_done = True


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem
        django_get_or_create = ('id',)

    order = factory.SubFactory(OrderFactory)
    archive_json = ''
    assigned_by_id = None
    assigned_date = None
    assigned_to_id = None
    buy_count_updated = False
    closed_on = None
    coi_id = None
    cost_price = Decimal('3000.00')
    created = datetime.datetime(year=2018, month=2, day=12)
    delivery_price_excl_tax = Decimal('0.00')
    delivery_price_incl_tax = Decimal('0.00')
    delivery_service_id = None
    discount_amount = Decimal('0.00')
    draft_added_on = datetime.datetime(year=2018, month=2, day=12)
    draft_counter = 1
    expiry_date = None
    id = 486039
    is_addon = False
    is_combo = False
    is_variation = False
    last_oi_status = 5
    modified = datetime.datetime(year=2018, month=2, day=12)
    no_process = False
    oi_draft = '235709/draftupload_235709_486039_7309_20180803.docx'
    oi_flow_status = 0
    oi_price_before_discounts_excl_tax = Decimal('0.00')
    oi_price_before_discounts_incl_tax = Decimal('0.00')
    oi_resume = ''
    oi_status = 5
    oio_linkedin_id = None
    parent_id = None
    partner_id = 1
    partner_name = ''
    # product = factory.SubFactory(ProductFactory)
    quantity = 1
    selling_price = Decimal('3540.00')
    tat_date = None
    tax_amount = Decimal('540.00')
    title = 'Resume Booster'
    upc = '235709_486038'
    user_feedback = False
    waiting_for_input = False
    wc_cat = 21
    wc_follow_up = None
    wc_status = 41
    wc_sub_cat = 41


class GroupFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Group
        django_get_or_create = ('name',)


class ProductAuditHistoryFactory(factory.mongoengine.MongoEngineFactory):

    class Meta:
        model = ProductAuditHistory


class SkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Skill
        django_get_or_create = ('name', )

    name = 'Django'
    active = True


class ProductSkillFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductSkill
        django_get_or_create = ('skill', 'product')

    skill = factory.SubFactory(SkillFactory)
    product = factory.SubFactory(ProductFactory)
    priority = 1
    active = True

class ProductWithSkillFactory(ProductFactory):
    membership = factory.RelatedFactory(
        ProductSkillFactory, 'product')

class ProductWith4SkillsFactory(ProductFactory):
    membership1 = factory.RelatedFactory(
        ProductSkillFactory, 'product', skill__name='Python')
    membership2 = factory.RelatedFactory(
        ProductSkillFactory, 'product', skill__name='Django')
    membership3 = factory.RelatedFactory(
        ProductSkillFactory, 'product', skill__name='Html')
    membership4 = factory.RelatedFactory(
        ProductSkillFactory, 'product', skill__name='Css')


class AdminFactory(UserFactory):
    is_superuser = True
    email = 'root@root.com'


@factory.django.mute_signals(post_save)
class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile
        django_get_or_create = ('user', )

    user = factory.SubFactory(
        'shared.tests.factory.shared_factories.WriterFactory',
        userprofile=None)
    writer_type = 1
    pan_no = "pan_no"
    gstin = "gstin"
    address = "Gurgaon"
    po_number = "98765"
    valid_from = datetime.datetime.today() - datetime.timedelta(
        days=100)
    valid_to = datetime.datetime.today() + datetime.timedelta(
        days=100)


@factory.django.mute_signals(post_save)
class WriterFactory(UserFactory):
    email = 'writer1@gmail.com'
    userprofile = factory.RelatedFactory(
        UserProfileFactory, 'user')


class UniversityCategoryFactory(CategoryFactory):
    active = True
    is_university = True
    is_service = False
    is_skill = False
    type_level = 3


class FacultyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Faculty
        django_get_or_create = ('name', )
    name = "Faculty"
    role = FACULTY_TEACHER
    image = ''
    designation = 'Asst Professor'
    description = 'test description'
    short_desc = 'test short description'
    faculty_speak = 'test faculty speak'
    institute = factory.SubFactory(UniversityCategoryFactory)
    active = True
