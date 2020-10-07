import React from 'react';
import Header from '../../Common/Header/header';
import Banner from './Banner/banner';
import ResumeDetail from './ResumeDetail/resume-detail';
import ImproveResumeScore from './ImproveResumeScore/improveResumeScore';
import GetExpertHelp from './GetExpertHelp/getExpertHelp';
import CallToActionScore from './CallToAction/callToActionScore';
import Footer from '../../Common/Footer/footer';



export default function Score(){
    return (

        <div className="body-wrapper">
            {
                <div className="h-100">
                   <Header page = 'scorePage'/>
                   <Banner/>
                   <ResumeDetail/>
                   <ImproveResumeScore/>
                   <GetExpertHelp/>
                   <CallToActionScore/>
                   <Footer/>
                </div>
            }
    </div>
    );
}