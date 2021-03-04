import React from 'react';
import FindJob from '../FindRightJob/FindJob/findJob';
import ViewCourses from '../MakeCareerChange/ViewCourses/viewCourses';
import Footer from '../../../Common/Footer/Footer';


const ProgressCareer = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job_title')

    return (
        <div>
            {/* <GuidanceRecommendations /> */}
            {/* <FindJob /> */}
            { !!job ? <><ViewCourses {...props} /><Footer /></> : <FindJob type={"pcareer"} {...props}/> }
        </div>
    )
}

export default ProgressCareer;