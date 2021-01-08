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
            'id':course.id,
            'name':course.pNm,
            'about':course.pAb,
            'url':course.pURL,
            'imgUrl':course.pImg,
            'imgAlt':course.pImA,
            'title':course.pTt,
            'slug':course.pSg,
            'jobsAvailable':course.pNJ,
            'skillList': course.pSkilln,
            'rating': float(course.pARx),
            'stars': course.pStar,
            'mode':', '.join(course.pStM) if course.pStM else [],
            'providerName':course.pPvn,
            'price':float(course.pPin),
            'tags': PRODUCT_TAG_CHOICES[course.pTg][0],
            'highlights':format_extra_features(course.pBS) if course.pBS else None,
            'brochure':json.loads(course.pUncdl[0]).get('brochure') if course.pUncdl else None,
            'u_courses_benefits':json.loads(course.pUncdl[0]).get('highlighted_benefits').split(';') if course.pUncdl else None,
            'u_desc': course.pDsc,
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
            'about':assessment.pAb,
            'url':assessment.pURL,
            'imgUrl':assessment.pImg,
            'rating':assessment.pARx,
            'stars': assessment.pStar,
            'jobsAvailable':assessment.pNJ,
            'skillList': assessment.pSkilln,
            'mode': ', '.join(assessment.pStM) if assessment.pStM else [],
            'providerName':assessment.pPvn if assessment.pPvn else None,
            'price':float(assessment.pPin),
            'tags':PRODUCT_TAG_CHOICES[assessment.pTg][1],
            'brochure':json.loads(assessment.pUncdl[0]).get('brochure') if assessment.pUncdl else None,
            'test_duration':json.loads(assessment.pAsft[0]).get('test_duration') if assessment.pAsft else None,
            'number_of_questions':json.loads(assessment.pAsft[0]).get('number_of_questions') if assessment.pAsft else None,
        }
        assessments_data.append(assessment_data)

    return assessments_data