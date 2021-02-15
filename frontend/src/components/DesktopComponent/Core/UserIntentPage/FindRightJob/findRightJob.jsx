import React, { useRef, useEffect } from 'react';
import UIBanner from '../../../Common/UIBanner/UIbanner';
import FindJob from './FindJob/findJob';
import JobsUpskills from './JobsUpskills/jobsUpskills';


const FindRightJob = (props) => {
    const params = new URLSearchParams(window.location.search);
    const job = params.get('job')

    return (
        <div>
            <UIBanner {...props} />
            { job === null ? <FindJob /> : <JobsUpskills /> }
        </div>
    )
}

export default FindRightJob;