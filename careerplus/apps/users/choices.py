
WRITER_TYPE = (
    (0, 'Select Type'),
    (1, 'Starter'),
    (2, 'Runner'),
    (3, 'Expert'),
    (4, 'Veteran'),
)

# writer invoices variants

WRITING_STARTER_VALUE = 150

# starter is value calculation on WRITING_STARTER_VALUE
# runner, expert, and veteran value is given percentage of starter value
# matrix value is in percentages
RESUME_WRITING_MATRIX_DICT = {
    'FR': {
        1: 150, 2: 150,
        3: 180, 4: 200
    },
    'FP': {
        1: 250, 2: 200,
        3: 350, 4: 380},

    'SP': {
        1: 400, 2: 300,
        3: 450, 4: 500},

    'EP': {
        1: 600, 2: 400,
        3: 650, 4: 700
    },

    'DP': {
        1: 600, 2: 400,
        3: 650, 4: 700
    },
}


LINKEDIN_STARTER_VALUE = 300

# starter is value calculation on WRITING_STARTER_VALUE
# runner, expert, and veteran value is given percentage of starter value
# matrix value is in percentages
# 1 starter, 2 - runner, 3 - expert, 4 - veteran
LINKEDIN_WRITING_MATRIX_DICT = {
    'FR': {
        1: 350, 2: 300,
        3: 450, 4: 500},

    'FP': {
        1: 350, 2: 350,
        3: 450, 4: 500},

    'SP': {
        1: 500, 2: 400,
        3: 600, 4: 600},

    'EP': {
        1: 500, 2: 450,
        3: 600, 4: 700},

    'DP': {
        1: 500, 2: 450,
        3: 600, 4: 700},
}

INTERNATIONAL_RESUME_STARTER_VALUE = 225


# starter is value calculation on INTERNATIONAL_RESUME_STARTER_VALUE
# runner, expert, and veteran value is given percentage of starter value
# matrix value is in percentages
# 1 starter, 2 - runner, 3 - expert, 4 - veteran
INTERNATIONAL_RESUME_MATRIX_DICT = {
    'FR': {
        1: 250, 2: 100,
        3: 300, 4: 350},

    'FP': {
        1: 300, 2: 122,
        3: 400, 4: 450},

    'SP': {
        1: 400, 2: 166,
        3: 500, 4: 550},

    'EP': {
        1: 600, 2: 211,
        3: 700, 4: 750},

    'DP': {
        1: 600, 2: 211,
        3: 700, 4: 750},
}


VISUAL_RESUME_STARTER_VALUE = 225


# starter is value calculation on VISUAL_RESUME_STARTER_VALUE
# runner, expert, and veteran value is given percentage of starter value
# matrix value is in percentages
# 1 starter, 2 - runner, 3 - expert, 4 - veteran
VISUAL_RESUME_MATRIX_DICT = {
    'FR': {
        1: 250, 2: 100,
        3: 300, 4: 350},

    'FP': {
        1: 300, 2: 122,
        3: 400, 4: 450},

    'SP': {
        1: 400, 2: 166,
        3: 500, 4: 550},

    'EP': {
        1: 650, 2: 211,
        3: 700, 4: 750},

    'DP': {
        1: 650, 2: 211,
        3: 700, 4: 750},
}


PORTFOLIO_PRICE_MATRIX_DICT = {1: 700, 2: 700, 3:900, 4: 1000}

VISUAL_RESUME_MATRIX_DICT = {1: 75, 2: 75, 3: 80, 4: 85}

INTERNATIONAL_RESUME_MATRIX_DICT = {1: 75, 2: 75, 3: 80, 4: 85}

COUNTRY_SPCIFIC_VARIATION_MATRIX_DICT = {1: 75, 2: 75, 3: 80, 4: 85}

SECOND_REGULAR_RESUME_MATRIX_DICT = {1: 75, 2: 75, 3: 80, 4: 85}

EXECUTIVE_BIO_PRICE_MATRIX_DICT = {1: 500, 2: 500, 3: 600, 4: 750}

# 90% percentage
# 10 % penalty value
# 15% - 85%

# Addon Prices:
# EXPRESS = 50
# SUPER_EXPRESS = 125
EXPRESS = 75
SUPER_EXPRESS = 150

VISUAL_RESUME = 75
COVER_LETTER = 0
COUNTRY_SPCIFIC_VARIATION = 75
SECOND_REGULAR_RESUME = 75
INTERNATIONAL_RESUME = 75

# portfolio price
PORTFOLIO_PRICE = 1200


# combo discount
DISCOUNT_ALLOCATION_DAYS = 15
COMBO_DISCOUNT = 25  # in percentage
# COMBO_DISCOUNT_OF_TWO = 10  # in percentage
# COMBO_DISCOUNT_OF_THREE = 20  # in percentage

COMBO_DISCOUNT_OF_TWO = 5  # in percentage
COMBO_DISCOUNT_OF_THREE = 10  # in percentage


# SLA Incentive and Penalty Parameter

# REGULAR_SLA = 15
# EXPRESS_SLA = 12
# SUPER_EXPRESS_SLA = 10
REGULAR_SLA = 4
EXPRESS_SLA = 2
SUPER_EXPRESS_SLA = 1
PASS_PERCENTAGE = 85  # in percentage
INCENTIVE_PASS_PERCENTAGE = 95  # in percentage
PENALTY_PERCENTAGE = 10  # in percentage
INCENTIVE_PERCENTAGE = 10  # in percentage


MAX_INCENTIVE = 4000

# second regular 75 80 85
