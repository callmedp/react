# inbuild python imports
from decimal import Decimal
import datetime
from django.utils.text import slugify

# third party imports
import factory

# inter-app imports
from geolocation.models import Country
from shop.models import Product, ProductClass, Category, CategoryRelationship
from order.models import Order, OrderItem
# local imports


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

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


class CategoryRelationshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CategoryRelationship

    related_from = factory.SubFactory(CategoryFactory)
    related_to = factory.SubFactory(CategoryFactory)


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
    type_flow = 1
    type_product = 0
    upc = '74836'
    url = ''
    usd_price = Decimal('0.00')
    vendor_id = 3
    video_url = ''
    visibility = True
    product_class = factory.SubFactory(ProductClassFactory)


class ProductCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    category = factory.SubFactory(CategoryFactory)
    product = factory.SubFactory(ProductFactory)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    orderitem = factory.RelatedFactory(OrderItemFactory, 'order')

    address = 'afddress'
    alt_email = 'ritesh.bisht93@gmail.com'
    alt_mobile = '9958680578'
    archive_json = ''
    assigned_to_id = None
    candidate_id = '5ad08b049ba566523d4fa48a'
    closed_on = None
    co_id = None
    conv_charge = Decimal('0.00'),
    country_code = '91'
    country_id = 1,
    created = datetime.datetime(year=2018, month=2, day=12)
    crm_lead_id = None
    crm_sales_id = None
    currency = 0,
    date_placed = datetime.datetime(year=2018, month=2, day=12)
    email = 'ritesh.bisht93@gmail.com'
    first_name = 'ritesh'
    id = 235709,
    invoice = ''
    last_name = 'bisht'
    midout_sent_on = None
    mobile = '9958680578'
    modified = datetime.datetime(year=2018, month=2, day=12)
    number = 'CP235709'
    paid_by_id = 18,
    payment_date = datetime.datetime(year=2018, month=2, day=12)
    pincode = '110085'
    sales_user_info = ''
    site = 0,
    state = 'Delhi'
    status = 1,
    tax_config = '{"sgst" = 9.0, "igst" = 0, "cgst" = 9.0}'
    total_excl_tax = Decimal('6400.00'),
    total_incl_tax = Decimal('7552.00'),
    wc_cat = 21,
    wc_follow_up = None
    wc_status = 41,
    wc_sub_cat = 41,
    welcome_call_done = True



