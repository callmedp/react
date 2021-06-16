import React, { useEffect} from 'react';
// import { Link } from 'react-router-dom';
import { siteDomain } from 'utils/domains';
import './footer.scss';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTrendingCnA } from 'store/Footer/actions/index';
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';

const Footer = (props) => {

    const dispatch = useDispatch()
    const { trendingSkills, trendingCourses } = useSelector( store => store.footer )
    const sendLearningTracking = useLearningTracking();

    useEffect(() => {
        dispatch(fetchTrendingCnA({ ...props, numCourses:8 }))
    },[])

    const footerTracking = (title, ln_title, event_clicked, name, val, val1, val2, indx) => {
        let name_joined = name.replace(/ /g, '_');
        MyGA.SendEvent(title, ln_title, event_clicked, name_joined, val, val1, val2);

        sendLearningTracking({
            productId: '',
            event: `homepage_footer_${name_joined}_clicked`,
            pageTitle:`homepage`,
            sectionPlacement:'footer',
            eventCategory: `${name_joined}_${indx}`,
            eventLabel: name_joined,
            eventAction: 'click',
            algo: '',
            rank: indx,
        })
    }

    return(
        <section className="container-fluid">
            <footer className="row">
                <div className="container">
                    <div className="footer">
                        <ul className="footer-bdr">
                            <li>
                                <a href={`${siteDomain}/about-us`} onClick={() => footerTracking('homepage_footer','ln_homepage_footer', 'ln_homepage_footer_clicked', 'About Us','', false, true)}>About Us</a>&nbsp;&nbsp;
                            </li>
                            <li>
                            <a href={`${siteDomain}/privacy-policy`} onClick={() => footerTracking('homepage_footer','ln_homepage_footer', 'ln_homepage_footer_clicked', 'Privacy Policy','', false, true)}>Privacy Policy</a>&nbsp;&nbsp;
                            </li>
                            <li>
                            <a href={`${siteDomain}/tnc`} onClick={() => footerTracking('homepage_footer','ln_homepage_footer', 'ln_homepage_footer_clicked', 'Terms & Conditions','', false, true)}>Terms & Conditions</a>&nbsp;&nbsp;
                            </li>
                            <li>
                            <a href={`${siteDomain}/contact-us`} onClick={() =>  footerTracking('homepage_footer','ln_homepage_footer', 'ln_homepage_footer_clicked', 'Contact Us','', false, true)}>Contact Us</a>&nbsp;&nbsp;
                            </li>
                            <li>
                            <a href={`${siteDomain}/disclaimer`} onClick={() =>  footerTracking('homepage_footer','ln_homepage_footer', 'ln_homepage_footer_clicked', 'Disclaimer','', false, true)}>Disclaimer</a>&nbsp;&nbsp;
                            </li>
                            <li className="social-icon">
                                <a href="https://www.facebook.com/shinelearningdotcom/" className="icon-facebook mt-0" onClick={() =>  footerTracking('ln_new_homepage','ln_social_sign_in', 'ln_social_sign_in', 'facebook','', false, true)}></a>
                                <a  href="https://in.linkedin.com/company/shinelearning" className="icon-linkedin" onClick={() =>  footerTracking('ln_new_homepage','ln_social_sign_in', 'ln_social_sign_in', 'linkedin','', false, true)}></a>
                                <a href="https://twitter.com/shinelearning" className="icon-twitter mt-5" onClick={() =>  footerTracking('ln_new_homepage','ln_social_sign_in', 'ln_social_sign_in', 'twitter','', false, true)}></a>
                            </li>
                        </ul>
                        {
                            trendingCourses.length ?
                                <article className="">
                                    <strong>TRENDING  COURSES</strong>
                                    {
                                        trendingCourses.slice(0,25)?.map((course, index) => {
                                            return (
                                                <React.Fragment key={index}>
                                                    <a href={`${siteDomain}${course.url}`} onClick={() => footerTracking('ln_new_homepage','ln_trending_course', 'ln_click_course',course.name, '',false, true, index)}>{course.name}</a>&nbsp;
                                                    { trendingCourses.length - 1 === index ? '' : '|'}
                                                </React.Fragment>
                                            )
                                        })
                                    }
                                </article> : ''
                        }
                        {
                            trendingSkills.length ? 
                                <article className="">
                                    <strong>TRENDING  Skills</strong>
                                    {
                                        trendingSkills.slice(0,25)?.map((skill, index) => {
                                            return (
                                                <React.Fragment key={index} >
                                                    <a href={`${siteDomain}${skill.skillUrl}`} onClick={() => footerTracking('ln_new_homepage','ln_trending_skill', 'ln_click_skill',skill.skillName, '',false, true, index)}>{skill.skillName}</a>&nbsp;
                                                    { trendingSkills.length - 1 === index ? '' : '|'}
                                                </React.Fragment>
                                            )
                                        })
                                    }
                                </article> : ''
                        }

                        <div className="footer-btm">
                            <div className="footer-btm__secure-payment">
                                <figure className="icon-secure"></figure>
                                <p>
                                    <strong>100% Secure Payment</strong>
                                    All major credit & debit cards accepted
                                </p>
                            </div>
                            <div className="footer-btm__payment-option">
                                Payment options
                                <figure className="icon-payment"></figure>
                            </div>
                            <div className="footer-btm__copyright">
                                Copyright © { new Date().getFullYear()} HT Media Limited.
                            </div>
                        </div>
                    </div>
                </div>
            </footer>
        </section>
    )
}

export default Footer;