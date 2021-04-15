import { combineReducers } from 'redux';
import { DomainJobsReducer } from './SkillPage/DomainJobs/reducer';
import { NeedHelpReducer } from './SkillPage/NeedHelp/reducer';
import { SkillPageBannerReducer } from './SkillPage/Banner/reducer'; 
import { CourseAndAssessmentsReducer } from './SkillPage/CoursesTray/reducer';
import { HeaderReducer } from './Header/reducer/index';
import { FooterReducer, PopularCoursesReducer } from './Footer/reducer/index';
import { LoaderReducer } from './Loader/reducer';
import { CommentReducer } from './DashboardPage/AddSubmitComment/reducer/index';
import { ReviewsReducer } from './DashboardPage/AddSubmitReview/reducer/index';
import { RecommendationReducer } from './RecommendedCourses/reducer/index';
import { RecentlyAddedCoursesReducer, PopularServicesReducer, TrendingCategoriesReducer, AllCategoriesReducer } from './CataloguePage/reducer/index';
import {FetchUserInfoReducer} from './Authentication/reducer/index'
import { DashboardMyWalletReducer } from './DashboardPage/MyWallet/reducer/index'; 
import { DashboardMyOrdersReducer } from './DashboardPage/MyOrder/reducer/index'; 
import { DashboardMyCoursesReducer } from './DashboardPage/MyCourses/reducer/index';
import { DashboardMyServicesReducer } from './DashboardPage/MyServices/reducer/index';
import { InDemandProductsReducer, JobAssistanceAndBlogsReducer, MostViewedCoursesReducer, TestimonialsReducer, SkillwithDemandsReducer   } from './HomePage/reducers';
import { DashboardMyServicesResumeReducer, OiDetailsReducer } from './DashboardPage/MyServices/reducer/index';
import { VendorUrlReducer } from './DashboardPage/StartCourse/reducer/index';
import { mainCoursesReducer, ProductReviewsReducer, RecommendedCoursesReducer, AddToCartReducer, AddToCartRedeemReducer } from './DetailPage/reducers';
import { findRightJobsReducer, upskillYourselfReducer,  serviceRecommendationReducer, ResumeScoreReducer } from './UserIntentPage/reducers';

const rootReducer = combineReducers({
    needHelp : NeedHelpReducer,
    jobs : DomainJobsReducer,
    skillBanner : SkillPageBannerReducer,
    coursesTray : CourseAndAssessmentsReducer,
    header : HeaderReducer,
    footer : FooterReducer,
    loader : LoaderReducer,
    getComment: CommentReducer,
    getReviews: ReviewsReducer,
    recommendation : RecommendationReducer,
    popularCourses : PopularCoursesReducer,
    recentCourses : RecentlyAddedCoursesReducer,
    popularServices : PopularServicesReducer,
    popularCategories : TrendingCategoriesReducer,
    allCategories : AllCategoriesReducer,
    authentication: FetchUserInfoReducer,
    dashboardWallet: DashboardMyWalletReducer,
    dashboardOrders: DashboardMyOrdersReducer,
    dashboardCourses: DashboardMyCoursesReducer,
    dashboardServices: DashboardMyServicesReducer,
    mostViewed: MostViewedCoursesReducer,
    inDemand: InDemandProductsReducer,
    jobAssistance: JobAssistanceAndBlogsReducer,
    testimonials: TestimonialsReducer,
    skillDemand: SkillwithDemandsReducer,
    dashboardPendingResume: DashboardMyServicesResumeReducer,
    oiDetails: OiDetailsReducer,
    vendorUrl: VendorUrlReducer,
    mainCourses: mainCoursesReducer,
    reviews: ProductReviewsReducer,
    recommendedCourses: RecommendedCoursesReducer,
    addToCartCourses: AddToCartReducer,
    addToCartRedeemCourses: AddToCartRedeemReducer,
    resumeScore: ResumeScoreReducer,
    findRightJob: findRightJobsReducer,
    upskillYourself: upskillYourselfReducer,
    serviceRecommend: serviceRecommendationReducer
});


export default rootReducer;
