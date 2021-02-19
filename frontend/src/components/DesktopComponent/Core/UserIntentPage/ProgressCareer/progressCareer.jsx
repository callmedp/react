import React, { useRef, useEffect } from 'react';
import UIBanner from '../../../Common/UIBanner/UIbanner';
import UserGuidance from '../UserGuidance/UserGuidance';
import FindJob from '../FindRightJob/FindJob/findJob';
import ViewCourses from '../MakeCareerChange/ViewCourses/viewCourses';


const ProgressCareer = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job')

    return (
        <div>
            {/* <UIBanner /> */}
            <UIBanner {...props} />
            {/* <GuidanceRecommendations /> */}
            {/* <FindJob /> */}
            { !!job ? <ViewCourses /> : <FindJob type={"pcareer"} {...props}/> }
        </div>
    )
}

export default ProgressCareer;