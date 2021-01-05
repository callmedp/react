import { fetchSkillPageBanner } from 'store/SkillPage/Banner/actions';
import { fetchCoursesAndAssessments } from 'store/SkillPage/CoursesTray/actions/index';
import { fetchDomainJobs } from 'store/SkillPage/DomainJobs/actions';
import { fetchRecommendedProducts } from 'store/RecommendedCourses/actions/index';

export const getSkillPageActions = (params) => {
  return [
    { action: fetchSkillPageBanner, payload: { id: params?.id, 'medium': 0 } },
    { action: fetchCoursesAndAssessments, payload: { id: params?.id } },
    { action: fetchDomainJobs, payload: { id: params?.id } },
  ]
}

export const getSkillPageActionsMobile = (params) => {
  return [
    { action: fetchSkillPageBanner, payload: { id: params?.id, 'medium': 1 } },
    { action: fetchCoursesAndAssessments, payload: { id: params?.id, 'medium': 1 } },
    { action: fetchDomainJobs, payload: { id: params?.id } },
    { action: fetchRecommendedProducts, payload: {} },
  ]
}


