import React, { useRef, useEffect } from 'react';
import UIBanner from '../../../Common/UIBanner/UIbanner';
import UserGuidance from '../UserGuidance/UserGuidance';
import FindJob from '../FindRightJob/FindJob/findJob';
import ViewCourses from './ViewCourses/viewCourses';
import FeedbackResult from './ViewCourses/feedbackResult';


const MakeCareerChange = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job')

    return (
        <div>
            {/* <UIBanner /> */}
            <UIBanner {...props}/>
            {/* <GuidanceRecommendations /> */}
            { !!job ? <ViewCourses /> : <FindJob type={"career"} {...props}/> } 
            {/* <ViewCourses /> */}
            {/* <FeedbackResult /> */}
        </div>
    )
}

export default MakeCareerChange;