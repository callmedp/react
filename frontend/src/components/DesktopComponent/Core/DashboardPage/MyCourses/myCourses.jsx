import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ProgressBar } from 'react-bootstrap';
import { Collapse } from 'react-bootstrap';
import { Button } from 'react-bootstrap';
import { Modal } from 'react-bootstrap';
import NoCourses from './noCourses';
import './myCourses.scss';
import '../../SkillPage/NeedHelp/needHelp.scss';

   
const MyCourses = (props) => {
    const [addOpen, setaddOpen] = useState(false);
    const [open, setOpen] = useState(false);
    const [openReview, setOpenReview] = useState(false);
    const [openViewDetail, setOpenViewDetail] = useState(false);

    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    return(
        <div>
            {/* <NoCourses /> */}

            <div className="db-my-courses-detail">
                <div className="db-white-box w-100">
                    <div className="d-flex">
                        <figure>
                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                        </figure>

                        <div className="db-my-courses-detail--wrap">
                            <div className="d-flex w-100">
                                <div className="db-my-courses-detail__leftpan">
                                    <div className="db-my-courses-detail__leftpan--box">
                                        <h3><Link to={"#"}>Digital Marketing &amp; Email Marketing Training Course</Link></h3>
                                        <div className="db-my-courses-detail__leftpan--info">
                                            <span>Provider: <Link to={"#"}>Vskills</Link></span>
                                            <span>Enrolled on: <strong>27 Oct 2020</strong></span>
                                            <span>Duration: <strong>90 days</strong></span>
                                            <span>Mode: <strong>Online</strong></span>
                                            <span>Jobs: <strong>2892</strong></span>
                                        </div>

                                        <div className="db-my-courses-detail__leftpan--session">
                                            <span>Next session : <strong>Basic of Digital Marketing</strong></span>
                                            <span className="db-icon-date font-weight-bold">3PM |  29 nov 2020</span>
                                        </div>

                                        <div className="db-my-courses-detail__leftpan--alert">
                                            Hi, the recording for the session you missed is available now <Link to={"#"} className="ml-2">Click here</Link>
                                        </div>

                                        <div className="db-my-courses-detail__leftpan--status mb-2">
                                            Status:
                                            <strong className="ml-1">Course yet to start</strong> 
                                        </div>

                                        <Link 
                                            className="font-weight-bold"
                                            onClick={() => setOpenViewDetail(!openViewDetail)}
                                            aria-controls="addComments"
                                            aria-expanded={openViewDetail}
                                        >
                                            View Details
                                        </Link>

                                        <Collapse in={openViewDetail}>
                                            <div className="db-view-detail arrow-box left-big" id="openViewDetail">
                                            <span className="btn-close"  onClick={() => setOpenViewDetail(!openViewDetail)}>&#x2715;</span>
                                                <ul className="db-timeline-list">
                                                    <li>
                                                        <i className="db-timeline-list--dot"></i>
                                                        <span>Dec. 11, 2020    |   By Amit Kumar</span>
                                                        <p className="db-timeline-list--text">Need help to understand this service.</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="db-timeline-list--dot"></i>
                                                        <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                                        <p className="db-timeline-list--text">We will call you for detailed info of this service</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="db-timeline-list--dot"></i>
                                                        <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                                        <p className="db-timeline-list--text">Thanks for your confirmation!</p>
                                                    </li>
                                                    <li>
                                                        <i className="db-timeline-list--dot"></i>
                                                        <span>Dec. 11, 2020    |   By Amit Kumar</span>
                                                        <p className="db-timeline-list--text">Need help to understand this service.</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="db-timeline-list--dot"></i>
                                                        <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                                        <p className="db-timeline-list--text">We will call you for detailed info of this service</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="db-timeline-list--dot"></i>
                                                        <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                                        <p className="db-timeline-list--text">Thanks for your confirmation!</p>
                                                    </li>
                                                </ul>
                                            </div>
                                        </Collapse>
                                    </div>
                                </div>

                                <div className="db-my-courses-detail__rightpan">
                                    <div className="share">
                                        <i className="icon-share"></i>
                                        <div className="share__box arrow-box top">
                                            <Link to={"#"} className="facebook-icon"></Link>
                                            <Link to={"#"} className="linkedin-icon"></Link>
                                            <Link to={"#"} className="twitter-iocn"></Link>
                                            <Link to={"#"} className="whatsup-icon"></Link>
                                        </div>
                                    </div>

                                    <div className="day-remaning mb-20">
                                        <span className="day-remaning--box">9</span>
                                        <span className="day-remaning--box">0</span>
                                        <span className="ml-2 day-remaning--text">Days <br/>remaning</span>
                                    </div>

                                    <div className="db-status mt-20">
                                        <p className="mb-0 pb-1">Status: <strong>(0% Complete)</strong> </p>
                                        <ProgressBar now={0} />
                                    </div>

                                    <Link to={"#"} className="db-start-course font-weight-bold mt-30">Start course</Link>
                                </div>
                            </div>


                            <div className="db-my-courses-detail__bottom">
                                <Link
                                    className="db-comments font-weight-bold"
                                    onClick={() => setaddOpen(!addOpen)}
                                    aria-controls="addComments"
                                    aria-expanded={addOpen}
                                >
                                    Add comment
                                </Link>

                                

                                <div className="d-flex">
                                    <div className="card__rating">
                                        <span 
                                            className="cursor-pointer mr-2 font-weight-bold"
                                            onClick={handleShow}
                                        >
                                            Rate course
                                        </span>

                                        <span className="rating">
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                        </span>
                                    </div>

                                    <Modal show={show} onHide={handleClose} className="db-modal">
                                        <Modal.Header closeButton>
                                        </Modal.Header>
                                        <Modal.Body>
                                            <div className="text-center db-rate-services need-help">
                                                <img src="/media/images/rate-services.png" className="img-fluid" alt=""/>
                                                <p className="db-rate-services--heading">Rate service</p>
                                                
                                                <span className="rating">
                                                    <em className="icon-blankstar"></em>
                                                    <em className="icon-blankstar"></em>
                                                    <em className="icon-blankstar"></em>
                                                    <em className="icon-blankstar"></em>
                                                    <em className="icon-blankstar"></em>
                                                </span>
                                                <p className="db-rate-services--subheading">Click on rate to scale of 1-5</p>
                                                <form action="">
                                                    <div className="form-group">
                                                        <input type="email" className="form-control" id="email" name="email" placeholder=" "
                                                            value="" aria-required="true" aria-invalid="true" />
                                                        <label for="">Email</label>
                                                    </div>
                                                    
                                                    <div className="form-group">
                                                        <textarea  className="form-control" name="review" id="review" cols="30" rows="3" placeholder=" "></textarea>
                                                        <label for="">Review</label>
                                                    </div>

                                                    <button className="btn btn-primary px-5">Submit</button>
                                                </form>
                                            </div>
                                        </Modal.Body>
                                    </Modal>
                                </div>

                            </div>
                        </div>
                    </div>

                    <Collapse in={addOpen}>
                        <div className="db-add-comments lightblue-bg" id="addComments">
                            <span className="btn-close"  onClick={() => setaddOpen(!addOpen)}>&#x2715;</span>
                            <p className="font-weight-semi-bold"> Add comment </p>
                            <textarea class="form-control" rows="3"></textarea>
                            <button type="submit" class="btn btn-outline-primary mt-20 px-5">Submit</button>
                        </div>
                    </Collapse>
                </div>
                
                <div className="db-white-box w-100">
                    <div className="d-flex">
                        <figure>
                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                        </figure>

                        <div className="db-my-courses-detail--wrap">
                            <div className="d-flex w-100">
                                <div className="db-my-courses-detail__leftpan">
                                    <div className="db-my-courses-detail__leftpan--box">
                                        <h3><Link to={"#"}>Digital Marketing &amp; Email Marketing Training Course</Link></h3>
                                        <div className="db-my-courses-detail__leftpan--info">
                                            <span>Provider: <Link to={"#"}>Vskills</Link></span>
                                            <span>Enrolled on: <strong>27 Oct 2020</strong></span>
                                            <span>Duration: <strong>90 days</strong></span>
                                            <span>Mode: <strong>Online</strong></span>
                                            <span>Jobs: <strong>2892</strong></span>
                                        </div>


                                        <div className="db-my-courses-detail__leftpan--status mb-2">
                                            Status:
                                            <strong className="ml-1">Course yet to start</strong> 
                                        </div>

                                        <Link to={"#"} className="font-weight-bold">View Details</Link>
                                    </div>
                                </div>

                                <div className="db-my-courses-detail__rightpan">
                                    <div className="share">
                                        <i className="icon-share"></i>
                                        <div className="share__box arrow-box top">
                                            <Link to={"#"} className="facebook-icon"></Link>
                                            <Link to={"#"} className="linkedin-icon"></Link>
                                            <Link to={"#"} className="twitter-iocn"></Link>
                                            <Link to={"#"} className="whatsup-icon"></Link>
                                        </div>
                                    </div>

                                    <div className="db-status mt-20">
                                        <p className="mb-0 pb-1">Status: <strong className="mr-2">(0% Complete)</strong> 
                                            <i className="db-green-tick"></i> 
                                        </p>
                                        <ProgressBar now={100} />
                                    </div>

                                    <Link to={"#"} className="db-view-result font-weight-bold mt-30">View Result</Link>
                                </div>
                            </div>


                            <div className="db-my-courses-detail__bottom">
                                <Link
                                    className="db-comments font-weight-bold"
                                    onClick={() => setOpen(!open)}
                                    aria-controls="threeComments"
                                    aria-expanded={open}
                                >
                                    3 comments
                                </Link>
                                

                                <div className="d-flex">
                                    <div className="db-certificate">
                                        <i className="db-certificate-icon"></i>
                                        <span className="db-certificate--text arrow-box top">Download certificate</span>
                                    </div>
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
                                    
                                    <div className="position-relative">
                                        <Link 
                                            className="ml-15"
                                            onClick={() => setOpenReview(!openReview)}
                                            aria-controls="threeComments"
                                            aria-expanded={openReview}
                                        >
                                                
                                            <strong>2</strong> Reviews
                                        </Link>

                                        <Collapse in={openReview}>
                                            <div className="db-reviews-list-wrap arrow-box top-big">
                                                <span className="btn-close"  onClick={() => setOpenReview(!openReview)}>&#x2715;</span>
                                                <div className="reviews-list">
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

                                                            <span className="reviews-list--date">Dec. 21, 2020</span>
                                                            <p className="reviews-list--text">Great product for your career.  It helped alot to enhance my career</p>
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

                                                            <span className="reviews-list--date">Oct. 14, 2020</span>
                                                            <p className="reviews-list--text">Good Mentors with good experience</p>
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

                                                            <span className="reviews-list--date">Dec. 21, 2020</span>
                                                            <p className="reviews-list--text">Great product for your career.  It helped alot to enhance my career</p>
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

                                                            <span className="reviews-list--date">Oct. 14, 2020</span>
                                                            <p className="reviews-list--text">Good Mentors with good experience</p>
                                                        </li>
                                                    </ul>

                                                    <button className="btn btn-outline-primary">Add new</button>
                                                </div>
                                                
                                                <div className="db-reviews-list-wrap--bottom">
                                                    <button className="btn btn-outline-primary">Add new</button>
                                                </div>
                                            </div>
                                        </Collapse>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <Collapse in={open}>
                        <div className="position-relative" id="threeComments">
                            
                            <div className="db-add-comments lightblue-bg border-bottom-gray">
                                <span className="btn-close"  onClick={() => setOpen(!open)}>&#x2715;</span>
                                <ul className="db-timeline-list">
                                    <li>
                                        <i className="db-timeline-list--dot"></i>
                                        <span>Dec. 11, 2020    |   By Amit Kumar</span>
                                        <p className="db-timeline-list--text">Need help to understand this service.</p>
                                    </li>
                                    
                                    <li>
                                        <i className="db-timeline-list--dot"></i>
                                        <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                        <p className="db-timeline-list--text">We will call you for detailed info of this service</p>
                                    </li>
                                    
                                    <li>
                                        <i className="db-timeline-list--dot"></i>
                                        <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                        <p className="db-timeline-list--text">Thanks for your confirmation!</p>
                                    </li>
                                </ul>
                            </div>
                            
                            <div className="db-add-comments disabled-before lightblue-bg">
                                <p className="font-weight-semi-bold"> Add comment </p>
                                <textarea class="form-control" rows="3"></textarea>
                                <button type="submit" class="btn btn-outline-primary mt-20 px-5">Submit</button>
                            </div>
                        </div>
                    </Collapse>

                    <div className="db-mycourse-highlighter">Next course to take: <Link to={"#"} className="font-weight-bold ml-2">Seo Specialist</Link> </div>
                </div>


                <div className="db-white-box w-100">
                    <div className="d-flex">
                        <figure>
                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                        </figure>

                        <div className="db-my-courses-detail--wrap">
                            <div className="d-flex w-100">
                                <div className="db-my-courses-detail__leftpan">
                                    <div className="db-my-courses-detail__leftpan--box">
                                        <h3><Link to={"#"}>Digital Marketing &amp; Email Marketing Training Course</Link></h3>
                                        <div className="db-my-courses-detail__leftpan--info">
                                            <span>Provider: <Link to={"#"}>Vskills</Link></span>
                                            <span>Enrolled on: <strong>27 Oct 2020</strong></span>
                                            <span>Duration: <strong>90 days</strong></span>
                                            <span>Mode: <strong>Online</strong></span>
                                            <span>Jobs: <strong>2892</strong></span>
                                        </div>

                                        <div className="db-my-courses-detail__leftpan--session">
                                            <span>Next session : <strong>Basic of Digital Marketing</strong></span>
                                            <span className="db-icon-date font-weight-bold">3PM |  29 nov 2020</span>
                                        </div>

                                        <div className="db-my-courses-detail__leftpan--alert">
                                            Hi, the recording for the session you missed is available now <Link to={"#"} className="ml-2">Click here</Link>
                                        </div>

                                        <div className="db-my-courses-detail__leftpan--status mb-2">
                                            Status:
                                            <strong className="ml-1">Course yet to start</strong> 
                                        </div>

                                        <Link to={"#"} className="font-weight-bold">View Details</Link>
                                    </div>
                                </div>

                                <div className="db-my-courses-detail__rightpan">
                                    <div className="share">
                                        <i className="icon-share"></i>
                                        <div className="share__box arrow-box top">
                                            <Link to={"#"} className="facebook-icon"></Link>
                                            <Link to={"#"} className="linkedin-icon"></Link>
                                            <Link to={"#"} className="twitter-iocn"></Link>
                                            <Link to={"#"} className="whatsup-icon"></Link>
                                        </div>
                                    </div>

                                    <div className="day-remaning">
                                        <span className="day-remaning--box">3</span>
                                        <span className="day-remaning--box">0</span>
                                        <span className="ml-2 day-remaning--text">Days <br/>remaning</span>
                                    </div>

                                    <div className="db-status mt-20">
                                        <p className="mb-0 pb-1">Status: <strong>(50% Complete)</strong> </p>
                                        <ProgressBar now={50} />
                                    </div>

                                    <Link to={"#"} className="db-resume-course font-weight-bold mt-30">Resume course</Link>
                                </div>
                            </div>


                            <div className="db-my-courses-detail__bottom">
                                <Link className="db-comments font-weight-bold" to={"#"}>Add comment</Link>

                                <div className="d-flex">
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
                                    <div>
                                        <Link to={"#"} className="ml-15"> <strong>2</strong> Reviews</Link>
                                    </div>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
                
            </div>
        </div>
    )
}
   
export default MyCourses;