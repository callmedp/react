import React, {useState} from 'react';
import { Link } from 'react-router-dom';
import { Tabs, Tab, CarouselItem } from 'react-bootstrap';
import Button from 'react-bootstrap/Button';
import '../../../SkillPage/CoursesTray/coursesTray.scss';
import './jobsUpskills.scss';


const JobsUpskills = (props) => {
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
                            <Tabs
                            id="controlled-tab-example"
                            activeKey={key}
                            onSelect={(k) => setKey(k)}
                            className="jobs-upskills"
                            >
                    
                                <Tab eventKey="categories1" title={<h2>Jobs for you</h2>}>
                                    <ul className="shine-courses-listing ml-10n mt-30">
                                        <li className="col">
                                            <div className="course">
                                                <div className="d-flex p-20">
                                                    <div className="course__content">
                                                        <span className="hot-badge">
                                                            <figure className="icon-hot"></figure> Hot
                                                        </span>
                                                        <h3 className="heading3">
                                                            <Link to={"#"}>UI UX Designer Web,HTML5,CSS3,Adobe suite, Sketch, Invision</Link>
                                                        </h3>
                                                        <strong>eInfochips</strong>

                                                        <ul>
                                                            <li>2 - 4 Years </li>
                                                            <li>Gurgaon</li>
                                                        </ul>

                                                        <p className="mt-10">Prospects Should Build stunning UI / UX experience in our products that will enable in get more customer engagement. Identify blockers in the current user experience and provide a better</p>
                                                    </div>
                                                    <div className="course__price-date">
                                                        <span>Dec 18, 2020</span> 
                                                        <Link to={"#"} class="btn btn-secondary mt-10">Apply now</Link>
                                                    </div>
                                                    
                                                </div>
                                                <div className="course__bottom">
                                                    <strong>Skills: </strong>
                                                    <ul>
                                                        <li>adobe photoshop,</li>
                                                        <li>html,</li>
                                                        <li>jquery,</li>
                                                        <li>research,</li>
                                                        <li>android</li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </li>
                                        <li className="col">
                                            <div className="course">
                                                <div className="d-flex p-20">
                                                    <div className="course__content">
                                                        <h3 className="heading3">
                                                            <Link to={"#"}>UI UX Designer Web,HTML5,CSS3,Adobe suite, Sketch, Invision</Link>
                                                        </h3>
                                                        <strong>eInfochips</strong>

                                                        <ul>
                                                            <li>2 - 4 Years </li>
                                                            <li>Gurgaon</li>
                                                        </ul>

                                                        <p className="mt-10">Prospects Should Build stunning UI / UX experience in our products that will enable in get more customer engagement. Identify blockers in the current user experience and provide a better</p>
                                                    </div>
                                                    <div className="course__price-date">
                                                        <span>Dec 18, 2020</span> 
                                                        <Link to={"#"} class="btn btn-secondary mt-10">Apply now</Link>
                                                    </div>
                                                    
                                                </div>
                                                <div className="course__bottom">
                                                    <strong>Skills: </strong>
                                                    <ul>
                                                        <li>adobe photoshop,</li>
                                                        <li>html,</li>
                                                        <li>jquery,</li>
                                                        <li>research,</li>
                                                        <li>android</li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </li>
                                        <li className="col">
                                            <div className="course">
                                                <div className="d-flex p-20">
                                                    <div className="course__content">
                                                        <span className="hot-badge">
                                                            <figure className="icon-hot"></figure> Hot
                                                        </span>
                                                        <h3 className="heading3">
                                                            <Link to={"#"}>UI UX Designer Web,HTML5,CSS3,Adobe suite, Sketch, Invision</Link>
                                                        </h3>
                                                        <strong>eInfochips</strong>

                                                        <ul>
                                                            <li>2 - 4 Years </li>
                                                            <li>Gurgaon</li>
                                                        </ul>

                                                        <p className="mt-10">Prospects Should Build stunning UI / UX experience in our products that will enable in get more customer engagement. Identify blockers in the current user experience and provide a better</p>
                                                    </div>
                                                    <div className="course__price-date">
                                                        <span>Dec 18, 2020</span> 
                                                        <Link to={"#"} class="btn btn-secondary mt-10">Apply now</Link>
                                                    </div>
                                                    
                                                </div>
                                                <div className="course__bottom">
                                                    <strong>Skills: </strong>
                                                    <ul>
                                                        <li>adobe photoshop,</li>
                                                        <li>html,</li>
                                                        <li>jquery,</li>
                                                        <li>research,</li>
                                                        <li>android</li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </li>
                                        <li className="col">
                                            <div className="course">
                                                <div className="d-flex p-20">
                                                    <div className="course__content">
                                                        <h3 className="heading3">
                                                            <Link to={"#"}>UI UX Designer Web,HTML5,CSS3,Adobe suite, Sketch, Invision</Link>
                                                        </h3>
                                                        <strong>eInfochips</strong>

                                                        <ul>
                                                            <li>2 - 4 Years </li>
                                                            <li>Gurgaon</li>
                                                        </ul>

                                                        <p className="mt-10">Prospects Should Build stunning UI / UX experience in our products that will enable in get more customer engagement. Identify blockers in the current user experience and provide a better</p>
                                                    </div>
                                                    <div className="course__price-date">
                                                        <span>Dec 18, 2020</span> 
                                                        <Link to={"#"} class="btn btn-secondary mt-10">Apply now</Link>
                                                    </div>
                                                    
                                                </div>
                                                <div className="course__bottom">
                                                    <strong>Skills: </strong>
                                                    <ul>
                                                        <li>adobe photoshop,</li>
                                                        <li>html,</li>
                                                        <li>jquery,</li>
                                                        <li>research,</li>
                                                        <li>android</li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </li>
                                    </ul>
                                    <Link to={"#"} className="load-more">View More Jobs</Link>
                                </Tab>
                                <Tab eventKey="categories2" title={<h2>Upskill yourself</h2>}>
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
                                                    <div className="course__price-enrol mr-20 mt-20">
                                                        <strong>12999/-</strong> 
                                                        <Link to={"#"} class="btn btn-secondary mt-10">Enroll now</Link>
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
                                                        <p className="course__duration-mode mt-20 mt-20">
                                                            Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>  |   <strong>2819</strong> Jobs available
                                                        </p>
                                                    </div>
                                                    <div className="course__price-enrol mr-20 mt-20">
                                                        <strong>12999/-</strong> 
                                                        <Link to={"#"} class="btn btn-secondary mt-10">Enroll now</Link>
                                                    </div>
                                                </div>
                                                <div className="course__bottom">
                                                    <div className="d-flex pb-10">
                                                        <strong>Key Highlights</strong>
                                                        <ul>
                                                            <li>Earn a certificate after completion</li>
                                                            <li>Get Access on mobile </li>
                                                        </ul>
                                                        <Link to={"#"} className="more-popover ml-30">Lesser <figure className="icon-arrow-up-sm"></figure></Link>
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
                                                    <div className="course__price-enrol mr-20 mt-20">
                                                        <strong>12999/-</strong> 
                                                        <Link to={"#"} class="btn btn-secondary mt-10">Enroll now</Link>
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
                                </Tab>
                            </Tabs>
                        </div>
                        <div className="courses-feedback mt-50 mr-15p">
                            <strong>Are these courses recommendation relevant to your profile?</strong>
                            <span className="ml-auto">
                                <Button variant="outline-primary">Yes</Button>{' '}
                                <Button variant="outline-primary">No</Button>{' '}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    )
}

export default JobsUpskills;