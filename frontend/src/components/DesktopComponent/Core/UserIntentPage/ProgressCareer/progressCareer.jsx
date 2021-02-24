import React from 'react';
import UIBanner from '../../../Common/UIBanner/UIbanner';
import FindJob from '../FindRightJob/FindJob/findJob';
import ViewCourses from './ViewCourses/viewCourses';


const ProgressCareer = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job_title')

    return (
        <div>
            {/* <UIBanner /> */}
            <UIBanner {...props} />
            {/* <GuidanceRecommendations /> */}
            {/* <FindJob /> */}
            { !!job ? <ViewCourses {...props} /> : <FindJob type={"pcareer"} {...props}/> }
        </div>
    )
}

export default ProgressCareer;