import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import Button from 'react-bootstrap/Button';
import '../../../SkillPage/CoursesTray/courses.scss'
import './jobsUpskills.scss';
import { useSelector } from 'react-redux';
import { fetchFindRightJobsData } from 'store/UserIntentPage/actions';
import { useDispatch } from 'react-redux';

const JobsUpskills = (props) => {
    const [key, setKey] = useState('categories1');
    const dispatch = useDispatch();

    const findJobsData = useSelector(store => store.findRightJob.jobsList); 

    if(!findJobsData?.results) {
        const params = new URLSearchParams(props.location.search);

        const data = {
            'job': params.get('job_title'),
            'location': params.get('loc'), //Is document work on SSR?
            'skills': params.get('skill'),
            'experience': params.get('minexp')
        };
        new Promise((resolve) => dispatch(fetchFindRightJobsData({ data, resolve })));
    }

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
                <div className="m-jobs-upskills mt-20">
                    <div class="m-tabset-intent">
                        <input type="radio" name="tabset" id="tab1" aria-controls="Jobs for you" checked />
                        <label for="tab1">Jobs for you</label>

                        <input type="radio" name="tabset" id="tab2" aria-controls="Upskill yourself" />
                        <label for="tab2">Upskill yourself</label>

                        <div class="tab-panels">
                            <div id="tab1" class="tab-panel">
                                <ul className="m-shine-courses-listing mt-20">
                                    {findJobsData?.results?.map((jData,indx) => {
                                        return(
                                            <li>
                                                <div className="course">
                                                    <div className="d-flex p-15">
                                                        <div className="course__content">
                                                            <span className="hot-badge">
                                                                <figure className="icon-hot"></figure> Hot
                                                            </span>
                                                            <h3 className="heading3">
                                                                <Link to={"#"}>{jData.jJT}</Link>
                                                            </h3>
                                                            <strong>{jData.jCName}</strong>
                                                            <div className="d-flex">
                                                                <ul>
                                                                    <li>{jData.jExp}</li>
                                                                    <li>{jData.jLoc.join(',')}</li>
                                                                    <li>{jData.jKwd}</li>
                                                                </ul>
                                                                <div className="m-price-date">
                                                                    <Link to={"#"} class="btn-blue-outline mb-10">Apply</Link>
                                                                    <span>{jData.jPDate}</span> 
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        )
                                    })}
                                    {/* <li>
                                        <div className="course">
                                            <div className="d-flex p-15">
                                                <div className="course__content">
                                                    <span className="hot-badge">
                                                        <figure className="icon-hot"></figure> Hot
                                                    </span>
                                                    <h3 className="heading3">
                                                        <Link to={"#"}>UI UX Designer Web,HTML5,CSS3,Adobe suite, Sketch, Invision</Link>
                                                    </h3>
                                                    <strong>eInfochips</strong>
                                                    <div className="d-flex">
                                                        <ul>
                                                            <li>2 - 4 Years </li>
                                                            <li>Gurgaon</li>
                                                            <li>Java, Hibernate, Hadoop</li>
                                                        </ul>
                                                        <div className="m-price-date">
                                                            <Link to={"#"} class="btn-blue-outline mb-10">Apply</Link>
                                                            <span>Dec 18, 2020</span> 
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </li> */}
                                    {/* <li>
                                        <div className="course">
                                            <div className="d-flex p-15">
                                                <div className="course__content">
                                                    <span className="hot-badge">
                                                        <figure className="icon-hot"></figure> Hot
                                                    </span>
                                                    <h3 className="heading3">
                                                        <Link to={"#"}>UI UX Designer Web,HTML5,CSS3,Adobe suite, Sketch, Invision</Link>
                                                    </h3>
                                                    <strong>eInfochips</strong>
                                                    <div className="d-flex">
                                                        <ul>
                                                            <li>2 - 4 Years </li>
                                                            <li>Gurgaon</li>
                                                            <li>Java, Hibernate, Hadoop</li>
                                                        </ul>
                                                        <div className="m-price-date">
                                                            <Link to={"#"} class="btn-blue-outline mb-10">Apply</Link>
                                                            <span>Dec 18, 2020</span> 
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </li> */}
                                </ul>
                                    
                            </div>
                            <div id="tab2" class="tab-panel">
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
                        </div>
                    </div>
                </div>
                <div className="m-courses-feedback">
                    <strong>Are these courses recommendation relevant to your profile?</strong>
                    <span className="mt-15">
                        <Link className="btn-blue-outline">Yes</Link>
                        <Link className="btn-blue-outline">No</Link>
                    </span>
                </div>
            </div>
        </section>
    )
}

export default JobsUpskills;