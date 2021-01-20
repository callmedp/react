import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ProgressBar } from 'react-bootstrap';
import { Collapse } from 'react-bootstrap';
import { Button } from 'react-bootstrap';
import { Modal } from 'react-bootstrap';
import '../MyCourses/myCourses.scss';
import './myServices.scss';
import { startDashboardServicesPageLoader, stopDashboardServicesPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMyServices, uploadResumeForm, getoiComment } from 'store/DashboardPage/MyServices/actions';
import { useForm } from "react-hook-form";
import fileUpload from "utils/fileUpload";
import Swal from 'sweetalert2';
import {getCandidateId} from 'utils/storage';

const MyServices = (props) => {
    const [addOpen, setaddOpen] = useState(false);
    
    const [open, setOpen] = useState(false);
    const [openReview, setOpenReview] = useState(false);
    const toggleReviews = (id) => setOpenReview(openReview == id ? false : id);

    // const [openViewDetail, setOpenViewDetail] = useState(false);

    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    
    const [rejectShow, setRejectShow] = useState(false);
    const rejectHandelClose = () => setRejectShow(false);
    const rejectHandelShow = () => setRejectShow(true);
    
    const [uploadShow, setUploadShow] = useState(false);
    const uploadHandelClose = () => setUploadShow(false);
    const uploadHandelShow = () => setUploadShow(true);

    const results = useSelector(store => store.dashboardServices);
    const dispatch = useDispatch();
    const { history } = props;
    const { serviceLoader } = useSelector(store => store.loader);
    let comment_id = null;

    const comm = useSelector(store => console.log(store));
    
    const [isOpen, setIsOpen] = useState(false);
    const toggleDetails = (id) => setIsOpen(isOpen == id ? false : id);

    let [rating, setRating] = useState(-1);
    let [clicked, setClicked] = useState(false);

    const { register, handleSubmit, errors, getValues } = useForm();
    let [filename, setFileName] = useState("Upload a file");
    const [file, setFile] = useState(undefined);

    // hit api when clicked on add comment
    const addCommentDataFetch = (id) => {
        setaddOpen(!addOpen);
        let commVal = {
            cid: getCandidateId(),
            oi_id: id,
            type: 'GET'
        }
        if(!addOpen) {
            dispatch(getoiComment(commVal));
            comment_id = id;
        }
    };

    // add new comment
    const submitComment = (values) => {
        console.log(values)
        let new_values = {
          ...values,
          candidate_id: getCandidateId(),
          oi_pk: comment_id,
          type: "POST",
        };

        dispatch(getoiComment(new_values));
      };

    // fill starts of already rated courses
    const fillStarForCourse = (star) => {
        if(star === '*') return "icon-fullstar";
        else if(star === '+') return "icon-halfstar";
        else return "icon-blankstar";
    };

    // new rating
    const fillNewStar = (star) => {
        if (star <= rating) return "icon-fullstar";
        else return "icon-blankstar";
    };
    
    const setStars = (e, className = "blankstar") => {
        let data = typeof e == "number" ? e : parseInt(e.target.getAttribute("value")) - 1;
        let children = document.getElementsByClassName("rating-review")[0].children;
        for (let i = 0; i <= data; i++) {
            children[i].setAttribute("class", `icon-${className}`);
        }
    };

    const mouseOver = (e) => {
        setStars(4);
        setStars(e, "fullstar");
    };

    const mouseOut = (e) => (!clicked ? setStars(e) : null);
        const onClickEvent = (e, val = 0) => {
        setRating(
            parseInt(e.target.getAttribute("value"))
            ? parseInt(e.target.getAttribute("value"))
            : val
        );
        setStars(e, "fullstar");
        setClicked(true);
    };

    // for resume upload
    const getFile = (event) => {

        let fileName = event.target.files[0].name
        let fileUploadValue = fileUpload(event)

        console.log(fileUploadValue)

        if(fileUploadValue){
            setFileName(fileName);
            setFile(fileUploadValue)
        }
    }

    const onSubmit = async (values, event) => {
        try {
            values = { ...values, file: file };
            console.log(values)
            let response = await new Promise((resolve, reject) => {
                dispatch(uploadResumeForm({ values, resolve, reject }));
            });
            if (!response.error) {
                props.setUploadPopup(false);
                event.target.reset();
                Swal.fire({
                    icon: "success",
                    title: "Form Submitted Successfully"
                })
                setFile(undefined)
                setFileName("Upload a file");
            }
            else {
                Swal.fire({
                    icon: "error",
                    title: "Oops! <br> Something went wrong! Try Again"
                })
            }
        }
        catch {
            Swal.fire({
                icon: "error",
                title: "Something went wrong! Try Again"
            })
        }
    };

    
    

    useEffect(() => {
        handleEffects();
    }, [])
    
    const handleEffects = async () => {
        try {
            //You may notice that apis corresponding to these actions are not getting called on initial render.
            //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
            //So there is no need to fetch them again on the browser.
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardServicesPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyServices({ resolve, reject })))
                dispatch(stopDashboardServicesPageLoader());
            }
            else {
                //isServerRendered is needed to be deleted because when routing is done through react and not on the node,
                //above actions need to be dispatched.
                delete window.config?.isServerRendered
            }
        } catch (error) {
            if (error?.status == 404) {
                history.push('/404');
            }
        }
    };

    return(
        <div>
            {serviceLoader ? <Loader /> : ''}
            <div className="my-courses-detail">

            {results?.data && results?.data.length > 0 ?
                results.data.map((item, index) => {
                    return (
                        <div className="db-white-box w-100" key={index}>
                            <div className="d-flex">
                                <figure>
                                    <img src={item.img} alt={item.img_alt} />
                                </figure>

                                <div className="my-courses-detail--wrap">
                                    <div className="d-flex w-100">
                                        <div className="my-courses-detail__leftpan">
                                            <div className="my-courses-detail__leftpan--box">
                                                <h3><Link to={item.url}>{item.heading}</Link></h3>
                                                <div className="my-courses-detail__leftpan--info">
                                                    <span>Provider: <strong>{item.provider}</strong> </span>
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
                                                                    <div className="upload-btn-wrapper">
                                                                        {/* <button className="btn btn-outline-primary">Upload a file</button> */}
                                                                        <form onSubmit={handleSubmit(onSubmit)}>
                                                                            <div className="form-group d-flex align-items-center mt-5">
                                                                                <div className="upload-btn-wrapper">
                                                                                    <button className="btn btn-outline-primary" >{filename}</button>
                                                                                    <input
                                                                                        type="file"
                                                                                        name="file"
                                                                                        onChange={(e) => {
                                                                                            e.preventDefault();
                                                                                            getFile(e)
                                                                                        }}
                                                                                        ref={register()}
                                                                                    />
                                                                                </div>
                                                                            </div>
                                                                            <div>
                                                                                <span>
                                                                                    {errors.shine_resume &&
                                                                                        "* Either Upload Resume or use shine resume"}
                                                                                </span>
                                                                            </div>
                                                                        </form>
                                                                    </div>

                                                                    <span className="mx-4">Or</span>

                                                                    <div className="custom-control custom-checkbox">
                                                                        <input type="checkbox" className="custom-control-input" id="shineResume" /> 
                                                                        <label className="custom-control-label font-weight-bold" htmlFor="shineResume">Use shine resume</label>
                                                                    </div>
                                                                </div>
                                                                <hr className="my-5"/>

                                                                <div className="db-upload-resume--services">
                                                                    <strong>Select services</strong> for which you want to use this resume
                                                                    <ul className="db-upload-resume--list">
                                                                        <li className="custom-control custom-checkbox">
                                                                            <input type="checkbox" className="custom-control-input" id="resumeBooster" /> 
                                                                            <label className="custom-control-label font-weight-bold" htmlFor="resumeBooster">Resume Booster 5-10 years</label>
                                                                        </li>

                                                                        <li className="custom-control custom-checkbox">
                                                                            <input type="checkbox" className="custom-control-input" id="resumeBuilder" /> 
                                                                            <label className="custom-control-label font-weight-bold" htmlFor="resumeBuilder">Resume Builder 5-10 yrs</label>
                                                                        </li>

                                                                        <li className="custom-control custom-checkbox">
                                                                            <input type="checkbox" className="custom-control-input" id="services" /> 
                                                                            <label className="custom-control-label font-weight-bold" htmlFor="services">For all services</label>
                                                                        </li>
                                                                    </ul>
                                                                </div>

                                                                <button className="btn btn-primary px-5 mt-30" onClick={handleSubmit(onSubmit)}>Save</button>
                                                            </div>
                                                        </Modal.Body>
                                                    </Modal>
                                                </div>

                                                <Link 
                                                    to={'#'}
                                                    className="font-weight-bold"
                                                    onClick={() => toggleDetails(item.id)}
                                                    aria-controls="addComments"
                                                    aria-expanded={`openViewDetail`+index}
                                                >
                                                    View Details
                                                </Link>

                                                <Collapse in={isOpen == item.id}>
                                                    <div className="view-detail arrow-box left-big" id={`openViewDetail`+index}>
                                                    <span className="btn-close"  onClick={() => toggleDetails(item.id)}>&#x2715;</span>
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
                                            to={"#"}
                                            className="db-comments font-weight-bold"
                                            onClick={() => addCommentDataFetch(item.id)}
                                            aria-controls="addComments"
                                            aria-expanded={addOpen}
                                        >
                                            Add comment
                                        </Link>

                                        <div className="d-flex">
                                            <div className="card__rating">
                                                {item.stars === null ?
                                                    <span 
                                                        className="cursor-pointer mr-2 font-weight-bold"
                                                        onClick={handleShow}
                                                    >
                                                        Rate Services
                                                    </span>
                                                : null
                                                }
                                                <span className="rating">
                                                    {item.stars.map((val,ind) => {
                                                        return (
                                                            <i
                                                            key={ind}
                                                            value={val}
                                                            className={fillStarForCourse(val)}
                                                            ></i>
                                                        );
                                                    })}
                                                </span>
                                                {item.stars != null && item.stars.length > 0 ? 
                                                    <React.Fragment>
                                                        <span>{item.rating}/5</span> 
                                                        <Link 
                                                            className="ml-15"
                                                            onClick={() => toggleReviews(item.id)}
                                                            aria-controls="threeComments"
                                                            aria-expanded={`openReview` + index}
                                                            to={'#'}
                                                        >
                                                            <strong>{item.review}</strong> { item.review > 1 ? 'Reviews' : 'Review' }
                                                        </Link>

                                                        <Collapse in={openReview == item.id}>
                                                            <div className="reviews-list-wrap arrow-box top-big">
                                                                <span className="btn-close"  onClick={() => toggleReviews(item.id)}>&#x2715;</span>
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
                                                                    </ul>
                                                                </div>
                                                                
                                                                <div className="reviews-list-wrap--bottom">
                                                                    <button className="btn btn-outline-primary" onClick={handleShow}>Add new</button>
                                                                </div>
                                                            </div>
                                                        </Collapse>
                                                    </React.Fragment>
                                                : null}
                                            </div>

                                            <Modal show={show} onHide={handleClose}>
                                                <Modal.Header closeButton>
                                                </Modal.Header>
                                                <Modal.Body>
                                                    <div className="text-center rate-services need-help">
                                                        <img src="/media/images/rate-services.png" className="img-fluid" alt=""/>
                                                        <p className="rate-services--heading">Rate service</p>
                                                        
                                                        <span className="rating-review">
                                                        {[1, 2, 3, 4, 5].map((value,indx) => {
                                                                return (
                                                                    <i
                                                                    key={indx}
                                                                    value={value}
                                                                    className={fillNewStar(value)}
                                                                    onMouseOver={(e) => mouseOver(e)}
                                                                    onMouseOut={(e) => mouseOut(e)}
                                                                    onClick={(e) => onClickEvent(e)}
                                                                    ></i>
                                                                );
                                                            })}
                                                        </span>
                                                        <p className="rate-services--subheading">Click on rate to scale of 1-5</p>
                                                        <form action="">
                                                            <div className="form-group error">
                                                                <input type="email" className="form-control" id="email" name="email" placeholder=" "
                                                                    value="" aria-required="true" aria-invalid="true" />
                                                                <label htmlFor="">Email</label>
                                                                <span className="error-msg">Required</span>
                                                            </div>
                                                            
                                                            <div className="form-group">
                                                                <textarea  className="form-control" name="review" id="review" cols="30" rows="3" placeholder=" "></textarea>
                                                                <label htmlFor="">Review</label>
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

                            {/* add comment dropdown */}
                            <Collapse in={addOpen}>
                                <div className="position-relative" id="threeComments">
                                    <div className="db-add-comments lightblue-bg border-bottom-gray">
                                        <span className="btn-close"  onClick={() => setOpen(!open)}>&#x2715;</span>
                                        <ul className="db-timeline-list">
                                            {results.oi_comment && results.oi_comment.length > 0 ?
                                                results.oi_comment.map((comm,index) => {
                                                    return (
                                                        <li>
                                                            <i className="db-timeline-list--dot"></i>
                                                            <span>{comm.comment.created} {comm.comment.addedBy != "" ?  '   |   By ' + comm.comment.addedBy : ""} </span>
                                                            <p className="db-timeline-list--text">{comm.comment.message ? comm.comment.message : ""}</p>
                                                        </li>
                                                    )
                                                })
                                                : null
                                            }
                                            
                                        </ul>
                                    </div>
                                
                                    <form onSubmit={handleSubmit(submitComment())}>
                                        <div className="db-add-comments disabled-before lightblue-bg">
                                            <p className="font-weight-semi-bold"> Add comment </p>
                                            <textarea class="form-control" rows="3"></textarea>
                                            <button type="submit" class="btn btn-outline-primary mt-20 px-5">Submit</button>
                                        </div>
                                    </form>
                                </div>
                                {/* <form onSubmit={handleSubmit(submitComment())}>
                                    <div className="db-add-comments lightblue-bg" id="addComments">
                                        <span className="btn-close" onClick={() => setaddOpen(!addOpen)}>&#x2715;</span>
                                        <p className="font-weight-semi-bold"> Add comment </p>
                                        <textarea className="form-control" rows="3"></textarea>
                                        <button type="submit" className="btn btn-outline-primary mt-20 px-5">Submit</button>
                                    </div>
                                </form> */}
                            </Collapse>
                        </div>
                    )
                })
            : null
            }
            </div>
        </div>
    )
}
   
export default MyServices;