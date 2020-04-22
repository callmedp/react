import React from 'react';
import { siteDomain } from '../../../../Utils/domains';

export default function GetExpertHelp() {
    return(
        <div className="get-expert-help">
            <div className="container-box">
                <h2><span>Get Expert Help</span></h2>
                <p className="mt-15">Shine Learning is India’s largest professional courses and career skills portal. Launched by Shine.com, Shine Learning has a vision to up-skill the Indian talent pool to adapt to the changing job market.Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry standard dummy text ever since the 1500s.</p>

                <ul className="get-expert-help__list">
                    <li><a href = {`${siteDomain}/services/resume-writing/63/`} style={{color:'grey'}}>Resume Writing</a></li>
                    <li><a href={`${siteDomain}/services/resume-services/entry-level-freshers/pd-2052`} style={{color:'grey'}}>Visual Resume</a></li>
                    <li><a href={`${siteDomain}/services/resume-services/entry-level-freshers-4/pd-2553`} style={{color:'grey'}}>International Resume</a></li>
                </ul>
            </div>
        </div>
    );
}