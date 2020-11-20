
import { combineReducers } from 'redux';
import { DomainJobsReducer } from './SkillPage/DomainJobs/reducer';
import { NeedHelpReducer } from './SkillPage/NeedHelp/reducer';
import { SkillPageBannerReducer } from './SkillPage/Banner/reducer'; 
import { CourseAndAssessmentsReducer } from './SkillPage/CourseTray/reducer';
import { PopularCoursesReducer } from './SkillPage/PopularCourses/reducer';


const rootReducer = combineReducers({
    needHelp : NeedHelpReducer,
    jobs : DomainJobsReducer,
    skillBanner : SkillPageBannerReducer,
    courseTray : CourseAndAssessmentsReducer,
    popularCourses : PopularCoursesReducer
});


export default rootReducer;