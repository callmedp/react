import { fetchSkillPageBanner } from 'store/SkillPage/Banner/actions';
import { fetchCoursesAndAssessments } from 'store/SkillPage/CoursesTray/actions/index';
import { fetchDomainJobs } from 'store/SkillPage/DomainJobs/actions';

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
  ]
}


const fetchApiData = async ({ dispatch }, params, actionGroup) => {

  let actionList = actionGroup(params);

  let results = [];
  try {
   
    results = await Promise.all(
      (actionList || []).map((caller,index) => {
       
        return new Promise((resolve, reject) =>
          dispatch(caller['action']({
            ...caller.payload,
            resolve,
            reject
          })))
      })
    )
  }
  catch (e) {
    console.log('Error occured in skillPageApi ', e);
    
  }
  return results;
}

export default fetchApiData;