import React, { useRef, useEffect } from 'react';
import GuidanceRecommendations from '../UserGuidance/Guidance/guidanceRecommendations';
import FindJob from '../FindRightJob/FindJob/findJob';
import ViewCourses from './ViewCourses/viewCourses';
import FeedbackResult from './ViewCourses/feedbackResult';


const MakeCareerChange = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job')

    return (
        <div>
            {/* <GuidanceRecommendations /> */}
            {/* <FindJob /> */}
            { !!job ? <ViewCourses /> : <FindJob type={"career"} {...props}/> } 
            {/* <FeedbackResult /> */}
        </div>
    )
}

export default MakeCareerChange;