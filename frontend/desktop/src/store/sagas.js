import { all } from 'redux-saga/effects'
import WatchLeadForm from './NeedHelp/saga/index';
import WatchDomainJobs from './DomainJobs/saga/index';


export default function* () {
    yield all([
        WatchLeadForm(),
        WatchDomainJobs()
    ])
}