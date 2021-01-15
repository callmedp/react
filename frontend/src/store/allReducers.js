import { combineReducers } from 'redux';
import { DomainJobsReducer } from './SkillPage/DomainJobs/reducer';
import { NeedHelpReducer } from './SkillPage/NeedHelp/reducer';
import { SkillPageBannerReducer } from './SkillPage/Banner/reducer'; 
import { CourseAndAssessmentsReducer } from './SkillPage/CoursesTray/reducer';
import { HeaderReducer } from './Header/reducer/index';
import { FooterReducer, PopularCoursesReducer } from './Footer/reducer/index';
import { LoaderReducer } from './Loader/reducer';
import { RecommendationReducer } from './RecommendedCourses/reducer/index';
import { RecentlyAddedCoursesReducer, PopularServicesReducer, TrendingCategoriesReducer, AllCategoriesReducer } from './CataloguePage/reducer/index';
import { RecentlyServicesReducer } from './ServicePage/reducer/index';

const rootReducer = combineReducers({
    needHelp : NeedHelpReducer,
    jobs : DomainJobsReducer,
    skillBanner : SkillPageBannerReducer,
    coursesTray : CourseAndAssessmentsReducer,
    header : HeaderReducer,
    footer : FooterReducer,
    loader : LoaderReducer,
    recommendation : RecommendationReducer,
    popularCourses : PopularCoursesReducer,
    recentCourses : RecentlyAddedCoursesReducer,
    popularServices : PopularServicesReducer,
    popularCategories : TrendingCategoriesReducer,
    allCategories : AllCategoriesReducer,
    allServices : RecentlyServicesReducer

});


export default rootReducer;
