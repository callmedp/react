import requests
import logging

from datetime import date
import json
from django.conf import settings
from shine.core import ShineCandidateDetail
from microsite.roundoneapi import RoundOneAPI
from microsite.common import ShineUserDetail


class RoundOneMixin(RoundOneAPI):

    def roundone_personal_submit(self, data={}, request=None):
        try:
            name = data.get("first")
            contact = data.get("mobile")
            total_exp = data.get("total_exp")
            roundone_profile = request.session.get("roundone_profile")
            if not roundone_profile:
                roundone_profile = self.get_roundone_profile(request)
            if roundone_profile.get("response"):
                rouser = roundone_profile.get("user")
                rouser.update({
                    "name": name,
                    "mobile": contact,
                    "total_exp": total_exp,
                    "skills": ','.join(data.getlist("skill"))
                })
                response_json = self.post_roundone_profile(request, roundone_profile)
                if response_json.get("response"):
                    request.session.update({
                        "roundone_profile": roundone_profile})
                    return True, response_json.get("msg")
        except Exception as e:
            logging.getLogger('error_log').error('unable to submit details%s'%str(e))

        return False, 'Profile Not Updated'

    def roundone_edit_education(self, data, request, index_edu):
        try:
            institute_list = data.getlist("institute", "")
            degree_list = data.getlist("level", "")
            major_list = data.getlist("specialization", "")
            year_list = data.getlist("passout_year", "")
            marks_list = data.getlist("marks", "")

            if institute_list and degree_list and year_list and marks_list and major_list:
                try:
                    institute = institute_list[index_edu]
                except Exception as e:
                    logging.getLogger('error_log').error('unable to get institution%s' % str(e))
                    institute = ''
                try:
                    degree = degree_list[index_edu]
                except Exception as e:
                    logging.getLogger('error_log').error('unable to get degree%s' % str(e))
                    degree = ''
                try:
                    major = major_list[index_edu]
                except Exception as e:
                    logging.getLogger('error_log').error('unable to get major %s' % str(e))
                    major = ''
                try:
                    year = year_list[index_edu]
                except Exception as e:
                    logging.getLogger('error_log').error('unable to get year %s' % str(e))
                    year = 1900
                try:
                    marks = marks_list[index_edu]
                except Exception as e:
                    logging.getLogger('error_log').error('unable to get marks%s' % str(e))

                    marks = 1

                roundone_profile = request.session.get("roundone_profile")
                if not roundone_profile:
                    roundone_profile = self.get_roundone_profile(request)
                if roundone_profile.get("response"):
                    rouser = roundone_profile.get("user")
                    user_education = rouser.get("education", [])
                    edit_education = {
                        "institute": institute,
                        "degree": degree,
                        "major": major,
                        "year": year,
                        "marks": marks,
                    }
                    user_education.append(edit_education)

                    rouser.update({
                        "education": user_education
                    })

                    response_json = self.post_roundone_profile(request, roundone_profile)

                    if response_json.get("response"):
                        request.session.update({
                            "roundone_profile": roundone_profile})
                        return response_json.get("status"), response_json.get("msg")
        except Exception as e:
            logging.getLogger('error_log').error('unable to edit education details %s'%str(e))

        return False, 'Education Not Updated'

    def roundone_edit_employment(self, data, request, index_job):
        try:
            company_list = data.getlist("company")
            position_list = data.getlist("position")
            start_month_list = data.getlist("start_month")
            start_year_list = data.getlist("start_year")
            end_month_list = data.getlist("end_month")
            end_year_list = data.getlist("end_year")

            if company_list and position_list:
                try:
                    company = company_list[index_job]
                except Exception as e:
                    logging.getLogger('error_log').error('unable to get company %s' % str(e))
                    company = ''
                try:
                    position = position_list[index_job]
                except Exception as e:
                    logging.getLogger('error_log').error('unable to get position %s' % str(e))
                    position = ''
                try:
                    emp_from = date(int(start_year_list[index_job]), 1, int(start_month_list[index_job])).strftime("%Y-%m-%d")
                except Exception as e:
                    logging.getLogger('error_log').error('unable to get  job date from %s' % str(e))
                    emp_from = ''
                try:
                    emp_to = date(int(end_year_list[index_job]), 1, int(end_month_list[index_job])).strftime("%Y-%m-%d")
                except Exception as e:
                    logging.getLogger('error_log').error('unable to get job date to%s' % str(e))
                    emp_to = ''

                roundone_profile = request.session.get("roundone_profile")
                if not roundone_profile:
                    roundone_profile = self.get_roundone_profile(request)
                if roundone_profile.get("response"):
                    rouser = roundone_profile.get("user")
                    user_emp = rouser.get("employments", [])

                    if data.get('current'):
                        edit_emp = {
                            "company": company,
                            "position": position,
                            "from": emp_from,
                            "to": emp_to,
                            "current": 1,
                        }
                    else:
                        edit_emp = {
                            "company": company,
                            "position": position,
                            "from": emp_from,
                            "to": emp_to,
                            "current": 0,
                        }
                    user_emp.append(edit_emp)

                    rouser.update({
                        "education": user_emp
                    })

                    response_json = self.post_roundone_profile(request, roundone_profile)

                    if response_json.get("response"):
                        request.session.update({
                            "roundone_profile": roundone_profile})
                        return True, response_json.get("msg")
        except Exception as e:
            logging.getLogger('error_log').error('unable to update employment information %s'%str(e))

        return False, 'Education Not Updated'


