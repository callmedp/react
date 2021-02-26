import React from 'react';
import { shineSiteUrl } from 'utils/domains';

const JobListing = (props) => {

    const { jobList } = props;

    return (
        <ul className="shine-courses-listing ml-10n mt-30">
            {
                jobList?.map((job, index) => {
                    return (
                        <li className="col" key={index}>
                            <div className="course">
                                <div className="d-flex p-20">
                                    <div className="course__content">
                                    {
                                            job.jHJ === 1 && 
                                            <span className="hot-badge">
                                                <figure className="icon-hot"></figure> Hot
                                            </span>
                                        }
                                        {
                                            job.jPJ === 1 && 
                                            <span className="premium-badge">
                                                <figure className="icon-premium"></figure> Premium
                                            </span>
                                        }
                                        <h3 className="heading3">
                                            <a target="_blank" href={`${shineSiteUrl}${job.jSlug}`}>{ job?.jJT }</a>
                                        </h3>
                                        <strong>{job?.jCName}</strong>

                                        <ul>
                                            <li>{ job?.jExp } </li>
                                            <li>{ job?.jLoc?.join(", ")}</li>
                                        </ul>

                                        <p className="mt-10">{ job?.jJDT }</p>
                                    </div>
                                    <div className="course__price-date">
                                        <span>
                                        {new Date(job?.jPDate).toLocaleString('en-us',{month:'short', year:'numeric', day:'numeric'})}
                                        </span>
                                        <a target="_blank" href={`${shineSiteUrl}${job?.jSlug}`} className="btn btn-secondary mt-10">Apply now</a>
                                    </div>
                                </div>
                                <div className="course__bottom">
                                    <strong>Skills: </strong>
                                    <ul>
                                       <li> { job?.jKwd } </li>
                                    </ul>
                                </div>
                            </div>
                        </li>
                    )
                })
            }
        </ul>
    )
}

export default JobListing;
