import React from 'react';
import { Link } from 'react-router-dom';
import './domainJobs.scss';

const DomainJobs = (props) => {
    return (
        <section className="m-container m-domain-jobs mb-0 mt-0">
            <div className="m-domain-jobs__list">
                <strong className="m-heading2">Jobs in this domain</strong>
                <ul>
                    <li><Link to={"#"}>Digital Marketing Jobs</Link></li>
                    <li><Link to={"#"}>Online Marketing Jobs</Link></li>
                    <li><Link to={"#"}>SEO Jobs</Link></li>
                    <li><Link to={"#"}>Business Development Jobs</Link></li>
                    <li><Link to={"#"}>Sales & Marketing Professionals</Link></li>
                </ul>
            </div>
        </section>
    )
}

export default DomainJobs;