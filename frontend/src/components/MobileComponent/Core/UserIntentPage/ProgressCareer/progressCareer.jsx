import React, { useRef, useEffect } from 'react';
import GuidanceRecommendations from '../FindRightJob/GuidanceRecommendations/guidanceRecommendations';
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