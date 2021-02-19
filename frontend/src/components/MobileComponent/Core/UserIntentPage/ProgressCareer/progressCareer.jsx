import React, { useRef, useEffect } from 'react';
import GuidanceRecommendations from '../UserGuidance/Guidance/guidanceRecommendations';
import FindJob from '../FindRightJob/FindJob/findJob';
import ViewCourses from '../MakeCareerChange/ViewCourses/viewCourses';


const ProgressCareer = (props) => {
    return (
        <div>
            {/* <GuidanceRecommendations /> */}
            {/* <FindJob /> */}
            <ViewCourses />
        </div>
    )
}

export default ProgressCareer;