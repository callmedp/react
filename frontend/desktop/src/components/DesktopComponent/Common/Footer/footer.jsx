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
        <section className="container-fluid">
            <footer className="row">
                <div className="container">
                    <div className="footer">
                        <ul className="footer-bdr">
                            <li>
                                <a href={`${siteDomain}/about-us`}>About Us</a>
                            </li>
                            <li>
                            <a href={`${siteDomain}/privacy-policy`}>Privacy Policy</a>
                            </li>
                            <li>
                            <a href={`${siteDomain}/tnc`}>Terms & Conditions</a>
                            </li>
                            <li>
                            <a href={`${siteDomain}/contact-us`}>Contact Us</a>
                            </li>
                            <li>
                            <a href={`${siteDomain}/disclaimer`}>Disclaimer</a>
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
                                trendingCourses?.map((course, index) => {
                                    return (
                                        <React.Fragment key={index}>
                                            <a href={`${siteDomain}${course.url}`}>{course.name}</a>&nbsp;
                                            { trendingCourses.length - 1 === index ? '' : '|'}
                                        </React.Fragment>
                                    )
                                })
                            }
                            {/* <Link to={"#"}>DevOps Certification Training</Link> | <Link to={"#"}>AWS Architect Training</Link> | <Link to={"#"}>Big Data Hadoop</Link> | <Link to={"#"}>Training Tableau Training</Link> | <Link to={"#"}>Python Certification</Link> | <Link to={"#"}>Training for Data Science Selenium Training PMP® Certification</Link> | <Link to={"#"}>Training Robotic Process Automation Training</Link> | <Link to={"#"}>Spark and Scala Certification Training</Link> | <Link to={"#"}>Microsoft Power BI Training</Link> | <Link to={"#"}>Online Java Course Training Python Certification Course</Link> | <Link to={"#"}>Big Data Hadoop Certification Training Course</Link> | <Link to={"#"}>Data Science with Python Training Course</Link> | <Link to={"#"}>Machine Learning Certification Course</Link> */}
                        </article>
                        <article className="">
                            <strong>TRENDING  Skills</strong>
                            {
                                trendingSkills?.map((skill, index) => {
                                    return (
                                        <React.Fragment key={index}>
                                            <a href={`${siteDomain}${skill.productSlug}`}>{skill.skillName}</a>&nbsp;
                                            { trendingSkills.length - 1 === index ? '' : '|'}
                                        </React.Fragment>
                                    )
                                })
                            }
                            {/* <Link to={"#"}>Big Data Hadoop Certification Training Course</Link> | <Link to={"#"}>Data Science with Python Training Course</Link> | <Link to={"#"}>Machine Learning Certification Course</Link> */}
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