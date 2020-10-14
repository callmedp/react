from django.template.defaultfilters import slugify
import logging

class SaveSlug(object):

    def save_slug(self, slug, name):
        try:
            if slug and '_' in slug:
                return slugify(slug.replace("_", "-"))
            elif not slug and name:
                return slugify(name.replace("_", "-"))
        except Exception as e:
            logging.getLogger('error_log').error('unable to replace slug %s' % str(e))
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
            logging.getLogger('error_log').error(str(e))
            pass
        return user_detail_dict

    def get_skills(self, request):
        skills = ""
        if request.session.get('candidate_profile', ''):
            candidate_profile = request.session.get('candidate_profile', '')
            skills = candidate_profile.get('skills', '')
        else:
            skills = {}
        return skills

    def get_resume_file(self, request):
        resume_file = ""
        if request.session.get('candidate_profile'):
            candidate_profile = request.session.get('candidate_profile', '')
            resume_data = candidate_profile.get('resumes', '')
            for data in resume_data:
                if data.get('is_default') == 1:
                    resume_file = data.get('resume_name') + data.get('extension')
        else:
            resume_file = {}
        return resume_file

    def update_resume_in_session(self, request, file_dict):
        try:
            ff = file_dict.get('resume_file').name
            files = ff.split('.')
            if request.session.get('candidate_profile'):
                candidate_profile = request.session.get('candidate_profile', '')
                resume_data = candidate_profile.get('resumes', '')
                for data in resume_data:
                    if data.get('is_default') == 1:
                        data.update({
                            'resume_name': files[0], 'extension': files[1]
                        })
        except Exception as e:
            logging.getLogger('error_log').error('unable to update resume file %s' % str(e))

            pass
