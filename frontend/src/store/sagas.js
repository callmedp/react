import { all } from 'redux-saga/effects'
import WatchLeadForm from './SkillPage/NeedHelp/saga/index';
import WatchDomainJobs from './SkillPage/DomainJobs/saga/index';
import WatchBannerData from './SkillPage/Banner/saga/index';
import WatchCoursesAndAssessments from './SkillPage/CoursesTray/saga';
import WatchHeader from './Header/saga/index';
import WatchFooter from './Footer/saga/index';
import WatchComments from './DashboardPage/AddSubmitComment/saga/index';
import WatchReviews from './DashboardPage/AddSubmitReview/saga/index';
import WatchRecommendation from './RecommendedCourses/saga/index';
import watchTracking from './Tracking/saga/index';
import WatchCataloguePage from './CataloguePage/saga/index';
import WatchDashboardMyWallet from './DashboardPage/MyWallet/saga/index';
import WatchDashboardMyOrders from './DashboardPage/MyOrder/saga/index';
import WatchDashboardMyCourses from './DashboardPage/MyCourses/saga/index';
import WatchDashboardMyServices from './DashboardPage/MyServices/saga/index';
import WatchHomePage from './HomePage/saga';
import WatchDashboardStartCourse from './DashboardPage/StartCourse/saga/index';
import WatchUserIntentPage from './UserIntentPage/saga';

export default function* () {
    yield all([
        WatchLeadForm(),
        WatchDomainJobs(),
        WatchBannerData(),
        WatchCoursesAndAssessments(),
        WatchHeader(),
        WatchFooter(),
        WatchComments(),
        WatchReviews(),
        WatchRecommendation(),
        watchTracking(),
        WatchCataloguePage(),
        WatchDashboardMyWallet(),
        WatchDashboardMyOrders(),
        WatchDashboardMyCourses(),
        WatchDashboardMyServices(),
        WatchHomePage(),
        WatchUserIntentPage()
    ])
}
