import React, { useRef, useEffect } from 'react';
import GuidanceRecommendations from '../UserGuidance/Guidance/guidanceRecommendations';
import FindJob from './FindJob/findJob';
import ViewCourses from './ViewCourses/viewCourses';
import FeedbackResult from './ViewCourses/feedbackResult';


const MakeCareerChange = (props) => {
    return (
        <div>
            {/* <GuidanceRecommendations /> */}
            {/* <FindJob /> */}
            <ViewCourses />
            {/* <FeedbackResult /> */}
        </div>
    )
}

export default MakeCareerChange;