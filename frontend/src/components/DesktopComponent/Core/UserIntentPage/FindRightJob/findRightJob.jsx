import React, { useRef, useEffect } from 'react';
import UIBanner from '../../../Common/UIBanner/UIbanner';
import FindJob from './FindJob/findJob';
import JobsUpskills from './JobsUpskills/jobsUpskills';
import FindJobEdit from './FindJob/findJobEdit';


const FindRightJob = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job')

    return (
        <div>
            <UIBanner {...props} />
            { !!job ? <JobsUpskills /> : <FindJob type={"job"} {...props}/> }
        </div>
    )
}

export default FindRightJob;