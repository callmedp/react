import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ProgressBar } from 'react-bootstrap';
import { Collapse } from 'react-bootstrap';
import { Button } from 'react-bootstrap';
import { Modal } from 'react-bootstrap';
import '../MyCourses/myCourses.scss';
import './myServices.scss';

   
const MyServices = (props) => {
    const [addOpen, setaddOpen] = useState(false);
    
    const [open, setOpen] = useState(false);
    const [openReview, setOpenReview] = useState(false);
    const [openViewDetail, setOpenViewDetail] = useState(false);

    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    
    const [rejectShow, setRejectShow] = useState(false);
    const rejectHandelClose = () => setRejectShow(false);
    const rejectHandelShow = () => setRejectShow(true);
    
    const [uploadShow, setUploadShow] = useState(false);
    const uploadHandelClose = () => setUploadShow(false);
    const uploadHandelShow = () => setUploadShow(true);

    return(
        <div>

            <div className="my-courses-detail">

                <div className="db-white-box w-100">
                    <div className="d-flex">
                        <figure>
                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                        </figure>

                        <div className="my-courses-detail--wrap">
                            <div className="d-flex w-100">
                                <div className="my-courses-detail__leftpan">
                                    <div className="my-courses-detail__leftpan--box">
                                        <h3><Link to={"#"}>Resume Booster 5-10 years</Link></h3>
                                        <div className="my-courses-detail__leftpan--info">
                                            <span>Provider: <strong>Shine learning</strong> </span>
                                            <span>Bought on: <strong>27 Oct 2020</strong></span>
                                            <span>Duration: <strong>90 days</strong></span>
                                        </div>

                                        <div className="my-courses-detail__leftpan--alert">
                                        Hi, the recording for the session you missed is available now
                                        </div>

                                        <div className="my-courses-detail__leftpan--status mb-2">
                                            Status:
                                            <strong className="ml-1">Upload your resume 
                                                <Link to={"#"} className="ml-2" onClick={uploadHandelShow}>Upload</Link> 
                                            </strong> 

                                            <Modal show={uploadShow} onHide={uploadHandelClose}>
                                                <Modal.Header closeButton>
                                                </Modal.Header>
                                                <Modal.Body>
                                                    <div className="text-center rate-services db-custom-select-form db-upload-resume">
                                                        <img src="/media/images/upload-resume.png" className="img-fluid" alt=""/>
                                                        <p className="rate-services--heading mb-0 mt-0">Upload Resume</p>
                                                    
                                                        <p className="">To initiate your services, <strong>upload resume</strong></p>
                                                        
                                                        <div className="d-flex align-items-center justify-content-center mt-20">
                                                            <div class="upload-btn-wrapper">
                                                                <button class="btn btn-outline-primary">Upload a file</button>
                                                                <input type="file" name="myfile" />
                                                            </div>

                                                            <span className="mx-4">Or</span>

                                                            <div className="custom-control custom-checkbox">
                                                                <input type="checkbox" className="custom-control-input" id="shineResume" /> 
                                                                <label className="custom-control-label font-weight-bold" for="shineResume">Use shine resume</label>
                                                            </div>
                                                        </div>
                                                        <hr className="my-5"/>

                                                        <div className="db-upload-resume--services">
                                                            <strong>Select services</strong> for which you want to use this resume
                                                            <ul className="db-upload-resume--list">
                                                                <li className="custom-control custom-checkbox">
                                                                    <input type="checkbox" className="custom-control-input" id="resumeBooster" /> 
                                                                    <label className="custom-control-label font-weight-bold" for="resumeBooster">Resume Booster 5-10 years</label>
                                                                </li>

                                                                <li className="custom-control custom-checkbox">
                                                                    <input type="checkbox" className="custom-control-input" id="resumeBuilder" /> 
                                                                    <label className="custom-control-label font-weight-bold" for="resumeBuilder">Resume Builder 5-10 yrs</label>
                                                                </li>

                                                                <li className="custom-control custom-checkbox">
                                                                    <input type="checkbox" className="custom-control-input" id="services" /> 
                                                                    <label className="custom-control-label font-weight-bold" for="services">For all services</label>
                                                                </li>
                                                            </ul>
                                                        </div>

                                                        <button className="btn btn-primary px-5 mt-30">Save</button>
                                                    </div>
                                                </Modal.Body>
                                            </Modal>

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
                                            <div className="view-detail arrow-box left-big" id="openViewDetail">
                                            <span className="btn-close"  onClick={() => setOpenViewDetail(!openViewDetail)}>&#x2715;</span>
                                                <ul className="timeline-list">
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 11, 2020    |   By Amit Kumar</span>
                                                        <p className="timeline-list--text">Need help to understand this service.</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                                        <p className="timeline-list--text">We will call you for detailed info of this service</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                                        <p className="timeline-list--text">Thanks for your confirmation!</p>
                                                    </li>
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 11, 2020    |   By Amit Kumar</span>
                                                        <p className="timeline-list--text">Need help to understand this service.</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                                        <p className="timeline-list--text">We will call you for detailed info of this service</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                                        <p className="timeline-list--text">Thanks for your confirmation!</p>
                                                    </li>
                                                </ul>
                                            </div>
                                        </Collapse>
                                    </div>
                                </div>

                                <div className="my-courses-detail__rightpan">
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
                                </div>
                            </div>


                            <div className="my-courses-detail__bottom">
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
                                            Rate Services
                                        </span>

                                        <span className="rating">
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                        </span>
                                    </div>

                                    <Modal show={show} onHide={handleClose}>
                                        <Modal.Header closeButton>
                                        </Modal.Header>
                                        <Modal.Body>
                                            <div className="text-center rate-services need-help">
                                                <img src="/media/images/rate-services.png" className="img-fluid" alt=""/>
                                                <p className="rate-services--heading">Rate service</p>
                                                
                                                <span className="rating">
                                                    <em className="icon-blankstar"></em>
                                                    <em className="icon-blankstar"></em>
                                                    <em className="icon-blankstar"></em>
                                                    <em className="icon-blankstar"></em>
                                                    <em className="icon-blankstar"></em>
                                                </span>
                                                <p className="rate-services--subheading">Click on rate to scale of 1-5</p>
                                                <form action="">
                                                    <div className="form-group error">
                                                        <input type="email" className="form-control" id="email" name="email" placeholder=" "
                                                            value="" aria-required="true" aria-invalid="true" />
                                                        <label for="">Email</label>
                                                        <span class="error-msg">Required</span>
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

                        <div className="my-courses-detail--wrap">
                            <div className="d-flex w-100">
                                <div className="my-courses-detail__leftpan">
                                    <div className="my-courses-detail__leftpan--box">
                                        <h3><Link to={"#"}>Profile Booster</Link></h3>
                                        <div className="my-courses-detail__leftpan--info">
                                            <span>Provider: <strong>Shine learning</strong> </span>
                                            <span>Bought on: <strong>27 Oct 2020</strong></span>
                                            <span>Duration: <strong>90 days</strong></span>
                                        </div>

                                        <div className="my-courses-detail__leftpan--status mb-2">
                                            Status:
                                            <strong className="ml-1">Service under progress</strong> 
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
                                            <div className="view-detail arrow-box left-big" id="openViewDetail">
                                            <span className="btn-close"  onClick={() => setOpenViewDetail(!openViewDetail)}>&#x2715;</span>
                                                <ul className="timeline-list">
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 11, 2020    |   By Amit Kumar</span>
                                                        <p className="timeline-list--text">Need help to understand this service.</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                                        <p className="timeline-list--text">We will call you for detailed info of this service</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                                        <p className="timeline-list--text">Thanks for your confirmation!</p>
                                                    </li>
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 11, 2020    |   By Amit Kumar</span>
                                                        <p className="timeline-list--text">Need help to understand this service.</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                                        <p className="timeline-list--text">We will call you for detailed info of this service</p>
                                                    </li>
                                                    
                                                    <li>
                                                        <i className="timeline-list--dot"></i>
                                                        <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                                        <p className="timeline-list--text">Thanks for your confirmation!</p>
                                                    </li>
                                                </ul>
                                            </div>
                                        </Collapse>
                                    </div>
                                </div>

                                <div className="my-courses-detail__rightpan">
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
                                    <Link to={"#"} className="db-start-course font-weight-bold mt-30">Start course</Link>
                                </div>
                            </div>


                            <div className="my-courses-detail__bottom">
                                <Link
                                    className="db-comments font-weight-bold"
                                >
                                    3 comment
                                </Link>
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

                        <div className="my-courses-detail--wrap">
                            <div className="d-flex w-100">
                                <div className="my-courses-detail__leftpan">
                                    <div className="my-courses-detail__leftpan--box">
                                        <h3><Link to={"#"}>Linkedin Profile Writing</Link></h3>
                                        <div className="my-courses-detail__leftpan--info">
                                            <span>Provider: <strong>Shine learning</strong> </span>
                                            <span>Bought on: <strong>27 Oct 2020</strong></span>
                                            <span>Duration: <strong>90 days</strong></span>
                                        </div>


                                        <div className="my-courses-detail__leftpan--status mb-2">
                                            Status:
                                            <strong className="ml-1">Service under progress</strong> 
                                        </div>

                                        <Link to={"#"} className="font-weight-bold">View Details</Link>
                                    </div>
                                </div>

                                <div className="my-courses-detail__rightpan">
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
                                </div>
                            </div>


                            <div className="my-courses-detail__bottom">
                                <Link
                                    className="db-comments font-weight-bold"
                                    onClick={() => setOpen(!open)}
                                    aria-controls="threeComments"
                                    aria-expanded={open}
                                >
                                    3 comments
                                </Link>
                                

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
                                            <div className="reviews-list-wrap arrow-box top-big">
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
                                                </div>
                                                
                                                <div className="reviews-list-wrap--bottom">
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
                                <ul className="timeline-list">
                                    <li>
                                        <i className="timeline-list--dot"></i>
                                        <span>Dec. 11, 2020    |   By Amit Kumar</span>
                                        <p className="timeline-list--text">Need help to understand this service.</p>
                                    </li>
                                    
                                    <li>
                                        <i className="timeline-list--dot"></i>
                                        <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                        <p className="timeline-list--text">We will call you for detailed info of this service</p>
                                    </li>
                                    
                                    <li>
                                        <i className="timeline-list--dot"></i>
                                        <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                        <p className="timeline-list--text">Thanks for your confirmation!</p>
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
                </div>


                <div className="db-white-box w-100">
                    <div className="d-flex">
                        <figure>
                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                        </figure>

                        <div className="my-courses-detail--wrap">
                            <div className="d-flex w-100">
                                <div className="my-courses-detail__leftpan">
                                    <div className="my-courses-detail__leftpan--box">
                                        <h3><Link to={"#"}>Resume Builder 0-2 years</Link></h3>
                                        <div className="my-courses-detail__leftpan--info">
                                            <span>Provider: <strong>Shine learning</strong> </span>
                                            <span>Bought on: <strong>27 Oct 2020</strong></span>
                                            <span>Duration: <strong>90 days</strong></span>
                                        </div>

                                        <div className="my-courses-detail__leftpan--status mb-2">
                                            Status:
                                            <strong className="ml-1"> 
                                                <Link to={"#"} className="mx-2">Newresume.pdf</Link> 
                                                uploaded by Shine

                                                <Link className="accept" to={"#"}>Accept</Link>
                                                <Link 
                                                    className="ml-2 reject" to={"#"}
                                                    onClick={rejectHandelShow}
                                                >  
                                                Reject
                                                </Link>
                                            </strong>
                                           
                                            <Modal show={rejectShow} onHide={rejectHandelClose}>
                                                <Modal.Header closeButton>
                                                </Modal.Header>
                                                <Modal.Body>
                                                    <div className="text-center rejectModal need-help">
                                                       <p className="rejectModal--heading">Get a Better resume by sharing us the feedback for resume</p>
                                                        <form action="">

                                                            <div className="form-group">
                                                                <textarea  className="form-control" name="review" id="review" cols="30" rows="4" placeholder=" "></textarea>
                                                                <label for="">Review</label>
                                                            </div>

                                                            <button className="btn btn-primary px-5">Submit</button>
                                                        </form>
                                                    </div>
                                                </Modal.Body>
                                            </Modal>

                                        </div>

                                        <Link to={"#"} className="font-weight-bold">View Details</Link>
                                    </div>
                                </div>

                                <div className="my-courses-detail__rightpan">
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
                                </div>
                            </div>


                            <div className="my-courses-detail__bottom">
                                <Link className="db-comments font-weight-bold" to={"#"}>Add comment</Link>

                                <div className="d-flex">
                                    <div className="card__rating">
                                        <span class="cursor-pointer mr-2 font-weight-bold">Rate Services</span>
                                        <span className="rating">
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <em className="icon-blankstar"></em>
                                        </span>
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
   
export default MyServices;