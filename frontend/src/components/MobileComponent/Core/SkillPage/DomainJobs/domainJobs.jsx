import React from 'react';
import { useDispatch, useSelector, connect } from 'react-redux';
import './domainJobs.scss';
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';



const DomainJobs = (props) => {

    const { jobsList } = useSelector(store => store.jobs) 
    const tracking_data = getTrackingInfo();
    const dispatch = useDispatch();
    
    return (
        jobsList?.length ? (
            <section className="m-container m-domain-jobs mb-0 mt-0 pt-0 pb-0" data-aos="fade-up">
                <div className="m-domain-jobs__list">
                    <strong className="m-heading2">Also Check</strong>
                    <ul>
                        {
                            jobsList?.map((job, index) => {
                                return (
                                    <li key={index}>
                                        <a href={job.url} onClick={() => trackUser({ "query" : tracking_data, "action" : 'exit_skill_page' })}>{job.name}</a>
                                    </li>
                                )
                            })
                        }
                    </ul>
                </div>
            </section>
        ) : ''
    )
}

const mapDispatchToProps = (dispatch) => {
    return {
        "trackUser": (data) => {
            return dispatch(trackUser(data))
        }
    }
}

export default connect(null, mapDispatchToProps)(DomainJobs);