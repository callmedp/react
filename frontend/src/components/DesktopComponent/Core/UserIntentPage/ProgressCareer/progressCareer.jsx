import React, { useRef, useEffect } from 'react';
import UIBanner from '../../../Common/UIBanner/UIbanner';
import UserGuidance from '../UserGuidance/UserGuidance';
import FindJob from './FindJob/findJob';
import ViewCourses from '../MakeCareerChange/ViewCourses/viewCourses';


const ProgressCareer = (props) => {
    return (
        <div>
            {/* <UIBanner /> */}
            <UIBanner {...props} />
            {/* <GuidanceRecommendations /> */}
            {/* <FindJob /> */}
            <ViewCourses />
        </div>
    )
}

export default ProgressCareer;