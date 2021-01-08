from rest_framework.response import Response
import json
from shop.choices import PRODUCT_CHOICES,PRODUCT_TAG_CHOICES
from shop.templatetags.shop_tags import get_faq_list, format_features, format_extra_features


def APIResponse(data=None, message=None, status=None, error=False):
    resp_json = {
        'message': message,
        'data': data,
        'status': status,
        'error': error
    }
    return Response(resp_json, status=status)


def CoursesFormatter(courses=[]):
    course_data = []
    for course in courses:
        d = json.loads(course.pVrs).get('var_list')
        data = {
            'imgUrl':course.pImg,
            'url':course.pURL,
            'name':course.pNm,
            'imgAlt':course.pImA,
            'rating': float(course.pARx),
            'mode':course.pStM[0] if course.pStM else None,
            'providerName':course.pPvn,
            'price':float(course.pPin),
            'skillList': course.pSkilln,
            'about':course.pAb,
            'title':course.pTt,
            'slug':course.pSg,
            'jobsAvailable':course.pNJ,
            'tags': PRODUCT_TAG_CHOICES[course.pTg][0],
            'brochure':json.loads(course.pUncdl[0]).get('brochure') if course.pUncdl else None,
            'u_courses_benefits':json.loads(course.pUncdl[0]).get('highlighted_benefits').split(';') if course.pUncdl else None,
            'u_desc': course.pDsc,
            'stars': course.pStar,
            'highlights':format_extra_features(course.pBS) if course.pBS else None,
            'id':course.id,
            }
        if len(d)!=0:
            data.update({
                'duration':d[0].get('dur_days'), 
                'type':d[0].get('type'),  
                'label':d[0].get('label'), 
                'level':d[0].get('level'), 
            })
        course_data.append(data)

    return course_data

def AssesmentsFormatter(assesments=[]):
    assessments_data = []
    for assessment in assesments:
        assessment_data = {
            'name':assessment.pNm,
            'imgUrl':assessment.pImg,
            'url':assessment.pURL,
            'rating':assessment.pARx,
            'mode': assessment.pStM,# :product_mode_choice
            'providerName':assessment.pPvn if assessment.pPvn else None,
            'price':float(assessment.pPin),
            'about':assessment.text,
            'jobsAvailable':assessment.pNJ,
            'tags':PRODUCT_TAG_CHOICES[assessment.pTg][1],
            'stars': assessment.pStar,
            'brochure':json.loads(assessment.pUncdl[0]).get('brochure') if assessment.pUncdl else None,
            'test_duration':json.loads(assessment.pAsft[0]).get('test_duration') if assessment.pAsft else None,
            'number_of_questions':json.loads(assessment.pAsft[0]).get('number_of_questions') if assessment.pAsft else None,
        }
        assessments_data.append(assessment_data)

    return assessments_data