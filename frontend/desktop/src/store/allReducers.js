import DomainJobs from 'components/Core/SkillPage/DomainJobs/domainJobs';
import { combineReducers } from 'redux';
import { DomainJobsReducer } from './DomainJobs/reducer';
import { NeedHelpReducer } from './NeedHelp/reducer';



const rootReducer = combineReducers({
    needHelp : NeedHelpReducer,
    jobs : DomainJobsReducer,
});


export default rootReducer;