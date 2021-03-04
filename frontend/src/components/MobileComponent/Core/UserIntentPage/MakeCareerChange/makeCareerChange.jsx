import React, { useRef, useEffect } from 'react';
import FindJob from '../FindRightJob/FindJob/findJob';
import ViewCourses from './ViewCourses/viewCourses';
import FeedbackResult from './ViewCourses/feedbackResult';
import Footer from 'components/MobileComponent/Common/Footer/Footer';


const MakeCareerChange = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job_title')

    return (
        <div>
            {/* <GuidanceRecommendations /> */}
            {/* <FindJob /> */}
            { !!job ? <><ViewCourses {...props} /><Footer /></> : <FindJob type={"career"} {...props}/> } 
            {/* <FeedbackResult /> */}
        </div>
    )
}

export default MakeCareerChange;