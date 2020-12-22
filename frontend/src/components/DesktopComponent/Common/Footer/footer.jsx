import React, { useEffect} from 'react';
import { Link } from 'react-router-dom';
import { siteDomain } from 'utils/domains';
import './footer.scss';
import { useDispatch, useSelector } from 'react-redux';
import { fetchTrendingCnA } from 'store/Footer/actions/index';

const Footer = (props) => {

    const dispatch = useDispatch()
    const { trendingSkills, trendingCourses } = useSelector( store => store.footer )

    useEffect(() => {
        dispatch(fetchTrendingCnA())
    },[])

    return(
        <section className="container-fluid" data-aos="fade-up">
            <footer className="row">
                <div className="container">
                    <div className="footer">
                        <ul className="footer-bdr">
                            <li>
                                <a href={`${siteDomain}/about-us`}>About Us</a>&nbsp;&nbsp;
                            </li>
                            <li>
                            <a href={`${siteDomain}/privacy-policy`}>Privacy Policy</a>&nbsp;&nbsp;
                            </li>
                            <li>
                            <a href={`${siteDomain}/tnc`}>Terms & Conditions</a>&nbsp;&nbsp;
                            </li>
                            <li>
                            <a href={`${siteDomain}/contact-us`}>Contact Us</a>&nbsp;&nbsp;
                            </li>
                            <li>
                            <a href={`${siteDomain}/disclaimer`}>Disclaimer</a>&nbsp;&nbsp;
                            </li>
                            <li className="social-icon">
                                <a href="https://www.facebook.com/shinelearningdotcom/" className="icon-facebook"></a>
                                <a  href="https://www.linkedin.com/showcase/13203963/" className="icon-linkedin"></a>
                                <a href="https://twitter.com/shinelearning" className="icon-twitter"></a>
                            </li>
                        </ul>
                        <article className="">
                            <strong>TRENDING  COURSES</strong>
                            {
                                trendingCourses?.slice(0,25).map((course, index) => {
                                    return (
                                        <React.Fragment key={index}>
                                            <a href={`${siteDomain}${course.url}`}>{course.name}</a>&nbsp;
                                            { trendingCourses.length - 1 === index ? '' : '|'}
                                        </React.Fragment>
                                    )
                                })
                            }
                        </article>
                        <article className="">
                            <strong>TRENDING  Skills</strong>
                            {
                                trendingSkills?.slice(0,25).map((skill, index) => {
                                    return (
                                        <React.Fragment key={index}>
                                            <a href={`${siteDomain}${skill.skillUrl}`}>{skill.skillName}</a>&nbsp;
                                            { trendingSkills.length - 1 === index ? '' : '|'}
                                        </React.Fragment>
                                    )
                                })
                            }
                        </article>
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
                                Copyright © 2019 HT Media Limited.
                            </div>
                        </div>
                    </div>
                </div>
            </footer>
        </section>
    )
}

export default Footer;