import React from 'react';
import SkillBanner from './Banner/banner';
import AboutSection from './AboutSection/aboutSection';
import WhoLearn from './WhoLearn/whoLearn';
import NeedHelp from './NeedHelp/needHelp';
import SkillGain from './SkillGain/skillGain';
import '../SkillPage/skillPage.scss'

const SkillPage = (props) => {
    return (
        <div>
            <SkillBanner/>
            <div className="container">
                <div className="row">
                    <div className="col-sm-9">
                        <div className="ml-5">
                            <AboutSection/>
                            <WhoLearn/>
                        </div>
                    </div>
                    <div className="col-sm-3 right-widget">
                        <NeedHelp />
                    </div>
                </div>
            </div>
            <SkillGain />
        </div>
    )
}

export default SkillPage;