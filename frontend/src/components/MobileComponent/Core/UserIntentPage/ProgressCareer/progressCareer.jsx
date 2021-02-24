import React, { useRef, useEffect } from 'react';
import FindJob from '../FindRightJob/FindJob/findJob';
import ViewCourses from '../MakeCareerChange/ViewCourses/viewCourses';


const ProgressCareer = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job_title')

    return (
        <div>
            {/* <GuidanceRecommendations /> */}
            {/* <FindJob /> */}
            { !!job ? <ViewCourses /> : <FindJob type={"pcareer"} {...props}/> }
        </div>
    )
}

export default ProgressCareer;