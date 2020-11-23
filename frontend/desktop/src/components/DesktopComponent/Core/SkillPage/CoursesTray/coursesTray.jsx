import React, {useState} from 'react';
import './coursesTray.scss';
import { Tabs, Tab } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import Popover from 'react-bootstrap/Popover';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
   
function CoursesTray() {
  const [key, setKey] = useState('courses');
  const popover = (
    <Popover className="courses-popover" id="popover-basic">
      <Popover.Content>
        <p className="type">Type: <strong>Certification</strong>  |   <strong>Course level:</strong> Intermediate 
        <br /><strong>2819</strong> Jobs available
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
        <button type="submit" className="btn btn-inline btn-secondary mx-auto" role="button">Enroll now</button>
      </Popover.Content>
    </Popover>
  );
  return (
    <section className="container" id="courseTr">
        <div className="row"> 
            <div className="col courses-tray">
                <Tabs
                id="controlled-tab-example"
                activeKey={key}
                onSelect={(k) => setKey(k)}
                >
        
                <Tab eventKey="courses" title="Courses">
                    <ul className="courses-tray__list">
                        <li className="col">
                        <OverlayTrigger trigger="hover" placement="right" overlay={popover}>
                            <div className="card">
                                <div className="card__heading">
                                    <span className="flag-blue">NEW</span>
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Digital Marketing Training Course</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                            </OverlayTrigger>
                        </li>
                        <li className="col">
                            <div className="card">
                                <div className="card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Email Marketing Master Training Course</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                        </li>
                        <li className="col">
                            <div className="card">
                                <div className="card__heading">
                                    <span className="flag-red">BESTSELLER</span>
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Digital Marketing Training Course</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                        </li>
                    </ul>
                    <ul className="courses-tray__list">
                        <li className="col">
                        <OverlayTrigger trigger="hover" placement="right" overlay={popover}>
                            <div className="card">
                                <div className="card__heading">
                                    <span className="flag-blue">NEW</span>
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Digital Marketing Training Course</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                            </OverlayTrigger>
                        </li>
                        <li className="col">
                            <div className="card">
                                <div className="card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Email Marketing Master Training Course</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                        </li>
                        <li className="col">
                            <div className="card">
                                <div className="card__heading">
                                    <span className="flag-red">BESTSELLER</span>
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Digital Marketing Training Course</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                        </li>
                    </ul>
                    <Link to={"#"} className="load-more pt-30">Load More Courses</Link>
                </Tab>
                <Tab eventKey="assessments" title="Assessments">
                    <ul className="courses-tray__list">
                        <li className="col">
                        <OverlayTrigger trigger="hover" placement="right" overlay={popover}>
                            <div className="card">
                                <div className="card__heading">
                                    <span className="flag-blue">NEW</span>
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Certified Digital Marketing Master Certification</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                            </OverlayTrigger>
                        </li>
                        <li className="col">
                            <div className="card">
                                <div className="card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Email Marketing Master Training Course</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                        </li>
                        <li className="col">
                            <div className="card">
                                <div className="card__heading">
                                    <span className="flag-red">BESTSELLER</span>
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Digital Marketing Training Course</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                        </li>
                    </ul>
                    <ul className="courses-tray__list">
                        <li className="col">
                        <OverlayTrigger trigger="hover" placement="right" overlay={popover}>
                            <div className="card">
                                <div className="card__heading">
                                    <span className="flag-blue">NEW</span>
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Digital Marketing Training Course</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                            </OverlayTrigger>
                        </li>
                        <li className="col">
                            <div className="card">
                                <div className="card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Email Marketing Master Training Course</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                        </li>
                        <li className="col">
                            <div className="card">
                                <div className="card__heading">
                                    <span className="flag-red">BESTSELLER</span>
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="heading3">
                                        <Link to={"#"}>Digital Marketing Training Course</Link>
                                    </h3>
                                </div>
                                <div className="card__box">
                                    <div className="card__rating mt-5">
                                    <span className="mr-10">By ERB</span>
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="card__duration-mode mt-10">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>
                                    </div>
                                    <div className="card__price mt-30">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="icon-pdf"></Link>
                                    </div>
                                </div>
                            </div>
                        </li>
                    </ul>
                    <Link to={"#"} className="load-more pt-30">Load More Assessments</Link>
                </Tab>
            
                </Tabs>
            </div>
        </div>
    </section>
  );
}
   
export default CoursesTray;