import React from 'react';
import '../../SkillPage/DomainJobs/domainJobs.scss';
import {Link} from 'react-router-dom';

const ComboIncludes = (props) => {

    return (
        <section className="m-container m-domain-jobs mb-0 pt-0 pb-0" data-aos="fade-up">
            <div className="m-domain-jobs__list">
                <strong className="m-heading2">Combo includes</strong>
                <ul>
                    <li><Link to={"#"}>Featured Profile : 30 Days</Link></li>
                    <li><Link to={"#"}>AWS Architect Certification Training</Link></li>
                </ul>
            </div>
        </section>
    )
}

export default ComboIncludes;