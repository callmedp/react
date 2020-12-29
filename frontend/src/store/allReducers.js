
import { combineReducers } from 'redux';
import { DomainJobsReducer } from './SkillPage/DomainJobs/reducer';
import { NeedHelpReducer } from './SkillPage/NeedHelp/reducer';
import { SkillPageBannerReducer } from './SkillPage/Banner/reducer'; 
import { CourseAndAssessmentsReducer } from './SkillPage/CoursesTray/reducer';
import { HeaderReducer } from './Header/reducer/index';
import { FooterReducer } from './Footer/reducer/index';
import { LoaderReducer } from './Loader/reducer';
import { RecommendationReducer } from './RecommendedCourses/reducer/index';
import { RecentlyAddedCoursesReducer } from './CataloguePage/reducer/index';

const rootReducer = combineReducers({
    needHelp : NeedHelpReducer,
    jobs : DomainJobsReducer,
    skillBanner : SkillPageBannerReducer,
    coursesTray : CourseAndAssessmentsReducer,
    header : HeaderReducer,
    footer : FooterReducer,
    loader : LoaderReducer,
    recommendation : RecommendationReducer,
    recentCourses : RecentlyAddedCoursesReducer,
});


export default rootReducer;