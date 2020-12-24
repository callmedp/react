import { all } from 'redux-saga/effects'
import WatchLeadForm from './SkillPage/NeedHelp/saga/index';
import WatchDomainJobs from './SkillPage/DomainJobs/saga/index';
import WatchBannerData from './SkillPage/Banner/saga/index';
import WatchCoursesAndAssessments from './SkillPage/CoursesTray/saga';
import WatchHeader from './Header/saga/index';
import WatchFooter from './Footer/saga/index';
import WatchRecommendation from './RecommendedCourses/saga/index';
import watchTracking from './Tracking/saga/index';

export default function* () {
    yield all([
        WatchLeadForm(),
        WatchDomainJobs(),
        WatchBannerData(),
        WatchCoursesAndAssessments(),
        WatchHeader(),
        WatchFooter(),
        WatchRecommendation(),
        watchTracking()
    ])
}