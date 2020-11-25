import React, { useEffect } from 'react';
import WhoLearn from './WhoLearn/whoLearn';
import SkillGain from './SkillGain/skillGain';
import WriteMyResume from './WriteMyResume/writeMyResume';
import OtherSkills from './OtherSkills/otherSkills';
import DomainJobs from './DomainJobs/domainJobs';
import { useDispatch } from 'react-redux';
import { fetchSkillPageBanner } from 'store/SkillPage/Banner/actions';


const SkillPage = (props) => {
    const dispatch = useDispatch()
    const pageId = props.match.params.id;
    useEffect(() => {
        dispatch(fetchSkillPageBanner({id : pageId}))
    },[])
    return(
        <div>
            <WhoLearn />
            <SkillGain />
            <WriteMyResume />
            <OtherSkills />
            <DomainJobs pageId={pageId}/>
            
        </div>
    )
}

export default SkillPage;