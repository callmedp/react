import React from 'react';
import FindJob from './FindJob/findJob';
import JobsUpskills from './JobsUpskills/jobsUpskills';
import Footer from '../../../Common/Footer/Footer';

const FindRightJob = (props) => {
    const params = new URLSearchParams(props.location.search);
    const job = params.get('job_title');

    return (
        <div>
            { !!job ? <><JobsUpskills {...props} /><Footer /></> : <FindJob type={"job"} {...props}/> }
        </div>
    )
}

export default FindRightJob;