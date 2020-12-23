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

            <figure id="domain-jobs" className="domain-jobs__img" data-aos="fade-up">
                <span className="domain-tween1" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100">
                    <img src={`${imageUrl}desktop/domain-tween1.svg`} />
                </span>
                <span className="domain-tween2" data-aos="zoom-out" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="200">
                    <img src={`${imageUrl}desktop/domain-tween2.svg`} />
                </span>
            </figure>
        </section>
    )
}

export default DomainJobs;