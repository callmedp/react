import React from 'react';
import { useSelector } from 'react-redux';
import './domainJobs.scss';



const DomainJobs = (props) => {

    const { jobsList } = useSelector(store => store.jobs) 
    
    return (
        jobsList?.length ? (
            <section className="m-container m-domain-jobs mb-0 mt-0 pt-0 pb-0" data-aos="fade-up">
                <div className="m-domain-jobs__list">
                    <strong className="m-heading2">Jobs in this domain</strong>
                    <ul>
                        {
                            jobsList?.map((job, index) => {
                                return (
                                    <li key={index}>
                                        <a href={job.url}>{job.name}</a>
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

export default DomainJobs;