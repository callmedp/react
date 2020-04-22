import React from 'react';
import { siteDomain } from '../../../../Utils/domains';

export default function GetExpertHelp() {
    return(
        <div className="get-expert-help">
            <div className="container-box">
                <h2><span>Get Expert Help</span></h2>
                <p className="mt-15">Make your resume more compelling with the help of our professional resume writers, who has helped over 10,000 professional to get interviewed in many companies and get hired quickly. Our experts will not only help in improving your score but also help you in customizing your resume as per your desired job and industry.</p>

                <ul className="get-expert-help__list">
                    <li><a href = {`${siteDomain}/services/resume-writing/63/`} style={{color:'grey'}}>Resume Writing</a></li>
                    <li><a href={`${siteDomain}/services/resume-services/entry-level-freshers/pd-2052`} style={{color:'grey'}}>Visual Resume</a></li>
                    <li><a href={`${siteDomain}/services/resume-services/entry-level-freshers-4/pd-2553`} style={{color:'grey'}}>International Resume</a></li>
                </ul>
            </div>
        </div>
    );
}