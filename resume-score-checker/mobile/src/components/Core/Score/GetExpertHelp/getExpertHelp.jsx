import React from 'react';
import { siteDomain } from '../../../../Utils/domains';
import { eventClicked } from '../../../../stores/googleAnalytics/actions/index';
import { useDispatch } from 'react-redux';


export default function GetExpertHelp() {
    const dispatch = useDispatch();
    const handleEventClick =(action,label) =>{
        dispatch(eventClicked({
            'action': action,
            'label': label
        }))
    }
    return(
        <div className="get-expert-help">
            <div className="container-box">
                <h2><span>Get Expert Help</span></h2>
                <p className="mt-15">Make your resume more compelling with the help of our professional resume writers, who has helped over 10,000 professional to get interviewed in many companies and get hired quickly. Our experts will not only help in improving your score but also help you in customizing your resume as per your desired job and industry.</p>

                <ul className="get-expert-help__list">
                    <li><a href = {`${siteDomain}/services/resume-writing/63/`} onClick={()=>handleEventClick('M_resumewriting','ExpertHelp')} style={{color:'grey'}}>Resume Writing</a></li>
                    <li><a href={`${siteDomain}/services/resume-services/entry-level-freshers/pd-2052`} onClick= {() =>handleEventClick('M_VisualResume','ExpertHelp')} style={{color:'grey'}}>Visual Resume</a></li>
                    <li><a href={`${siteDomain}/resume-builder/`} onClick= {() =>handleEventClick('M_Resume Builder','ExpertHelp')} style={{color:'grey'}}>Resume Builder</a></li>
                    <li><a href={`${siteDomain}/services/resume-services/entry-level-freshers-4/pd-2553`}  onClick={()=>handleEventClick('M_IntResume','ExpertHelp')} style={{color:'grey'}}>International Resume</a></li>
                </ul>
            </div>
        </div>
    );
}