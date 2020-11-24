import React from 'react';
import WhoLearn from './WhoLearn/whoLearn';
import SkillGain from './SkillGain/skillGain';
import WriteMyResume from './WriteMyResume/writeMyResume';
import OtherSkills from './OtherSkills/otherSkills';
import DomainJobs from './DomainJobs/domainJobs';


const SkillPage = (props) => {
    return(
        <div>
            <WhoLearn />
            <SkillGain />
            <WriteMyResume />
            <OtherSkills />
            <DomainJobs />
            
        </div>
    )
}

export default SkillPage;