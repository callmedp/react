// React Core Import
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import Aos from "aos";

// Local Import 
import MenuNav from '../../../Common/MenuNav/menuNav';
import Header from '../../../Common/Header/Header';
import Footer from '../../../Common/Footer/Footer';
import '../MyCourses/myCourses.scss'
import './myServices.scss';

// API Import
import { fetchServices } from 'store/DashboardPage/Service/actions/index';


const MyServices = (props) => {
    const dispatch = useDispatch();
    const [showSearchPage, setShowSearchPage] = useState(false)
    const { myServices } = useSelector(store => store.allServices );

    useEffect(() => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
        //You may notice that apis corresponding to these actions are not getting called on initial render.
        //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
        //So there is no need to fetch them again on the browser.
        if (!(window && window.config && window.config.isServerRendered)) {
            new Promise((resolve, reject) => dispatch(fetchServices({ resolve, reject })));
        }
        else {
            //isServerRendered is needed to be deleted because when routing is done through react and not on the node,
            //above actions need to be dispatched.
            delete window.config?.isServerRendered
        }
        console.log(myServices)
    }, [])
    return (
        <div>


            <MenuNav />
            <header className="m-container m-header">
                <Header setShowSearchPage={setShowSearchPage} hideName={true} />

            </header>
            <main className="mb-0">


                <div className="m-courses-detail db-warp">
                    <div className="m-card pl-0">
                        <div className="m-share" aria-haspopup="true">
                            <i className="icon-share"></i>
                            <div className="m-share__box m-arrow-box m-top">
                                <Link to={"#"} className="m-facebook-icon"></Link>
                                <Link to={"#"} className="m-linkedin-icon"></Link>
                                <Link to={"#"} className="m-twitter-iocn"></Link>
                                <Link to={"#"} className="m-whatsup-icon"></Link>
                            </div>
                        </div>

                        <div className="d-flex">
                            <figure>
                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                            </figure>
                            <div className="m-courses-detail__info">
                                <h2>Resume Booster 5-10 years</h2>
                                <p className="m-pipe-divides mb-5">Provider: <strong>Shine learning</strong> </p>
                                <p className="m-pipe-divides mb-5"><span>Bought on: <strong>27 Oct 2020</strong> </span> <span>Duration: <strong>90 days</strong> </span></p>
                            </div>
                        </div>

                        <div className="m-courses-detail--alert mt-15">
                            To initiate your service upload your latest resume
                    </div>

                        <div className="pl-15 mt-15 fs-12">
                            Status: <strong>Upload your resume</strong><Link to={"#"} className="font-weight-bold ml-10">upload</Link>
                            <Link to={"#"} className="d-block font-weight-bold mt-10">View Details</Link>
                        </div>

                        <div className="pl-15">
                            <div className="m-courses-detail__bottomWrap">
                                <div>
                                    <div className="m-day-remaning">
                                        <span className="m-day-remaning--box">9</span>
                                        <span className="m-day-remaning--box">0</span>
                                        <span className="ml-2 m-day-remaning--text">Days <br />remaning</span>
                                    </div>
                                </div>
                            </div>

                            <div className="m-courses-detail__userInput">
                                <Link to="/404" className="m-db-comments font-weight-bold">Add comment</Link>
                                <div className="d-flex">
                                    <span className="">Rate</span>
                                    <span className="m-rating">
                                        <em className="micon-blankstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <em className="micon-blankstar"></em>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>


                    <div className="m-card pl-0">
                        <div className="m-share" aria-haspopup="true">
                            <i className="icon-share"></i>
                            <div className="m-share__box m-arrow-box m-top">
                                <Link to={"#"} className="m-facebook-icon"></Link>
                                <Link to={"#"} className="m-linkedin-icon"></Link>
                                <Link to={"#"} className="m-twitter-iocn"></Link>
                                <Link to={"#"} className="m-whatsup-icon"></Link>
                            </div>
                        </div>

                        <div className="d-flex">
                            <figure>
                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                            </figure>
                            <div className="m-courses-detail__info">
                                <h2>Profile Booster</h2>
                                <p className="m-pipe-divides mb-5">Provider: <strong>Shine learning</strong> </p>
                                <p className="m-pipe-divides mb-5"><span>Bought on: <strong>27 Oct 2020</strong> </span> <span>Duration: <strong>90 days</strong> </span></p>
                            </div>
                        </div>


                        <div className="pl-15 mt-15 fs-12">
                            Status: <strong>Service under progress</strong>
                            <Link to={"#"} className="d-block font-weight-bold mt-10">View Details</Link>
                        </div>

                        <div className="pl-15">
                            <div className="m-courses-detail__bottomWrap">
                                <div>
                                    <div className="m-day-remaning">
                                        <span className="m-day-remaning--box">9</span>
                                        <span className="m-day-remaning--box">0</span>
                                        <span className="ml-2 m-day-remaning--text">Days <br />remaning</span>
                                    </div>
                                </div>

                                <Link to={"#"} className="m-db-start-course font-weight-bold pr-10">Start Service</Link>
                            </div>

                            <div className="m-courses-detail__userInput">
                                <Link to="/404" className="m-db-comments font-weight-bold">Add Comment</Link>
                                <div className="d-flex">
                                    <span className="">Rate</span>
                                    <span className="m-rating">
                                        <em className="micon-blankstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <em className="micon-blankstar"></em>
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div className="m-card pl-0">
                        <div className="m-share" aria-haspopup="true">
                            <i className="icon-share"></i>
                            <div className="m-share__box m-arrow-box m-top">
                                <Link to={"#"} className="m-facebook-icon"></Link>
                                <Link to={"#"} className="m-linkedin-icon"></Link>
                                <Link to={"#"} className="m-twitter-iocn"></Link>
                                <Link to={"#"} className="m-whatsup-icon"></Link>
                            </div>
                        </div>

                        <div className="d-flex">
                            <figure>
                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                            </figure>
                            <div className="m-courses-detail__info">
                                <h2>Linkedin Profile Writing</h2>
                                <p className="m-pipe-divides mb-5">Provider: <strong>Shine learning</strong> </p>
                                <p className="m-pipe-divides mb-5"><span>Bought on: <strong>27 Oct 2020</strong> </span> <span>Duration: <strong>90 days</strong> </span></p>
                            </div>
                        </div>

                        <div className="pl-15 mt-15 fs-12">
                            Status: <strong>Service under progress</strong>
                            <Link to={"#"} className="d-block font-weight-bold mt-10">View Details</Link>
                        </div>

                        <div className="pl-15">
                            <div className="m-courses-detail__bottomWrap">
                                <div>
                                    <div className="m-day-remaning">
                                        <span className="m-day-remaning--box">9</span>
                                        <span className="m-day-remaning--box">0</span>
                                        <span className="ml-2 m-day-remaning--text">Days <br />remaning</span>
                                    </div>
                                </div>

                                <Link to={"#"} className="m-db-start-course font-weight-bold pr-10">Start Service</Link>
                            </div>

                            <div className="m-courses-detail__userInput">
                                <Link to="/404" className="m-db-comments font-weight-bold">3 Comment</Link>
                                <div className="d-flex">
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span className="ml-5">4/5</span>
                                    </span>
                                    <Link to={"#"} className="font-weight-bold ml-10">2</Link>
                                </div>
                            </div>
                        </div>
                    </div>


                    <div className="m-card pl-0">
                        <div className="m-share" aria-haspopup="true">
                            <i className="icon-share"></i>
                            <div className="m-share__box m-arrow-box m-top">
                                <Link to={"#"} className="m-facebook-icon"></Link>
                                <Link to={"#"} className="m-linkedin-icon"></Link>
                                <Link to={"#"} className="m-twitter-iocn"></Link>
                                <Link to={"#"} className="m-whatsup-icon"></Link>
                            </div>
                        </div>

                        <div className="d-flex">
                            <figure>
                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                            </figure>
                            <div className="m-courses-detail__info">
                                <h2>Resume Builder 0-2 years</h2>
                                <p className="m-pipe-divides mb-5">Provider: <strong>Shine learning</strong> </p>
                                <p className="m-pipe-divides mb-5"><span>Bought on: <strong>27 Oct 2020</strong> </span> <span>Duration: <strong>90 days</strong> </span></p>
                            </div>
                        </div>

                        <div className="pl-15 mt-15 fs-12">
                            Status: <Link to={"#"} className="font-weight-bold">Newresume.pdf</Link> <strong> uploaded by Shine</strong>
                            <p className="mt-10 mb-25">
                                <Link className="m-accept" to={"#"}>Accept</Link>
                                <Link className="m-reject" to={"#"}>Reject</Link>
                            </p>
                            <Link to={"#"} className="d-block font-weight-bold mt-10">View Details</Link>
                        </div>

                        <div className="pl-15">
                            <div className="m-courses-detail__bottomWrap">
                                <div>
                                    <div className="m-day-remaning">
                                        <span className="m-day-remaning--box">9</span>
                                        <span className="m-day-remaning--box">0</span>
                                        <span className="ml-2 m-day-remaning--text">Days <br />remaning</span>
                                    </div>
                                </div>

                                <Link to={"#"} className="m-db-start-course font-weight-bold pr-10">Start Service</Link>
                            </div>

                            <div className="m-courses-detail__userInput">
                                <Link to="/404" className="m-db-comments font-weight-bold">3 Comment</Link>
                                <div className="d-flex">
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span className="ml-5">4/5</span>
                                    </span>
                                    <Link to={"#"} className="font-weight-bold ml-10">2</Link>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="m-slide-modal">
                    <div className="text-center" style={{ display: 'none' }}>
                        <span className="m-db-close">&#x2715;</span>
                        <h2 className="mt-15">Get a Better resume by sharing us the feedback for resume</h2>
                        <div className="m-enquire-now mt-15">
                            <div className="m-form-group">
                                <textarea id="addComments" placeholder=" " rows="4"></textarea>
                                <label htmlFor="addComments">Enter feedback here</label>
                            </div>

                            <button className="btn btn-blue">Submit</button>
                        </div>
                    </div>

                    <div className="text-center" style={{ display: 'none' }}>
                        <span className="m-db-close">&#x2715;</span>
                        <h2>Upload Resume</h2>
                        <p>To initiate your services, <strong>upload resume</strong></p>
                        <div className="d-flex align-items-center justify-content-center mt-20">
                            <div className="m-upload-btn-wrapper">
                                <button className="btn btn-blue-outline">Upload a file</button>
                                <input type="file" name="myfile" />
                            </div>

                            <span className="mx-4">Or</span>

                            <div className="m-custom">
                                <input type="checkbox" id="shineResume" />
                                <label className="m-custom--label font-weight-bold mb-0" htmlfor="shineResume">Use shine resume</label>
                            </div>
                        </div>

                        <hr className="my-20" />

                        <div className="m-db-upload-resume">
                            <strong>Select services</strong> for which you want to use this resume
                        <ul className="m-db-upload-resume--list">
                                <li className="m-custom">
                                    <input type="checkbox" id="resumeBooster" />
                                    <label className="font-weight-bold" htmlfor="resumeBooster">Resume Booster 5-10 years</label>
                                </li>

                                <li className="m-custom">
                                    <input type="checkbox" id="resumeBuilder" />
                                    <label className="font-weight-bold" htmlfor="resumeBuilder">Resume Builder 5-10 yrs</label>
                                </li>

                                <li className="m-custom">
                                    <input type="checkbox" id="services" />
                                    <label className="font-weight-bold" htmlfor="services">For all services</label>
                                </li>
                            </ul>
                        </div>

                        <button className="btn btn-primary px-5 mt-30">Save</button>
                    </div>
                </div>
            </main>
            <Footer />

        </div>
    )
}

export default MyServices;