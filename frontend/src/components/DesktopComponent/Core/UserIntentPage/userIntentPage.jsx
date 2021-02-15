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
import { Helmet } from 'react-helmet';

const UserIntentPage = (props) => {
    const { history } = props;
    const dbContainer = props.match.params.name;
    const userIntentRoutes = [undefined, 'find-right-job', 'make-career-change', 'improve-profile', 'progress-career']

    useEffect(() => {
        if (!userIntentRoutes.includes(dbContainer)) {
            history.push('/404');
        }

        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
    }, [dbContainer])

    return (
        <div>
            <Helmet>
                <title>
                    {
                        {
                            'find-right-job': 'Find the right job | Shine Learning',
                            undefined: 'Find the right job | Shine Learning',
                            'make-career-change': 'Make a career change | Shine Learning',
                            'improve-profile': 'Improve your profile | Shine Learning',
                            'progress-career': 'Progress your career | Shine Learning'
                        }[dbContainer]
                    }
                </title>
            </Helmet>
            <Header />
            <main>
                {
                    {
                        'find-right-job': <FindRightJob title="Find the right job" back={false}/>,
                        'make-career-change': <MakeCareerChange title="Make a career change" back={true}/>,
                        'improve-profile': <ImproveProfile title="Improve your profile" back={true}/>,
                        'progress-career': <ProgressCareer title="Progress your career" back={true}/>,
                        undefined: <FindRightJob title="Find the right job" back={false} />
                    }[dbContainer]
                }
            </main>
            <Footer />
        </div>
    )
}

export default UserIntentPage;