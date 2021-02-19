import React, { useEffect } from 'react';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import UIBanner from './FindRightJob/UIBanner/UIbanner'
import UIBanner1 from './FindRightJob/UIBanner/UIbanner1'
import FindRightJob from './FindRightJob/findRightJob';
import MakeCareerChange from './MakeCareerChange/makeCareerChange';
import ImproveProfile from './ImproveProfile/improveProfile';
import ProgressCareer from './ProgressCareer/progressCareer';
import './userIntentPage.scss';
import Footer from '../../Common/Footer/Footer';
import Aos from "aos";
import "aos/dist/aos.css";

const UserIntentPage = (props) => {
    useEffect( () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [])
    return (
        <div>
            <MenuNav />
            <header className="m-container m-header">
                <Header />
                {/* <UIBanner /> */}
                <UIBanner1 />
            </header>
            <main className="mb-0">
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