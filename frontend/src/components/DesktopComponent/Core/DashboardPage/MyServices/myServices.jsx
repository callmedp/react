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
import { fetchMyServices, getoiComment,fetchMyReview } from 'store/DashboardPage/MyServices/actions';
import { useForm } from "react-hook-form";
import Swal from 'sweetalert2';
import {getCandidateId} from 'utils/storage';
import UploadResumeModal from '../Inbox/uploadResumeModal';
import ViewDetailModal from '../Inbox/viewDetailModal';
import RateModal from '../Inbox/rateModal';
import ReviewRating from '../Inbox/reviewRating';
import AddCommentModal from '../Inbox/addCommentModal';

const MyServices = (props) => {
    let servPage = '3';
    const [addOpen, setaddOpen] = useState(false);
    
    // const [open, setOpen] = useState(false);
    const [openReview, setOpenReview] = useState(false);
    const toggleReviews = (id) => {
        new Promise((resolve, reject) => dispatch(fetchMyReviews({ data: id, resolve, reject })));
        setOpenReview(openReview == id ? false : id);
    }

    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    
    // const [rejectShow, setRejectShow] = useState(false);
    // const rejectHandelClose = () => setRejectShow(false);
    // const rejectHandelShow = () => setRejectShow(true);
    
    const [uploadShow, setUploadShow] = useState(false);
    const uploadHandelClose = () => setUploadShow(false);
    const uploadHandelShow = () => setUploadShow(true);

    const results = useSelector(store => store.dashboardServices.data);
    const oiComments = useSelector(store => store.dashboardServices.oi_comment);

    const dispatch = useDispatch();
    const { history } = props;
    const { serviceLoader } = useSelector(store => store.loader);

    const [isOpen, setIsOpen] = useState(false);
    const toggleDetails = (id) => setIsOpen(isOpen == id ? false : id);

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
                await new Promise((resolve, reject) => dispatch(fetchMyServices({ page: servPage, resolve, reject })))
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
                                                        <strong className="ml-1">{item.status}
                                                            <Link to={"#"} className="ml-2" onClick={uploadHandelShow}>Upload</Link> 
                                                        </strong> 

                                                        <UploadResumeModal uploadHandelClose={uploadHandelClose} show={uploadShow} data={results.pending_resume_items} />
                                                    </div>

                                                    {item.datalist && item.datalist.length > 0 ?
                                                        <Link 
                                                            to={'#'}
                                                            className="font-weight-bold"
                                                            onClick={() => toggleDetails(item.id)}
                                                            aria-controls="addComments"
                                                            aria-expanded={`openViewDetail`+item.id}
                                                        >
                                                            View Details
                                                        </Link>
                                                        : null 
                                                    }

                                                    {/* course detail modal open */}
                                                    <ViewDetailModal id={item.id} toggleDetails={toggleDetails} isOpen={isOpen} data={item.datalist}/>
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
                                                aria-expanded={`openComment`+item.id}
                                            >
                                                Add comment
                                            </Link>

                                            {/* ratings start here */}
                                            <div className="d-flex">
                                                <ReviewRating
                                                    item={item}
                                                    handleShow={handleShow}
                                                    toggleReviews={toggleReviews} 
                                                    setOpenReview={setOpenReview}
                                                    openReview={openReview}
                                                    name="Service"/>

                                                {/* rate service modal */}
                                                <RateModal handleClose={handleClose} show={show} name="Service"/>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                {/* add comment dropdown */}
                                {oiComments ? <AddCommentModal id={item.id} data={oiComments[0]} addOpen={addOpen} /> : null }
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