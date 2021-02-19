import React, { useEffect } from 'react';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import UIBanner from './FindRightJob/UIBanner/UIbanner'
import UIBanner1 from './FindRightJob/UIBanner/UIbanner1'
import FindRightJob from './FindRightJob/findRightJob';
import MakeCareerChange from './MakeCareerChange/makeCareerChange';
import UserGuidance from './UserGuidance/UserGuidance';
import ImproveProfile from './ImproveProfile/improveProfile';
import ProgressCareer from './ProgressCareer/progressCareer';
import './userIntentPage.scss';
import Footer from '../../Common/Footer/Footer';
import Aos from "aos";
import "aos/dist/aos.css";
import { Helmet } from 'react-helmet';

const UserIntentPage = (props) => {
    const { history } = props;
    const UIContainer = props.match.params.name;
    const UserIntentRoutes = [undefined, 'find-right-job', 'make-career-change', 'improve-profile', 'progress-career']

    useEffect(() => {
        if (!UserIntentRoutes.includes(UIContainer)) {
            history.push('/404');
        }
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [UIContainer])

    return (
        <div>
            <Helmet>
                <title>
                    {
                        {
                            'find-right-job': 'Find the right job | Shine Learning',
                            undefined: 'Career Guidance personalized recommendations | Shine Learning',
                            'make-career-change': 'Make a career change | Shine Learning',
                            'improve-profile': 'Improve your profile | Shine Learning',
                            'progress-career': 'Progress your career | Shine Learning'
                        }[UIContainer]
                    }
                </title>
            </Helmet>
            <MenuNav />
            <header className="m-container m-header">
                <Header />
            
                {/* <UIBanner1 /> */}
            </header>
            <main className="mb-0">
                {
                    {
                        'find-right-job': <FindRightJob icon="icon-ui2" title="Find the right job" back={true} {...props} />,
                        'make-career-change': <MakeCareerChange icon="icon-ui2" title="Make a career change" back={true} {...props} />,
                        'improve-profile': <ImproveProfile icon="icon-ui2" title="Improve your profile" back={true} />,
                        'progress-career': <ProgressCareer icon="icon-ui2" title="Progress your career" back={true} {...props} />,
                        undefined: <UserGuidance icon="icon-ui1" title="Career Guidance with personalized recommendations" back={false} />
                    }[UIContainer]
                }
            </main>
            <Footer />
        </div>
    )
}

export default UserIntentPage;