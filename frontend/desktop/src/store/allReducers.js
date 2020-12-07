
import { combineReducers } from 'redux';
import { DomainJobsReducer } from './SkillPage/DomainJobs/reducer';
import { NeedHelpReducer } from './SkillPage/NeedHelp/reducer';
import { SkillPageBannerReducer } from './SkillPage/Banner/reducer'; 
import { CourseAndAssessmentsReducer } from './SkillPage/CoursesTray/reducer';
import { PopularCoursesReducer } from './SkillPage/PopularCourses/reducer';
import { NavigationReducer } from './Common/Navigation/reducer';
import { HeaderReducer } from './Header/reducer/index';

const rootReducer = combineReducers({
    needHelp : NeedHelpReducer,
    jobs : DomainJobsReducer,
    skillBanner : SkillPageBannerReducer,
    coursesTray : CourseAndAssessmentsReducer,
    popularCourses : PopularCoursesReducer,
    navOffersAndTags: NavigationReducer,
    header : HeaderReducer
});


export default rootReducer;