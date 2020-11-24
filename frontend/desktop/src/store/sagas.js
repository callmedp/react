import { all } from 'redux-saga/effects'
import WatchLeadForm from './SkillPage/NeedHelp/saga/index';
import WatchDomainJobs from './SkillPage/DomainJobs/saga/index';
import WatchBannerData from './SkillPage/Banner/saga/index';
import WatchCoursesAndAssessments from './SkillPage/CoursesTray/saga';

export default function* () {
    yield all([
        WatchLeadForm(),
        WatchDomainJobs(),
        WatchBannerData(),
        WatchCoursesAndAssessments()
    ])
}