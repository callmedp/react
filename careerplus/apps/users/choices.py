
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
        1: 200, 2: 200,
        3: 250, 4: 300},

    'SP': {
        1: 300, 2: 300,
        3: 350, 4: 400},

    'EP': {
        1: 400, 2: 400,
        3: 450, 4: 500
    },

    'DP': {
        1: 400, 2: 400,
        3: 450, 4: 500
    },
}


LINKEDIN_STARTER_VALUE = 300

# starter is value calculation on WRITING_STARTER_VALUE
# runner, expert, and veteran value is given percentage of starter value
# matrix value is in percentages
# 1 starter, 2 - runner, 3 - expert, 4 - veteran
LINKEDIN_WRITING_MATRIX_DICT = {
    'FR': {
        1: 300, 2: 300,
        3: 400, 4: 400},

    'FP': {
        1: 350, 2: 350,
        3: 450, 4: 450},

    'SP': {
        1: 400, 2: 400,
        3: 450, 4: 500},

    'EP': {
        1: 450, 2: 450,
        3: 500, 4: 550},

    'DP': {
        1: 450, 2: 450,
        3: 500, 4: 550},
}

INTERNATIONAL_RESUME_STARTER_VALUE = 225


# starter is value calculation on INTERNATIONAL_RESUME_STARTER_VALUE
# runner, expert, and veteran value is given percentage of starter value
# matrix value is in percentages
# 1 starter, 2 - runner, 3 - expert, 4 - veteran
INTERNATIONAL_RESUME_MATRIX_DICT = {
    'FR': {
        1: 100, 2: 100,
        3: 115, 4: 126},

    'FP': {
        1: 122, 2: 122,
        3: 146, 4: 171},

    'SP': {
        1: 166, 2: 166,
        3: 191, 4: 215},

    'EP': {
        1: 211, 2: 211,
        3: 235, 4: 260},

    'DP': {
        1: 211, 2: 211,
        3: 235, 4: 260},
}


VISUAL_RESUME_STARTER_VALUE = 225


# starter is value calculation on VISUAL_RESUME_STARTER_VALUE
# runner, expert, and veteran value is given percentage of starter value
# matrix value is in percentages
# 1 starter, 2 - runner, 3 - expert, 4 - veteran
VISUAL_RESUME_MATRIX_DICT = {
    'FR': {
        1: 100, 2: 100,
        3: 115, 4: 126},

    'FP': {
        1: 122, 2: 122,
        3: 146, 4: 171},

    'SP': {
        1: 166, 2: 166,
        3: 191, 4: 215},

    'EP': {
        1: 211, 2: 211,
        3: 235, 4: 260},

    'DP': {
        1: 211, 2: 211,
        3: 235, 4: 260},
}


PORTFOLIO_PRICE_MATRIX_DICT = {1: 700, 2: 800, 3: 900, 4: 900}

VISUAL_RESUME_MATRIX_DICT = {1: 75, 2: 80, 3: 85, 4: 85}

INTERNATIONAL_RESUME_MATRIX_DICT = {1: 75, 2: 80, 3: 85, 4: 85}

COUNTRY_SPCIFIC_VARIATION_MATRIX_DICT = {1: 75, 2: 80, 3: 85, 4: 85}

SECOND_REGULAR_RESUME_MATRIX_DICT = {1: 75, 2: 80, 3: 85, 4: 85}

EXECUTIVE_BIO_PRICE_MATRIX_DICT = {1: 500, 2: 500, 3: 550, 4: 600}

# 90% percentage
# 10 % penalty value
# 15% - 85%

# Addon Prices:
EXPRESS = 50
SUPER_EXPRESS = 125
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
COMBO_DISCOUNT_OF_TWO = 10  # in percentage
COMBO_DISCOUNT_OF_THREE = 20  # in percentage

# SLA Incentive and Penalty Parameter

REGULAR_SLA = 15
EXPRESS_SLA = 12
SUPER_EXPRESS_SLA = 10
PASS_PERCENTAGE = 85  # in percentage
INCENTIVE_PASS_PERCENTAGE = 95  # in percentage
PENALTY_PERCENTAGE = 10  # in percentage
INCENTIVE_PERCENTAGE = 10  # in percentage

# second regular 75 80 85
