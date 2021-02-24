import React from 'react';
import FindJob from './FindJob/findJob';
import JobsUpskills from './JobsUpskills/jobsUpskills';

const FindRightJob = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job_title');

    return (
        <div>
            { !!job ? <JobsUpskills {...props} /> : <FindJob type={"job"} {...props}/> }
        </div>
    )
}

export default FindRightJob;