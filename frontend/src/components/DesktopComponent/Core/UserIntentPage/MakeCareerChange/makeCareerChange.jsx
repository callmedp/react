import React, { useRef, useEffect } from 'react';
import UIBanner from './UIBanner/UIbanner';
import UIBanner1 from './UIBanner/UIbanner1';
import GuidanceRecommendations from '../FindRightJob/GuidanceRecommendations/guidanceRecommendations';
import FindJob from './FindJob/findJob';
import ViewCourses from './ViewCourses/viewCourses';
import FeedbackResult from './ViewCourses/feedbackResult';


const MakeCareerChange = (props) => {
    return (
        <div>
            {/* <UIBanner /> */}
            <UIBanner1 />
            {/* <GuidanceRecommendations /> */}
            <FindJob />
            {/* <ViewCourses /> */}
            {/* <FeedbackResult /> */}
        </div>
    )
}

export default MakeCareerChange;