class UpdateShineProfileMixin(ShineCandidateDetail, RoundOneMixin):

    def update_candidate_personal(self, shine_id=None, user_access_token=None,
                              client_token=None, data={}, type_of=None, token=None):
        error_msg = "Personal Details not updated"
        personal_response = None
        try:
            if not client_token:
                client_token = self.get_client_token()
            if shine_id and data and user_access_token:
                email = data.get('email', '')
                first_name = data.get("first", "")
                last_name = data.get('last')
                mobile = data.get("mobile", "")
                resume_title = data.get('resume_title', '')
                country_code = data.get('mobile_country', None)
                gender = 1 if data.get('gender') == "Mail" else 2
                if email and mobile and first_name:
                    personal_data = {
                        "candidate_id": shine_id,
                        "first_name": first_name,
                        "last_name": last_name,
                        "cell_phone": mobile,
                        "email": email,
                        "country_code": country_code,
                        "gender": gender,
                        'resume_title':resume_title
                    }

                    request_header = self.get_api_headers(token=token)

                    if type_of == "edit":
                        if shine_id is None:
                            raise "Candidate id does not exist."
                        personal_url = settings.SHINE_SITE + "/api/v2/candidate-personal-details/" +\
                            shine_id + "/?format=json"
                        personal_response = requests.put(
                            personal_url, data=personal_data, headers=request_header)
                        status, msg = self.roundone_personal_submit(data, self.request)

                    if personal_response.status_code in [200, 201] and status:
                        return True, ""

        except Exception as e:
            logging.getLogger('error_log').error('unable to update personal details %s'%str(e))
        if personal_response and personal_response.json():
            personal_response_json = personal_response.json()
            error_msg = personal_response_json.get("non_field_errors", error_msg)
        return False, error_msg

    def update_candidate_jobs(self, shine_id=None, user_access_token=None,
                              client_token=None, data={}, type_of=None, token=None):
        error_msg = "Jobs Update Failed"
        jobs_response = None
        returnlist = []

        try:
            if not client_token:
                client_token = self.get_client_token()

            if shine_id and data and user_access_token:
                job_title_list = data.getlist("position", [])
                company_list = data.getlist("company", [])
                start_year_list = data.getlist("start_year", [])
                start_month_list = data.getlist("start_month", [])
                end_year_list = data.getlist("end_year", [])
                end_month_list = data.getlist("end_month", [])
                sub_field_list = data.getlist("sub_field", [])
                id_list = data.getlist("id", [])
                industry_id_list = data.getlist("industry_id", [])

                job_title = ""
                company_name = ""
                is_current = False
                sub_field = 1001
                industry_id = 1
                start_year = 2014
                start_month = 1
                end_year = 2015
                end_month = 1

                for job in range(len(id_list)):
                    job_title = job_title_list[job]
                    company_name = company_list[job]
                    sub_field = sub_field_list[job]
                    industry_id = industry_id_list[job]
                    start_year = start_year_list[job]
                    start_month = start_month_list[job]
                    try:
                        end_year = end_year_list[job]
                        end_month = end_month_list[job]
                    except Exception as e:
                        logging.getLogger('error_log').error(str(e))
                        end_year = ""
                        end_month = ""
                    if data.get('current', False) and end_year == "" and end_month == "":
                        jobs_data = {
                            "candidate_id": shine_id,
                            "sub_field": sub_field,
                            "job_title": job_title,
                            "industry_id": industry_id,
                            "is_current": data.get("current", False),
                            "description": data.get("description", " "),
                            "company_name": company_name,
                            "start_year": start_year,
                            "start_month": start_month,
                            "end_year": end_year,
                            "end_month": end_month
                        }
                    else:
                        jobs_data = {
                            "candidate_id": shine_id,
                            "sub_field": sub_field,
                            "job_title": job_title,
                            "industry_id": industry_id,
                            "is_current": is_current,
                            "description": data.get("description", " "),
                            "company_name": company_name,
                            "start_year": start_year,
                            "start_month": start_month,
                            "end_year": end_year,
                            "end_month": end_month
                        }
                    request_header = self.get_api_headers(token=token)
                    if type_of == "edit":
                        if not id_list[job]:
                            return False, "Job id doesnot exists."

                        jobs_url = settings.SHINE_SITE + "/api/v2/candidate/" +\
                            shine_id + "/jobs/" + id_list[job] + "/?format=json"

                        jobs_response = requests.put(
                            jobs_url, data=jobs_data, headers=request_header)

                        status, msg = self.roundone_edit_employment(
                            data, self.request, job)

                    if jobs_response.status_code in [200, 201]:
                        returnlist.append(True)
                if False not in returnlist:
                    return True, ""
        except Exception as e:
            logging.getLogger('error_log').error('unable to update employment information%s'%str(e))

        if jobs_response and jobs_response.json():
            jobs_response_json = jobs_response.json()
            error_msg = jobs_response_json.get("non_field_errors", error_msg)
        return False, error_msg

    def update_candidate_education(self, shine_id=None, user_access_token=None,
                                   client_token=None, data={}, type_of=None, token=None):
        error_msg = "Education Update Failed"
        educations_response = None
        returnlist = []

        try:
            if not client_token:
                client_token = self.get_client_token()
            if shine_id and data and user_access_token:

                id_list = data.getlist("id", [])
                institute_name_list = data.getlist("institute", [])
                year_of_passout_list = data.getlist("passout_year", [])
                course_type_list = data.getlist("course_type", [])
                education_specialization_list = data.getlist("specialization", [])
                education_level_list = data.getlist("level", [])

                institute_name = ""
                education_level = 20
                education_specialization = 1
                year_of_passout = 2015
                course_type = 1
                
                for education in range(len(id_list)):
                    education_level = education_level_list[education]
                    education_specialization = education_specialization_list[education]
                    institute_name = institute_name_list[education]
                    year_of_passout = year_of_passout_list[education]
                    course_type = course_type_list[education]
                    
                    education_data = {
                        "candidate_id": shine_id,
                        "education_level": education_level,
                        "education_specialization": education_specialization,
                        "institute_name": institute_name,
                        "year_of_passout": year_of_passout,
                        "course_type": course_type
                    }

                    request_header = self.get_api_headers(token=token)

                    if type_of == "edit":
                        if not id_list[education]:
                            return False, "The education id doesnot exists."
                        educations_url = settings.SHINE_SITE + \
                            "/api/v2/candidate/" + shine_id + "/educations/" + \
                            id_list[education] + "/?format=json"

                        edu_rsp = requests.put(
                            educations_url, data=education_data, headers=request_header)
                        # status, msg = self.roundone_personal_submit(data, self.request)
                        status, msg = self.roundone_edit_education(data, self.request, education)

                    if edu_rsp.status_code in [201, 200] and status:
                        returnlist.append(True)

                if False not in returnlist:
                    return True, ""

        except Exception as e:
            logging.getLogger('error_log').error('unable to update candidate education %s'%str(e))

        if edu_rsp and edu_rsp.json():
            edu_rsp_json = edu_rsp.json()
            error_msg = edu_rsp_json.get("non_field_errors", error_msg)
        return False, error_msg

    def update_candidate_skills(self, shine_id=None, user_access_token=None,
                                client_token=None, data={}, type_of=None, token=None):
        error_msg = "Skill Update Failed"
        skills_response = None

        try:
            returnlist = []

            if not client_token:
                client_token = self.get_client_token()

            if shine_id and data and user_access_token:
                skill_list = data.getlist("skill", [])
                years_list = data.getlist("level_id", [])

                skill_level_dict = dict(zip(skill_list, years_list))

                request_header = self.get_api_headers(token=token)
                request_header.update({'Content-Type':'application/json', 'Accept':'application/json'})

                for skill, level_id in skill_level_dict.items():
                    sk_list = []
                    try:
                        years_of_experience = int(level_id)
                    except Exception as e:
                        logging.getLogger('error_log').error('unable to get years of experience %s' % str(e))
                        years_of_experience = 4

                    sk_list.append({"value": skill, "years_of_experience": years_of_experience})

                    skill_data = {
                        "candidate_id": shine_id,
                        'skills_data':sk_list
                    }

                    if type_of == "edit":
                        skills_url = settings.SHINE_SITE + "/api/v2/candidate/" +\
                            shine_id + "/bulk-skills/"

                        skills_response = requests.post(
                            skills_url, data=json.dumps(skill_data), headers=request_header)

                        status, msg = self.roundone_personal_submit(data, self.request)

                    if skills_response.status_code in [200, 201] and status:
                        returnlist.append(True)

                if False not in returnlist:
                    return True, ""
        except Exception as e:
            logging.getLogger('error_log').error('unable to update candidate skills%s'%str(e))

        if skills_response and skills_response.json():
            skills_response_json = skills_response.json()
            error_msg = skills_response_json.get("non_field_errors", error_msg)
        return False, error_msg

    def upload_resume(self, shine_id=None, user_access_token=None, client_token=None, data={}, type_of=None, token=None):
        try:
            if not client_token:
                client_token = self.get_client_token()

            if shine_id and data and user_access_token:
                upload_source = "web"
                upload_medium = "direct"
                file = self.request.FILES.get('resume')
                resume_data = {
                    "candidate_id": shine_id,
                    "upload_source": upload_source,
                    "upload_medium": upload_medium,
                }
                files = {'resume_file': file}
                request_header = self.get_api_headers(token=token)
                if type_of == "edit":
                    resume_url = settings.SHINE_SITE + "/api/v2/candidate/" +\
                        shine_id + "/resumefiles/?format=json"

                    resume_response = requests.post(
                        resume_url, files=files, data=resume_data,
                        headers=request_header)
                    if resume_response.status_code in [201, 200]:
                        ShineUserDetail().update_resume_in_session(
                            self.request, files)
                        return True, ""
                    elif resume_response.status_code not in [201, 200]:
                        json_rsp = resume_response.json()
                        return False, json_rsp
        except Exception as e:
            logging.getLogger('error_log').error('unable to upload resume%s'%str(e))
