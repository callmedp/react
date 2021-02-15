import React, { useRef, useEffect } from 'react';
import Header from '../../Common/Header/header';
import FindRightJob from './FindRightJob/findRightJob';
import MakeCareerChange from './MakeCareerChange/makeCareerChange';
import UserGuidance from './UserGuidance/UserGuidance';
import ImproveProfile from './ImproveProfile/improveProfile';
import ProgressCareer from './ProgressCareer/progressCareer';
import Footer from '../../Common/Footer/footer';
import './userIntentPage.scss';
import Aos from "aos";
import "aos/dist/aos.css";
import { Helmet } from 'react-helmet';

const UserIntentPage = (props) => {
    const { history } = props;
    const UIContainer = props.match.params.name;
    const userIntentRoutes = [undefined, 'find-right-job', 'make-career-change', 'improve-profile', 'progress-career']

    useEffect(() => {
        if (!userIntentRoutes.includes(UIContainer)) {
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
                            undefined: 'Career Guidance with personalized recommendations | Shine Learning',
                            'make-career-change': 'Make a career change | Shine Learning',
                            'improve-profile': 'Improve your profile | Shine Learning',
                            'progress-career': 'Progress your career | Shine Learning'
                        }[UIContainer]
                    }
                </title>
            </Helmet>
            <Header />
            <main>
                {
                    {
                        'find-right-job': <FindRightJob icon="icon-ui2" title="Find the right job" back={true}/>,
                        'make-career-change': <MakeCareerChange icon="icon-ui2" title="Make a career change" back={true}/>,
                        'improve-profile': <ImproveProfile icon="icon-ui2" title="Improve your profile" back={true}/>,
                        'progress-career': <ProgressCareer icon="icon-ui2" title="Progress your career" back={true}/>,
                        undefined: <UserGuidance icon="icon-ui1" title="Career Guidance with personalized recommendations" back={false}/>
                    }[UIContainer]
                }
            </main>
            <Footer />
        </div>
    )
}

export default UserIntentPage;