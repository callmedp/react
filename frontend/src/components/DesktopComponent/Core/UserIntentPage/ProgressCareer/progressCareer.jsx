import React, { useRef, useEffect } from 'react';
import UIBanner from './UIBanner/UIbanner';
import UIBanner1 from './UIBanner/UIbanner1';
import GuidanceRecommendations from '../FindRightJob/GuidanceRecommendations/guidanceRecommendations';
import FindJob from './FindJob/findJob';
import ViewCourses from '../MakeCareerChange/ViewCourses/viewCourses';


const ProgressCareer = (props) => {
    return (
        <div>
            {/* <UIBanner /> */}
            <UIBanner1 />
            {/* <GuidanceRecommendations /> */}
            {/* <FindJob /> */}
            <ViewCourses />
        </div>
    )
}

export default ProgressCareer;