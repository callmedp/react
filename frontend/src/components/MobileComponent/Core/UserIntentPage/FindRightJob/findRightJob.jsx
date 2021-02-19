import React, { useRef, useEffect } from 'react';
import GuidanceRecommendations from '../UserGuidance/Guidance/guidanceRecommendations';
import FindJob from './FindJob/findJob';
import FindJobEdit from './FindJob/findJobEdit';
import JobsUpskills from './JobsUpskills/jobsUpskills';


const FindRightJob = (props) => {
    return (
        <div>
            <GuidanceRecommendations />
            {/* <FindJob /> */}
            {/* <FindJobEdit /> */}
            {/* <JobsUpskills /> */}
        </div>
    )
}

export default FindRightJob;