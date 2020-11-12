import React from 'react';
import { Link } from 'react-router-dom';
import './domainJobs.scss';

const DomainJobs = (props) => {
    return (
        <section className="domain-jobs">
            <div className="domain-jobs__list">
                <strong className="heading3">Jobs in this domain</strong>
                <ul>
                    <li><Link to={"#"}>Digital Marketing Jobs</Link></li>
                    <li><Link to={"#"}>Online Marketing Jobs</Link></li>
                    <li><Link to={"#"}>SEO Jobs</Link></li>
                    <li><Link to={"#"}>Business Development Jobs</Link></li>
                    <li><Link to={"#"}>Sales & Marketing Professionals</Link></li>
                </ul>
            </div>
            <figure className="domain-jobs__img">
                <img src="./media/images/domain-jobs.svg" alt="Jobs in this domain" />
            </figure>
        </section>
    )
}

export default DomainJobs;