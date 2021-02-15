import React, { useRef, useEffect } from 'react';
import UIBanner from '../../../Common/UIBanner/UIbanner';
import UserGuidance from '../UserGuidance/UserGuidance';
import FindJob from './FindJob/findJob';
import ViewCourses from './ViewCourses/viewCourses';
import FeedbackResult from './ViewCourses/feedbackResult';


const MakeCareerChange = (props) => {

    

    return (
        <div>
            {/* <UIBanner /> */}
            <UIBanner {...props}/>
            {/* <GuidanceRecommendations /> */}
            <FindJob />
            {/* <ViewCourses /> */}
            {/* <FeedbackResult /> */}
        </div>
    )
}

export default MakeCareerChange;