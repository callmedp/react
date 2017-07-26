from django.template.defaultfilters import slugify


class SaveSlug(object):

    def save_slug(self, slug, name):
        try:
            if slug and '_' in slug:
                return slugify(slug.replace("_", "-"))
            elif not slug and name:
                return slugify(name.replace("_", "-"))
        except:
            pass
        return slug


class ShineUserDetail(object):

    def get_shine_user_profile_detail(self, request):
        try:
            user_detail_dict = {}
            test_li = []
            job_li = []
            candidate_profile = request.session.get('candidate_profile', '')
            personal_details = candidate_profile.get('personal_detail', '')
            jobs = candidate_profile.get('jobs', '')

            for personal_detail in personal_details:
                user_detail_dict.update(personal_detail)

            for job in jobs:
                if job.get('is_current'):
                    test_li.append(job['company_name'])
                    job_li.append(job['job_title'])
                    
            user_detail_dict['company_name'] = test_li[1]
            user_detail_dict['job_title'] = job_li[1]
            tt_exp = 0
            if candidate_profile['total_experience']:
                experiences = candidate_profile['total_experience']
                for experience in experiences:
                    tt_exp = str(experience.get('experience_in_years'))+"years"+"-"+str(experience.get('experience_in_months'))+'months'
            user_detail_dict['total_exp']=tt_exp
        except Exception as e:
            pass
        return user_detail_dict

    def get_skills(self, request):
        candidate_profile = request.session.get('candidate_profile', '')
        skills = candidate_profile.get('skills', '')
        return skills

    def get_resume_file(self, request):
        resume_file = ""
        candidate_profile = request.session.get('candidate_profile', '')
        resume_data = candidate_profile.get('resumes', '')
        for data in resume_data:
            if data.get('is_default') == 1:
                resume_file = data.get('resume_name') + data.get('extension')
        return resume_file


