import React, { useRef, useEffect } from 'react';
import FindJob from '../FindRightJob/FindJob/findJob';
import ViewCourses from './ViewCourses/viewCourses';
import FeedbackResult from './ViewCourses/feedbackResult';
import Footer from 'components/MobileComponent/Common/Footer/Footer';


const MakeCareerChange = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job_title')

    useEffect(() => {
        if (!job) {
            props.setShowCTAPage(false)
        }
        return function cleanup() {
            props.setShowCTAPage(true)
        }
    })

    return (
        <div>
            {/* <GuidanceRecommendations /> */}
            {/* <FindJob /> */}
            { !!job ? <><ViewCourses {...props} /><Footer pageType={'user_intent_make_career_change'} /></> : <FindJob type={"career"} {...props}/> } 
            {/* <FeedbackResult /> */}
        </div>
    )
}

export default MakeCareerChange;