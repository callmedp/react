import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import Button from 'react-bootstrap/Button';
import '../../../SkillPage/CoursesTray/courses.scss'
import '../../FindRightJob/JobsUpskills/jobsUpskills.scss';


const FeedbackResult = (props) => {
    const [key, setKey] = useState('categories1');
    return (
        <section className="m-container mt-0 mb-0 pl-0 pr-0">
            <div className="m-ui-main col">
                <div className="d-flex align-items-center">
                    <div className="m-ui-steps">
                        <Link className="m-completed" to={"#"}>1</Link>
                        <Link className="m-completed" to={"#"}>2</Link>
                        <Link className="m-current" to={"#"}>3</Link>
                    </div>
                    <Link className="btn-blue-outline m-back-goal-btn" to={"/user-intent/"}>Back to goal</Link>
                </div>
                <h2 className="m-heading3 mt-20">Here’s how you can make a new career</h2>
                <div className="m-jobs-upskills mt-20">
                    <div className="m-courses mt-20">
                        <div className="m-card">
                            <div className="m-card__heading">
                                <figure>
                                    <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                </figure>
                                <h3 className="m-heading3">
                                    <Link to={"#"}>Digital Marketing Training Course Programme</Link>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating">
                                <span className="mr-10">By ERB</span>
                                <span className="m-rating">
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-blankstar"></em>
                                    <span>4/5</span>
                                </span>
                                </div>
                                <div className="m-card__duration-mode">
                                    Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong> <span className="d-block"><strong>2819</strong> Jobs available</span>
                                </div>
                                <div className="m-card__price">
                                    <strong>12999/-</strong> 
                                    <Link to={"#"} className="m-view-more">View more</Link>
                                </div>
                            </div>
                        </div>
                        <div className="m-card">
                            <div className="m-card__heading">
                                <figure>
                                    <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                </figure>
                                <h3 className="m-heading3">
                                    <Link to={"#"}>Email Marketing Master Training Course</Link>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating">
                                <span className="mr-10">By ERB</span>
                                <span className="m-rating">
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-blankstar"></em>
                                    <span>4/5</span>
                                </span>
                                </div>
                                <div className="m-card__duration-mode">
                                    Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong> <span className="d-block"><strong>2819</strong> Jobs available</span>
                                </div>
                                <div className="m-card__price">
                                    <strong>12999/-</strong> 
                                </div>
                            </div>
                            <div className="m-card__popover">
                                <p className="m-type">Type: <strong>Certification</strong>  |   <strong>Course level:</strong> Intermediate 
                                    <strong> 2819</strong> Jobs available
                                </p>
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
                                <p className="d-flex align-items-center">
                                    <button type="submit" className="btn-yellow" role="button">Enroll now</button>
                                    <Link to={"#"} className="micon-pdf ml-auto"></Link>
                                </p>
                                <Link to={"#"} className="m-view-less d-block text-right">View less</Link>
                            </div>
                        </div>
                        <div className="m-card">
                            <div className="m-card__heading">
                                <figure>
                                    <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                </figure>
                                <h3 className="m-heading3">
                                    <Link to={"#"}>Digital Marketing Training Course Programme</Link>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating">
                                <span className="mr-10">By ERB</span>
                                <span className="m-rating">
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-blankstar"></em>
                                    <span>4/5</span>
                                </span>
                                </div>
                                <div className="m-card__duration-mode">
                                    Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong> <span className="d-block"><strong>2819</strong> Jobs available</span>
                                </div>
                                <div className="m-card__price">
                                    <strong>12999/-</strong> 
                                    <Link to={"#"} className="m-view-more">View more</Link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="m-courses-feedback">
                    <strong>Thanks for your feedback!</strong>
                </div>
            </div>
        </section>
    )
}

export default FeedbackResult;