import React, { useRef, useEffect } from 'react';
import FindJob from './FindJob/findJob';
import FindJobEdit from './FindJob/findJobEdit';
import JobsUpskills from './JobsUpskills/jobsUpskills';


const FindRightJob = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job')

    return (
        <div>
            { !!job ? <JobsUpskills /> : <FindJob type={"job"} {...props}/> }
        </div>
    )
}

export default FindRightJob;