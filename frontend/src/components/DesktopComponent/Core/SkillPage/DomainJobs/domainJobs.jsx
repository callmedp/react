import React from 'react';
import { useSelector } from 'react-redux';
import './domainJobs.scss';

import { imageUrl } from 'utils/domains';

const DomainJobs = (props) => {

    const { jobsList } = useSelector(store => store.jobs) 


    return (
        <section className="domain-jobs">
            <div className="domain-jobs__list">
                <strong className="heading3">Jobs in this domain</strong>
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
            <figure className="domain-jobs__img">
                <img src={`${imageUrl}desktop/domain-jobs.svg`} alt="Jobs in this domain" />
            </figure>
        </section>
    )
}

export default DomainJobs;