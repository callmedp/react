import { all } from 'redux-saga/effects'
import WatchLeadForm from './SkillPage/NeedHelp/saga/index';
import WatchDomainJobs from './SkillPage/DomainJobs/saga/index';
import WatchBannerData from './SkillPage/Banner/saga/index';
import WatchCoursesAndAssessments from './SkillPage/CoursesTray/saga';
import WatchHeader from './Header/saga/index';
import WatchFooter from './Footer/saga/index';
import WatchRecommendation from './RecommendedCourses/saga/index';
import watchTracking from './Tracking/saga/index';
import WatchCataloguePage from './CataloguePage/saga/index';
<<<<<<< HEAD
import WatchServicePage from './ServicePage/saga/index';
=======
import WatchDashboardMyWallet from './DashboardPage/MyWallet/saga/index';
>>>>>>> 23c20429e16eba4048ab52d929ea73051efad457

export default function* () {
    yield all([
        WatchLeadForm(),
        WatchDomainJobs(),
        WatchBannerData(),
        WatchCoursesAndAssessments(),
        WatchHeader(),
        WatchFooter(),
        WatchRecommendation(),
        watchTracking(),
        WatchCataloguePage(),
<<<<<<< HEAD
        WatchServicePage(),
=======
        WatchDashboardMyWallet()
>>>>>>> 23c20429e16eba4048ab52d929ea73051efad457
    ])
}
