import React from 'react';
import { shineSiteUrl } from 'utils/domains';

const JobListing = (props) => {

    const { jobList } = props;

    return (
        <ul className="m-shine-courses-listing mt-20">
            {
                jobList?.map((jData,indx) => {
                    return(
                        <li key={indx}>
                            <div className="course">
                                <div className="d-flex p-15">
                                    <div className="course__content">
                                        {
                                            jData.jHJ === 1 && 
                                            <span className="hot-badge">
                                                <figure className="micon-hot"></figure> Hot
                                            </span>
                                        }
                                        {
                                            jData.jPJ === 1 && 
                                            <span className="premium-badge">
                                                <figure className="micon-premium"></figure> Premium
                                            </span>
                                        }
                                        <h3 className="heading3">
                                            <a href={`${shineSiteUrl}${jData.jSlug}`} target="_blank">{jData.jJT}</a>
                                        </h3>
                                        <strong>{jData.jCName}</strong>
                                        <div className="d-flex">
                                            <ul>
                                                <li>{jData.jExp}</li>
                                                <li>{jData.jLoc.join(', ')}</li>
                                                <li>
                                                    {jData.jKwd.split(',').slice(0,5).join(', ')}...
                                                </li>
                                            </ul>
                                            <div className="m-price-date">
                                                {jData.jRUrl && <a href={jData.jRUrl} target="_blank" className="btn-blue-outline mb-10">Apply</a>}
                                                <span>{new Date(jData.jPDate).toLocaleString('en-us',{month:'short', year:'numeric', day:'numeric'})}</span> 
                                            </div>
                                        </div>
                                    </div>
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
