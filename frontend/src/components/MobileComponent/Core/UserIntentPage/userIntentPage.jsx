import React, { useEffect, useState } from 'react';
import MenuNav from '../../Common/MenuNav/menuNav';
import Header from '../../Common/Header/Header';
import FindRightJob from './FindRightJob/findRightJob';
import MakeCareerChange from './MakeCareerChange/makeCareerChange';
import UserGuidance from './UserGuidance/UserGuidance';
import ImproveProfile from './ImproveProfile/improveProfile';
import ProgressCareer from './ProgressCareer/progressCareer';
import UIBanner from '../../Common/UIBanner/UIbanner';
import SearchPage from '../../Common/SearchPage/SearchPage';
import './userIntentPage.scss';
import { useDispatch, useSelector } from 'react-redux';
import Footer from '../../Common/Footer/Footer';
import Aos from "aos";
import CTA from '../../Common/CTA/CTA';
import EnquiryModal from '../../Common/Modals/EnquiryModal';

// import "aos/dist/aos.css";
import { Helmet } from 'react-helmet';

const UserIntentPage = (props) => {
    const { history } = props;
    const UIContainer = props.match.params.name;
    const [showSearchPage, setShowSearchPage] = useState(false);
    const [enquiryForm, setEnquiryForm] = useState(false);
    const { name } = useSelector(store => store.skillBanner);
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
            { showSearchPage ? <SearchPage setShowSearchPage={setShowSearchPage} /> :
                <>
                    <MenuNav />
                    <header className="m-container m-header">
                        <Header setShowSearchPage={setShowSearchPage} />
                        {
                            {
                                'find-right-job': <UIBanner heading={'Find the <strong> right job </strong>'} />,
                                undefined: <UIBanner heading={'<strong>Career Guidance</strong> with personalized recommendations'} />,
                                'make-career-change': <UIBanner heading={'Make a <strong> career change </strong>'} />,
                                'improve-profile': <UIBanner heading={'<strong> Improve your</strong> profile'} />,
                                'progress-career': <UIBanner heading={'<strong> Progress your</strong> career'} />
                            }[UIContainer]
                        }

                        {/* <UIBanner heading={headingTitle} /> */}
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
                    <br/><br/>
                    <CTA setEnquiryForm={setEnquiryForm} pageType='userintent' heading={name} />
                    {
                        enquiryForm ? <EnquiryModal setEnquiryForm={setEnquiryForm} /> : null
                    }
                </>
            }
        </div>
    )
}

export default UserIntentPage;