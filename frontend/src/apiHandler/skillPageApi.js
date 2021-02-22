import { fetchSkillPageBanner } from 'store/SkillPage/Banner/actions';
import { fetchCoursesAndAssessments } from 'store/SkillPage/CoursesTray/actions/index';
import { fetchDomainJobs } from 'store/SkillPage/DomainJobs/actions';
import { fetchRecommendedProducts } from 'store/RecommendedCourses/actions/index';
import { fetchPopularCourses } from 'store/Footer/actions/index';
import {fetchAlreadyLoggedInUser} from 'store/Authentication/actions/index';
import { CountryCode2 } from 'utils/storage';
import { sessionAvailability } from 'store/Header/actions/index';
const code2 = CountryCode2()

export const getSkillPageActions = (params) => {
  return [
    { action: fetchSkillPageBanner, payload: { id: params?.id, 'medium': 0, code2: code2  } },
    { action: fetchCoursesAndAssessments, payload: { id: params?.id, code2: code2  } },
    { action: fetchDomainJobs, payload: { id: params?.id, code2: code2  } },
    { action: fetchPopularCourses, payload: { id: params?.id, code2: code2 , courseOnly : true } },
  ]
}

export const getSkillPageActionsMobile = (params) => {
  return [
    { action: fetchSkillPageBanner, payload: { id: params?.id, 'medium': 1, code2: code2  } },
    { action: fetchCoursesAndAssessments, payload: { id: params?.id, 'medium': 1, code2: code2  } },
    { action: fetchDomainJobs, payload: { id: params?.id, code2: code2  } },
    { action: fetchRecommendedProducts, payload: { code2: code2 } },
    { action: fetchPopularCourses, payload: { id: params?.id, courseOnly : true, code2: code2  } },
  ]
}



