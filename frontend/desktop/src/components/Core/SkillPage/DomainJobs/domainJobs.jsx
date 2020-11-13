import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import './domainJobs.scss';
import { fetchDomainJobs } from 'store/DomainJobs/actions/index';

const DomainJobs = (props) => {

    const dispatch = useDispatch()
    const jobList = useSelector(store => store.jobs.list) 

    useEffect(() => {
        dispatch(fetchDomainJobs())
    }, [])


    return (
        <section className="domain-jobs">
            <div className="domain-jobs__list">
                <strong className="heading3">Jobs in this domain</strong>
                <ul>
                    {
                        jobList?.map((job, index) => {
                            return (
                                <li key={index}>
                                    <a href={job.href}>{job.name}</a>
                                </li>
                            )
                        })
                    }
                    {/* <li><Link to={"#"}>Digital Marketing Jobs</Link></li>
                    <li><Link to={"#"}>Online Marketing Jobs</Link></li>
                    <li><Link to={"#"}>SEO Jobs</Link></li>
                    <li><Link to={"#"}>Business Development Jobs</Link></li>
                    <li><Link to={"#"}>Sales & Marketing Professionals</Link></li> */}
                </ul>
            </div>
            <figure className="domain-jobs__img">
                <img src="./media/images/domain-jobs.svg" alt="Jobs in this domain" />
            </figure>
        </section>
    )
}

export default DomainJobs;