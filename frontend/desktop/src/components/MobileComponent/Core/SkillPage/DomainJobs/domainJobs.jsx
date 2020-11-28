import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import './domainJobs.scss';
import { fetchDomainJobs } from 'store/SkillPage/DomainJobs/actions';


const DomainJobs = (props) => {

    const dispatch = useDispatch()
    const { jobsList } = useSelector(store => store.jobs) 
    const pageId = props.pageId
    useEffect(() => {
        dispatch(fetchDomainJobs({id : pageId}))
    }, [])

    return (
        jobsList?.length ? (
            <section className="m-container m-domain-jobs mb-0 mt-0">
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