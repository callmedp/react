import React, {useEffect, useState} from 'react';
import { Link } from 'react-router-dom';
// import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
// import Button from 'react-bootstrap/Button';
import '../../../SkillPage/CoursesTray/courses.scss'
import './jobsUpskills.scss';
import { useSelector } from 'react-redux';
import { fetchFindRightJobsData, fetchUpskillYourselfData } from 'store/UserIntentPage/actions';
import { useDispatch } from 'react-redux';

const JobsUpskills = (props) => {
    // const [key, setKey] = useState('categories1');
    const dispatch = useDispatch();
    const findJobsData = useSelector(store => store.findRightJob.jobsList);
    const {course_data, page, recommended_course_ids} = useSelector(store => store.upskillYourself.upskillList);
    const params = new URLSearchParams(props.location.search);

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+'
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }
    
    useEffect(() => {
        const data = {
            'job': params.get('job_title'),
            'location': params.get('loc'), //Is document work on SSR?
            'skills': params.get('skill'),
            'experience': params.get('minexp')
        };

        const dataUpskill = {
            'preferred_role': params.get('job_title'),
            'skills': params.get('skill'),
            'experience': params.get('minexp')
        };

        new Promise((resolve) => dispatch(fetchFindRightJobsData({ data, resolve })));
        new Promise((resolve) => dispatch(fetchUpskillYourselfData({ dataUpskill, resolve })));
    }, [])

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
                                            <li key={indx}>
                                                <div className="course">
                                                    <div className="d-flex p-15">
                                                        <div className="course__content">
                                                            {/* <span className="hot-badge">
                                                                <figure className="icon-hot"></figure> Hot
                                                            </span> */}
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
                                                                    <Link to={jData.jSlug} class="btn-blue-outline mb-10">Apply</Link>
                                                                    <span>{new Date(jData.jPDate).toLocaleDateString()}</span> 
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        )
                                    })}
                                </ul>
                            </div>
                            <div id="tab2" class="tab-panel">
                                <div className="m-courses mt-20">
                                    {course_data?.map((cour, indx) => {
                                        return (
                                            <div className="m-card">
                                                <div className="m-card__heading">
                                                    <figure>
                                                        <img src={cour.imgUrl} alt={cour.imgAlt} />
                                                    </figure>
                                                    <h3 className="m-heading3">
                                                        <Link to={cour.url}>{cour.name}</Link>
                                                    </h3>
                                                </div>
                                                <div className="m-card__box">
                                                    <div className="m-card__rating">
                                                        <span className="mr-10">By {cour.providerName}</span>
                                                        <span className="m-rating">
                                                            {cour?.stars?.map((star, index) => starRatings(star, index))}
                                                            {/* <em className="micon-fullstar"></em>
                                                            <em className="micon-fullstar"></em>
                                                            <em className="micon-fullstar"></em>
                                                            <em className="micon-fullstar"></em>
                                                            <em className="micon-blankstar"></em> */}
                                                            <span>{cour?.rating}</span>
                                                        </span>
                                                    </div>
                                                    <div className="m-card__duration-mode">
                                                        Duration: <strong>{cour?.duration > 0 ? cour?.duration + ' days' : '' }</strong>  |   Mode: <strong>{cour.mode || ''}</strong> <span className="d-block"><strong>{cour.jobsAvailable > 0 ? cour.jobsAvailable + 'Jobs available' : ''}</strong></span>
                                                    </div>
                                                    <div className="m-card__price">
                                                        <strong>{cour.price}/-</strong> 
                                                        <Link id={'upSk' + cour.id} className="m-view-more">View more</Link>
                                                    </div>
                                                </div>

                                                <div className="m-card__popover" htmlFor={'upSk' + cour.id}>
                                                        <p className="m-type"><strong>{cour?.type ? 'Type: ' + cour.type : ''}</strong>  |   <strong>Course level:</strong> Intermediate 
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
                                        )
                                    })}
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
                                    {/* <div className="m-card">
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
                                    </div> */}
                                    {/* <div className="m-card">
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
                                    </div> */}
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