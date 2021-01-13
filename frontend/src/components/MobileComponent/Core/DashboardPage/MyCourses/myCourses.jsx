import React from 'react';
import { Link } from 'react-router-dom';
import './myCourses.scss';

   
const MyCourses = (props) => {
    return(
        <div>
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
                            <h2>Certified Digital Marketing Master Certification</h2>
                            <p className="m-pipe-divides mb-5">Provider: <Link to={"#"} className="font-weight-bold">Vskills</Link></p>
                            <p className="m-pipe-divides mb-5"><span>Enrolled on: <strong>27 Oct 2020</strong> </span> <span>Mode: <strong>Online</strong> </span></p>
                            <p className="m-pipe-divides mb-5"><span>Duration: <strong>90 days</strong> </span> <span>Jobs: <strong>2892</strong> </span></p>
                        </div>
                    </div>
                    <div className="m-courses-detail--session pl-15 d-flex mb-15 mt-10">
                        <span>Next session :</span> 
                        <strong>Basic of Digital Marketing 3PM |  29 nov 2020</strong> 
                    </div>
                    
                    <div className="m-courses-detail--alert">
                    Hi, the recording for the session you missed is available now <Link to={"#"} className="font-weight-semi-bold">Check here</Link>
                    </div>

                    <div className="pl-15 mt-15 fs-12">
                        Status: <strong>Course yet to start</strong>
                        <Link to={"#"} className="d-block font-weight-bold">View Details</Link>
                    </div>

                    <div className="pl-15">
                        <div className="m-courses-detail__bottomWrap">
                            <div>
                                <div className="m-day-remaning mb-20">
                                    <span className="m-day-remaning--box">9</span>
                                    <span className="m-day-remaning--box">0</span>
                                    <span className="ml-2 m-day-remaning--text">Days <br/>remaning</span>
                                </div>

                                <div className="m-db-status">
                                    <p className="mb-0 pb-1">Status: <strong>(0% Complete)</strong> </p>

                                    <div class="m-progress">
                                        <div role="progressbar" class="m-progress-bar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style={{width: "0"}}></div>
                                    </div>
                                </div>
                            </div>

                            <Link to={"#"} className="m-db-start-course font-weight-bold pr-10">Start course</Link>
                        </div>

                        <div className="m-courses-detail__userInput">
                            <Link className="m-db-comments font-weight-bold">Add comment</Link>
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
                            <h2>Certified Digital Marketing Master Certification</h2>
                            <p className="m-pipe-divides mb-5">Provider: <Link to={"#"} className="font-weight-bold">Vskills</Link></p>
                            <p className="m-pipe-divides mb-5"><span>Enrolled on: <strong>27 Oct 2020</strong> </span> <span>Mode: <strong>Online</strong> </span></p>
                            <p className="m-pipe-divides mb-5"><span>Duration: <strong>90 days</strong> </span> <span>Jobs: <strong>2892</strong> </span></p>
                        </div>
                    </div>


                    <div className="pl-15 mt-15 fs-12">
                        Status: <strong>Course yet to start</strong>
                        <Link to={"#"} className="d-block font-weight-bold">View Details</Link>
                    </div>

                    <div className="pl-15">
                        <div className="m-courses-detail__bottomWrap">
                            <div>
                                <div className="m-db-status">
                                    <p className="mb-0 pb-1">Status: <strong>(100% Complete)</strong> 
                                        <i className="m-db-green-tick"></i> 
                                    </p>

                                    <div class="m-progress">
                                        <div role="progressbar" class="m-progress-bar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style={{width: "100%"}}></div>
                                    </div>
                                </div>
                            </div>
                            
                            <div className="d-flex align-items-center justify-content-end">
                                <Link to={"#"} className="font-weight-bold fs-13 mr-30">View result</Link>
                                <Link to={"#"} className="m-db-certificate-icon"></Link>
                            </div>
                        </div>

                        <div className="m-courses-detail__userInput">
                            <Link className="m-db-comments font-weight-bold">3 Comment</Link>
                            <div className="d-flex">
                                <span className="m-rating">
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-blankstar"></em>
                                    <span class="ml-5">4/5</span>
                                </span>
                                <Link to={"#"} className="font-weight-bold ml-10">2</Link>
                            </div>
                        </div>
                    </div>

                    <div className="m-mycourse-highlighter">Next course to take: <Link to={"#"} className="font-weight-bold ml-2">Seo Specialist</Link> </div>
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
                            <h2>Certified Digital Marketing Master Certification</h2>
                            <p className="m-pipe-divides mb-5">Provider: <Link to={"#"} className="font-weight-bold">Vskills</Link></p>
                            <p className="m-pipe-divides mb-5"><span>Enrolled on: <strong>27 Oct 2020</strong> </span> <span>Mode: <strong>Online</strong> </span></p>
                            <p className="m-pipe-divides mb-5"><span>Duration: <strong>90 days</strong> </span> <span>Jobs: <strong>2892</strong> </span></p>
                        </div>
                    </div>

                    <div className="pl-15 mt-15 fs-12">
                        Status: <strong>Course in progress</strong>
                        <Link to={"#"} className="d-block font-weight-bold">View Details</Link>
                    </div>

                    <div className="pl-15">
                        <div className="m-courses-detail__bottomWrap">
                            <div>
                                <div className="m-day-remaning mb-20">
                                    <span className="m-day-remaning--box">3</span>
                                    <span className="m-day-remaning--box">0</span>
                                    <span className="ml-2 m-day-remaning--text">Days <br/>remaning</span>
                                </div>

                                <div className="m-db-status">
                                    <p className="mb-0 pb-1">Status: <strong>(0% Complete)</strong> </p>

                                    <div class="m-progress">
                                        <div role="progressbar" class="m-progress-bar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style={{width: "0"}}></div>
                                    </div>
                                </div>
                            </div>

                            <Link to={"#"} className="m-db-resume-course font-weight-bold mt-30">Resume course</Link>
                        </div>

                        <div className="m-courses-detail__userInput">
                            <Link className="m-db-comments font-weight-bold">3 Comment</Link>
                            <div className="d-flex">
                                <span className="m-rating">
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-fullstar"></em>
                                    <em className="micon-blankstar"></em>
                                    <span class="ml-5">4/5</span>
                                </span>
                                <Link to={"#"} className="font-weight-bold ml-10">2</Link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div className="m-slide-modal">
                <div className="text-center"  style={{display: 'none'}}>
                    <span className="m-db-close">&#x2715;</span>
                    <h2>Add comment</h2>
                    <div className="m-enquire-now mt-15">
                        <div className="m-form-group">
                            <textarea id="addComments" placeholder=" " rows="4"></textarea>
                            <label htmlFor="addComments">Enter comment here</label>
                        </div>

                        <button className="btn btn-blue">Submit</button>
                    </div>
                </div>

                <div className="" style={{display: 'none'}}>
                    <span className="m-db-close">&#x2715;</span>
                    <ul className="m-timeline-list">
                        <li>
                            <i className="m-timeline-list--dot"></i>
                            <span>Dec. 11, 2020    |   By Amit Kumar</span>
                            <p className="m-timeline-list--text">Need help to understand this service.</p>
                        </li>
                        
                        <li>
                            <i className="m-timeline-list--dot"></i>
                            <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                            <p className="m-timeline-list--text">We will call you for detailed info of this service</p>
                        </li>
                        
                        <li>
                            <i className="m-timeline-list--dot"></i>
                            <span>Dec. 18, 2020    |   By Amit Kumar</span>
                            <p className="m-timeline-list--text">Thanks for your confirmation!</p>
                        </li>
                        <li>
                            <i className="m-timeline-list--dot"></i>
                            <span>Dec. 11, 2020    |   By Amit Kumar</span>
                            <p className="m-timeline-list--text">Need help to understand this service.</p>
                        </li>
                        
                        <li>
                            <i className="m-timeline-list--dot"></i>
                            <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                            <p className="m-timeline-list--text">We will call you for detailed info of this service</p>
                        </li>
                        
                        <li>
                            <i className="m-timeline-list--dot"></i>
                            <span>Dec. 18, 2020    |   By Amit Kumar</span>
                            <p className="m-timeline-list--text">Thanks for your confirmation!</p>
                        </li>
                    </ul>
                    <hr />
                    <div className="m-enquire-now mt-15 text-center">
                        <div className="m-form-group">
                            <textarea id="addComments" placeholder=" " rows="4"></textarea>
                            <label htmlFor="addComments">Enter comment here</label>
                        </div>

                        <button className="btn btn-blue">Submit</button>
                    </div>
                </div>

                <div className="addcomments" style={{display: 'block'}}>
                    <span className="m-db-close">&#x2715;</span>
                    
                    <div className="m-reviews-list">
                        <ul>
                            <li>
                                <div className="card__rating">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span> <strong>4</strong> /5</span>
                                    </span>
                                </div>

                                <span className="m-reviews-list--date">Dec. 21, 2020</span>
                                <p className="m-reviews-list--text">Great product for your career.  It helped alot to enhance my career</p>
                            </li>
                            
                            <li>
                                <div className="card__rating">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span> <strong>4</strong> /5</span>
                                    </span>
                                </div>

                                <span className="m-reviews-list--date">Oct. 14, 2020</span>
                                <p className="m-reviews-list--text">Good Mentors with good experience</p>
                            </li>
                            <li>
                                <div className="card__rating">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span> <strong>4</strong> /5</span>
                                    </span>
                                </div>

                                <span className="m-reviews-list--date">Dec. 21, 2020</span>
                                <p className="m-reviews-list--text">Great product for your career.  It helped alot to enhance my career</p>
                            </li>
                            
                            <li>
                                <div className="card__rating">
                                    <span className="rating">
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-fullstar"></em>
                                        <em className="icon-blankstar"></em>
                                        <span> <strong>4</strong> /5</span>
                                    </span>
                                </div>

                                <span className="m-reviews-list--date">Oct. 14, 2020</span>
                                <p className="m-reviews-list--text">Good Mentors with good experience</p>
                            </li>
                        </ul>
                    </div>
                    
                    <div className="m-reviews-list-wrap--bottom">
                        <button className="btn btn-blue-outline px-30">Add new</button>
                    </div>
                </div>

            </div>
        </div>
    )
}
   
export default MyCourses;