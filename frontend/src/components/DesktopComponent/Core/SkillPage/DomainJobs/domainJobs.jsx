import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import './domainJobs.scss';
import { fetchDomainJobs } from 'store/SkillPage/DomainJobs/actions';
import { imageUrl } from 'utils/domains';

const DomainJobs = (props) => {

    const dispatch = useDispatch()
    const { jobsList } = useSelector(store => store.jobs) 
    const pageId = props.pageId
    useEffect(() => {
        dispatch(fetchDomainJobs({id : pageId}))
    }, [pageId])


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