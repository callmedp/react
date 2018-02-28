
WRITER_TYPE = (
	(0, 'Select Type'),
	(1, 'Starter'),
	(2, 'Runner'),
	(3, 'Expert'),
	(4, 'Veteran'),
)

# writer invoices variants

WRITING_STARTER_VALUE = 180

# starter is value calculation on WRITING_STARTER_VALUE
# runner, expert, and veteran value is given percentage of starter value 
# matrix value is in percentages
RESUME_WRITING_MATRIX_DICT = {
	'FR': {
		1: 100, 2: 108,
		3: 115, 4: 122},

	'FP': {
		1: 170, 2: 184,
		3: 196, 4: 207},

	'SP': {
		1: 225, 2: 243,
		3: 259, 4: 275},

	'EP': {
		1: 357, 2: 386,
		3: 411, 4: 436},

	'DP': {
		1: 357, 2: 386,
		3: 411, 4: 436},

}


LINKEDIN_STARTER_VALUE = 400

# starter is value calculation on WRITING_STARTER_VALUE
# runner, expert, and veteran value is given percentage of starter value 
# matrix value is in percentages
# 1 starter, 2 - runner, 3 - expert, 4 - veteran
LINKEDIN_WRITING_MATRIX_DICT = {
	'FR': {
		1: 100, 2: 100,
		3: 135, 4: 140},

	'FP': {
		1: 100, 2: 100,
		3: 135, 4: 140},

	'SP': {
		1: 135, 2: 135,
		3: 182, 4: 189},

	'EP': {
		1: 135, 2: 135,
		3: 182, 4: 189},

	'DP': {
		1: 135, 2: 135,
		3: 182, 4: 189},
}


# Addon Prices:
EXPRESS = 75
SUPER_EXPRESS = 150
VISUAL_RESUME = 150
COVER_LETTER = 50
COUNTRY_SPCIFIC_VARIATION = 150
SECOND_REGULAR_RESUME = 150

# combo discount
DISCOUNT_ALLOCATION_DAYS = 15
COMBO_DISCOUNT = 25  # in percentage


# SLA Incentive and Penalty Parameter

REGULAR_SLA = 15
EXPRESS_SLA = 12
SUPER_EXPRESS_SLA = 10
PASS_PERCENTAGE = 60  # in percentage
INCENTIVE_PASS_PERCENTAGE = 85  # in percentage
PENALTY_PERCENTAGE = 10  # in percentage
INCENTIVE_PERCENTAGE = 15  # in percentage
