#python imports

#django imports

#local imports

#inter app imports

#third party imports

class ShineCandidate:
    """
    To save Shine candidate Detail data.
    Save this in redis to extract user from token.

    Sample Data - 

    {'bad_words_fields': {},
     'certifications': [],
     'id':'53ff1c11350d9d1f41ababfd',
     'candidate_id':'53ff1c11350d9d1f41ababfd',
     'desired_job': [{'candidate_id': '53ff1c11350d9d1f41ababfd',
       'candidate_location': [242],
       'functional_area': [1301],
       'industry': [0],
       'job_type': [0],
       'maximum_salary': [13],
       'minimum_salary': [7],
       'shift_type': [1]}],
     'education': [{'candidate_id': '53ff1c11350d9d1f41ababfd',
       'course_type': 1,
       'education_level': 110,
       'education_specialization': 503,
       'id': '5b3a69b94998e2428d0adfa6',
       'institute_name': 'Delhi College of Engineering',
       'year_of_passout': 2014}],
     'is_bad_word_present': False,
     'jobs': [{'candidate_id': '53ff1c11350d9d1f41ababfd',
       'company_name': 'HT Media',
       'description': '',
       'end_date': None,
       'end_month': None,
       'end_year': None,
       'id': '55655a68d6a4923b516efd42',
       'industry_id': 18,
       'industry_id_display_value': 'IT - Software',
       'is_current': True,
       'job_title': 'Python Developer',
       'job_title_lookup_id': None,
       'start_date': '2014-07-01T00:00:00',
       'start_month': 7,
       'start_year': 2014,
       'sub_field': 4530,
       'sub_field_display_value': 'Web / Mobile Technologies'}],
     'personal_detail': [{'candidate_location': 423,
       'cell_phone': '9717114180',
       'country_code': '91',
       'date_of_birth': '1991-12-20',
       'email': 'sanimesh007@gmail.com',
       'first_name': 'Animesh',
       'gender': 1,
       'id': '53ff1c11350d9d1f41ababfd',
       'is_cell_phone_verified': 0,
       'is_email_verified': 1,
       'is_featured_by_career_plus': False,
       'last_name': 'Sharma',
       'profile_badges': [],
       'resume_title': 'Software Engineer'}],
     'resumes': [{'candidate_id': '53ff1c11350d9d1f41ababfd',
       'creation_date': '2018-07-02T23:37:19',
       'extension': 'pdf',
       'id': '5b3a69d707fe270bf686c670',
       'is_default': 1,
       'resume_name': 'Animesh Sharma - Resume_02-Jul-18_23:37:20'}],
     'skills': [{'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6a724998e244038b7083',
       'value': 'Python',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'},
      {'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6a7a9924592cf8c39222',
       'value': 'Django',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'},
      {'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6a8807fe270b4263bc8a',
       'value': 'Rest APIs / Framework',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'},
      {'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6a944998e2434e67e0f1',
       'value': 'Solr / Lucene',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'},
      {'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6a9d445b890b2befbca3',
       'value': 'MongoDB',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'},
      {'candidate_id': '53ff1c11350d9d1f41ababfd',
       'id': '5b3a6aa89924592ef89311cf',
       'value': 'MySQL',
       'years_of_experience': 7,
       'years_of_experience_display_value': '4 Yrs'}],
     'total_experience': [{'experience_in_months': 0, 'experience_in_years': 7}],
     'workex': [{'experience_in_months': 0,
       'experience_in_years': 7,
       'id': '53ff1c11350d9d1f41ababfd',
       'notice_period': 0,
       'notice_period_last_working_date': None,
       'previous_salary': 7,
       'resume_title': 'Software Engineer',
       'salary_in_lakh': 3,
       'salary_in_thousand': 0,
       'summary': 'Experienced Web Developer with a demonstrated history of working in the internet industry. Skilled in Python, SQL, Solr, MongoDB, and Data Structures. Strong engineering professional with a B.Tech focused in Computer Science from Delhi College of Engineering.',
       'team_size_managed': 3}]}
    """

    def is_authenticated(self):
        return True

    def __init__(self,**kwargs):
        for key,value in kwargs.items():
            setattr(self,key,value)

    def __str__(self):
        return self.candidate_id



