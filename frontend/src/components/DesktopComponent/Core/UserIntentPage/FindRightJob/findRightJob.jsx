import React, { useRef, useEffect } from 'react';
import UIBanner from './UIBanner/UIbanner';
import UIBanner1 from './UIBanner/UIbanner1';
import GuidanceRecommendations from './GuidanceRecommendations/guidanceRecommendations';
import FindJob from './FindJob/findJob';
import FindJobEdit from './FindJob/findJobEdit';
import JobsUpskills from './JobsUpskills/jobsUpskills';


const FindRightJob = (props) => {
    return (
        <div>
            {/* <UIBanner /> */}
            <UIBanner1 />
            <GuidanceRecommendations />
            {/* <FindJob /> */}
            {/* <FindJobEdit /> */}
            {/* <JobsUpskills /> */}
        </div>
    )
}

export default FindRightJob;