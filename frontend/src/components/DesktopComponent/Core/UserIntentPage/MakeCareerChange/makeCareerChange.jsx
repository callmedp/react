import React, { useRef, useEffect } from 'react';
import UIBanner from '../../../Common/UIBanner/UIbanner';
import UserGuidance from '../UserGuidance/UserGuidance';
import FindJob from './FindJob/findJob';
import ViewCourses from './ViewCourses/viewCourses';
import FeedbackResult from './ViewCourses/feedbackResult';


const MakeCareerChange = (props) => {
    const params = new URLSearchParams(window.location.search);
    const job = params.get('job')

    return (
        <div>
            {/* <UIBanner /> */}
            <UIBanner {...props}/>
            {/* <GuidanceRecommendations /> */}
            { job === null ? <FindJob /> : <ViewCourses /> } 
            {/* <ViewCourses /> */}
            {/* <FeedbackResult /> */}
        </div>
    )
}

export default MakeCareerChange;