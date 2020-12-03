import React from 'react';
import { Link } from 'react-router-dom';
import './footer.scss';

const Footer = (props) => {
    return(
        <section className="container-fluid">
            <footer className="row">
                <div className="container">
                    <div className="footer">
                        <ul className="footer-bdr">
                            <li>
                                <Link to={"#"}>About Us</Link>
                            </li>
                            <li>
                                <Link to={"#"}>Partners</Link>
                            </li>
                            <li>
                                <Link to={"#"}>Privacy Policy</Link>
                            </li>
                            <li>
                                <Link to={"#"}>Terms & Condition</Link>
                            </li>
                            <li>
                                <Link to={"#"}>Contact us</Link>
                            </li>
                            <li className="social-icon">
                                <Link to={"#"} className="icon-facebook"></Link>
                                <Link to={"#"} className="icon-linkedin"></Link>
                                <Link to={"#"} className="icon-twitter"></Link>
                            </li>
                        </ul>
                        <article className="">
                            <strong>TRENDING  COURSES</strong>
                            <Link to={"#"}>DevOps Certification Training</Link> | <Link to={"#"}>AWS Architect Training</Link> | <Link to={"#"}>Big Data Hadoop</Link> | <Link to={"#"}>Training Tableau Training</Link> | <Link to={"#"}>Python Certification</Link> | <Link to={"#"}>Training for Data Science Selenium Training PMP® Certification</Link> | <Link to={"#"}>Training Robotic Process Automation Training</Link> | <Link to={"#"}>Spark and Scala Certification Training</Link> | <Link to={"#"}>Microsoft Power BI Training</Link> | <Link to={"#"}>Online Java Course Training Python Certification Course</Link> | <Link to={"#"}>Big Data Hadoop Certification Training Course</Link> | <Link to={"#"}>Data Science with Python Training Course</Link> | <Link to={"#"}>Machine Learning Certification Course</Link>
                        </article>
                        <article className="">
                            <strong>TRENDING  Skills</strong>
                            <Link to={"#"}>Big Data Hadoop Certification Training Course</Link> | <Link to={"#"}>Data Science with Python Training Course</Link> | <Link to={"#"}>Machine Learning Certification Course</Link>
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