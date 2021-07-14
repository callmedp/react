import React, {useEffect} from 'react';
import FindJob from '../FindRightJob/FindJob/findJob';
import ViewCourses from '../MakeCareerChange/ViewCourses/viewCourses';
import Footer from '../../../Common/Footer/Footer';


const ProgressCareer = (props) => {
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
            { !!job ? <><ViewCourses {...props} /><Footer pageType={'user_intent_progress_career'} /></> : <FindJob type={"pcareer"} {...props}/> }
        </div>
    )
}

export default ProgressCareer;