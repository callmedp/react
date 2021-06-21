import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import { Tabs, Tab, CarouselItem } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import '../../../SkillPage/CoursesTray/coursesTray.scss';
import './viewCourses.scss';


const FeedbackResult = (props) => {
    const [key, setKey] = useState('categories1');
    return (
        <section className="container-fluid mt-30n mb-0">
            <div className="row">
                <div className="container">
                    <div className="ui-main col">
                        <div className="ui-steps">
                            <Link className="completed" to={"#"}>1</Link>
                            <Link className="completed" to={"#"}>2</Link>
                            <Link className="current" to={"#"}>3</Link>
                        </div>
                        
                        <div className="jobs-upskills courses-tray mt-20 mr-15p">
                            <h2 className="heading3">Here’s how you can make a new career</h2>
                            <ul className="courses-listing ml-10n mt-30">
                                <li className="col">
                                    <div className="course">
                                        <div className="d-flex align-items-center">
                                            <figure className="course__icon">
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <div className="course__content">
                                                <span className="flag-red">BESTSELLER</span>
                                                <h3 className="heading3">
                                                    <Link to={"#"}>Digital Marketing Training Course</Link>
                                                </h3>
                                                <span className="mr-10">By ERB</span>
                                                <span className="rating">
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-blankstar"></em>
                                                    <span className="ml-10">4/5</span>
                                                </span>
                                                <p className="course__duration-mode mt-20">
                                                    Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>  |   <strong>2819</strong> Jobs available
                                                </p>
                                            </div>
                                            <div className="course__price-enrol mr-20">
                                                <strong>12999/-</strong> 
                                                <Link to={"#"} className="btn btn-secondary mt-10">Buy now</Link>
                                            </div>
                                        </div>
                                        <div className="course__bottom">
                                            <div className="d-flex">
                                                <strong>Key Highlights</strong>
                                                <ul>
                                                    <li>Earn a certificate after completion</li>
                                                    <li>Get Access on mobile </li>
                                                </ul>
                                                <Link to={"#"} className="more-popover ml-30">More <figure className="icon-arrow-down-sm"></figure></Link>
                                                <Link to={"#"} className="icon-pdf ml-auto"></Link>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="course">
                                        <div className="d-flex align-items-center">
                                            <figure className="course__icon">
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <div className="course__content">
                                                <span className="flag-blue">NEW</span>
                                                <h3 className="heading3">
                                                    <Link to={"#"}>Digital Marketing Training Course</Link>
                                                </h3>
                                                <span className="mr-10">By ERB</span>
                                                <span className="rating">
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-blankstar"></em>
                                                    <span className="ml-10">4/5</span>
                                                </span>
                                                <p className="course__duration-mode mt-20">
                                                    Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>  |   <strong>2819</strong> Jobs available
                                                </p>
                                            </div>
                                            <div className="course__price-enrol mr-20">
                                                <strong>12999/-</strong> 
                                                <Link to={"#"} className="btn btn-secondary mt-10">Buy now</Link>
                                            </div>
                                        </div>
                                        <div className="course__bottom">
                                            <div className="d-flex pb-10">
                                                <strong>Key Highlights</strong>
                                                <ul>
                                                    <li>Earn a certificate after completion</li>
                                                    <li>Get Access on mobile </li>
                                                </ul>
                                                <Link to={"#"} className="more-popover ml-30">More <figure className="icon-arrow-up-sm"></figure></Link>
                                                <Link to={"#"} className="icon-pdf ml-auto"></Link>
                                            </div>
                                            <div className="course-popover">
                                                <p className="type">Type: <strong>Certification</strong>  |   Course level: <strong>Intermediate</strong></p>
                                                <p>
                                                    <strong>About</strong>
                                                    This Course is intended for professionals and graduates wanting to excel in their chosen areas.
                                                </p>
                                                <p>
                                                    <strong>Skills you gain</strong>
                                                    Content Marketing  |  Email Marketing  |  Adwords Social Media  |  SEO  |  Copywriting  |  Digital Marketing 
                                                </p>
                                                <p>
                                                    <strong>Highlights</strong>
                                                    <ul>
                                                        <li>Anytime and anywhere access</li>
                                                        <li>Become a part of Job centre</li>
                                                        <li>Lifetime course access</li>
                                                        <li>Access to online e-learning</li>
                                                    </ul>
                                                </p>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="course">
                                        <div className="d-flex align-items-center">
                                            <figure className="course__icon">
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <div className="course__content">
                                                <span className="flag-blue">New</span>
                                                <h3 className="heading3">
                                                    <Link to={"#"}>Digital Marketing Training Course</Link>
                                                </h3>
                                                <span className="mr-10">By ERB</span>
                                                <span className="rating">
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-fullstar"></em>
                                                    <em className="icon-blankstar"></em>
                                                    <span className="ml-10">4/5</span>
                                                </span>
                                                <p className="course__duration-mode mt-20">
                                                    Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>  |   <strong>2819</strong> Jobs available
                                                </p>
                                            </div>
                                            <div className="course__price-enrol mr-20">
                                                <strong>12999/-</strong> 
                                                <Link to={"#"} className="btn btn-secondary mt-10">Buy now</Link>
                                            </div>
                                        </div>
                                        <div className="course__bottom">
                                            <div className="d-flex">
                                                <strong>Key Highlights</strong>
                                                <ul>
                                                    <li>Earn a certificate after completion</li>
                                                    <li>Get Access on mobile </li>
                                                </ul>
                                                <Link to={"#"} className="more-popover ml-30">More <figure className="icon-arrow-down-sm"></figure></Link>
                                                <Link to={"#"} className="icon-pdf ml-auto"></Link>
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                            <Link to={"#"} className="load-more">View More Courses</Link>
                        </div>
                        <div className="courses-feedback mt-50 mr-15p">
                            <strong>Thanks for your feedback!</strong>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default FeedbackResult;