import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ProgressBar } from 'react-bootstrap';
import { Collapse } from 'react-bootstrap';
import { Modal } from 'react-bootstrap';
import '../MyCourses/myCourses.scss';
import './myServices.scss';
import { startDashboardServicesPageLoader, stopDashboardServicesPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMyServices, uploadResumeForm, getoiComment,SubmitDashboardFeedback } from 'store/DashboardPage/MyServices/actions';
import { useForm } from "react-hook-form";
import fileUpload from "utils/fileUpload";
import Swal from 'sweetalert2';
import {getCandidateId} from 'utils/storage';
import {InputField, TextArea} from 'formHandler/desktopFormHandler/formFields';
import CoursesServicesForm from 'formHandler/desktopFormHandler/formData/coursesServices';

const MyServices = (props) => {
    const [addOpen, setaddOpen] = useState(false);
    
    const [open, setOpen] = useState(false);
    const [openReview, setOpenReview] = useState(false);
    const toggleReviews = (id) => setOpenReview(openReview == id ? false : id);

    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    
    const [rejectShow, setRejectShow] = useState(false);
    const rejectHandelClose = () => setRejectShow(false);
    const rejectHandelShow = () => setRejectShow(true);
    
    const [uploadShow, setUploadShow] = useState(false);
    const uploadHandelClose = () => setUploadShow(false);
    const uploadHandelShow = () => setUploadShow(true);

    const results = useSelector(store => store.dashboardServices.data);
    const dispatch = useDispatch();
    const { history } = props;
    const { serviceLoader } = useSelector(store => store.loader);

    const [isOpen, setIsOpen] = useState(false);
    const toggleDetails = (id) => setIsOpen(isOpen == id ? false : id);

    let [newRating, setRating] = useState(5);
    let [clicked, setClicked] = useState(false);

    const { register, handleSubmit, errors } = useForm();
    let [filename, setFileName] = useState("Upload a file");
    const [file, setFile] = useState(undefined);

    // hit api when clicked on add comment
    const addCommentDataFetch = (id) => {
        setaddOpen(addOpen == id ? false : id);
        
        let commVal = {
            cid: getCandidateId(),
            oi_id: id,
            type: 'GET'
        }
        if(!addOpen) dispatch(getoiComment(commVal));
    };

    // add new comment
    const submitComment = (values) => {
        console.log(values)
        const new_values = {
          ...values,
          candidate_id: getCandidateId(),
          oi_pk: results.oi_comment[0].oi_id,
          type: "POST",
        };

        dispatch(getoiComment(new_values));
    };

    // add new review
    const submitReview = (values) => {
        const new_review = {
            ...values,
            candidate_id: getCandidateId(),
            oi_pk: 503247,
            rating: newRating,
            full_name: (localStorage.getItem('first_name') || '') + (localStorage.getItem('last_name') || ''),
        };

        dispatch(SubmitDashboardFeedback(new_review));
    };

    // fill starts of already rated courses
    const fillStarForCourse = (star) => {
        if(star === '*') return "icon-fullstar";
        else if(star === '+') return "icon-halfstar";
        else return "icon-blankstar";
    };

    // new rating
    const fillNewStar = (star) => {
        if (star <= newRating) return "icon-fullstar";
        else return "icon-blankstar";
    };
    
    const setStars = (e, className = "blankstar") => {
        let data = typeof e == "number" ? e : parseInt(e.target.getAttribute("value")) - 1;
        let children = document.getElementsByClassName("rating-review")[0].children;
        console.log(data, children);
        for (let i = 0; i <= data; i++) {
            children[i].setAttribute("className", `icon-${className}`);
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
            // console.log(values)
            let response = await new Promise((resolve, reject) => {
                dispatch(uploadResumeForm({ values, resolve, reject }));
            });
            if (!response.error) {
                // props.setUploadPopup(false);
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

    console.log(results)

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
                {results?.data && results.data.length > 0 ?
                    results.data.map((item,index) => {
                        return(
                            <div className="db-white-box w-100" key={index}>
                                <div className="d-flex">
                                    <figure>
                                        <img src={item.img} alt={item.img_alt} />
                                    </figure>

                                    <div className="my-courses-detail--wrap">
                                        <div className="d-flex w-100">
                                            <div className="my-courses-detail__leftpan">
                                                <div className="my-courses-detail__leftpan--box">
                                                    <h3><Link to={item.productUrl ? item.productUrl : '#'}>{item.heading}</Link></h3>
                                                    <div className="my-courses-detail__leftpan--info">
                                                        <span>Provider: <strong>{item.vendor}</strong> </span>
                                                        <span>Bought on: <strong>{item.enroll_date}</strong></span>
                                                        <span>Duration: <strong>{item.duration ? item.duration : ""}</strong></span>
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
                                                            <Modal.Header closeButton></Modal.Header>
                                                            <Modal.Body>
                                                                <div className="text-center rate-services db-custom-select-form db-upload-resume">
                                                                    
                                                                </div>
                                                            </Modal.Body>
                                                        </Modal>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )
                    })
                    :null
                }
            </div>
        </div>
    )
}
   
export default MyServices;