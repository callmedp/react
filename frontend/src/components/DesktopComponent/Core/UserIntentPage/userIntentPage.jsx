import React, { useRef, useEffect } from 'react';
import Header from '../../Common/Header/header';
import FindRightJob from './FindRightJob/findRightJob';
import MakeCareerChange from './MakeCareerChange/makeCareerChange';
import ImproveProfile from './ImproveProfile/improveProfile';
import ProgressCareer from './ProgressCareer/progressCareer';
import Footer from '../../Common/Footer/footer';
import './userIntentPage.scss';
import Aos from "aos";
import "aos/dist/aos.css";

const UserIntentPage = (props) => {
    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])

    return (
        <div>
            <Header />
            <main>
                <FindRightJob />
                {/* <MakeCareerChange /> */}
                {/* <ImproveProfile /> */}
                {/* <ProgressCareer />  */}
            </main>
            <Footer />
        </div>
    )
}

export default UserIntentPage;