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
import { fetchMyServices, getoiComment,fetchMyReviews } from 'store/DashboardPage/MyServices/actions';
import { useForm } from "react-hook-form";
import Swal from 'sweetalert2';
import {getCandidateId} from 'utils/storage';
import UploadResumeModal from '../Inbox/uploadResumeModal';
import ViewDetailModal from '../Inbox/viewDetailModal';
import RateModal from '../Inbox/rateModal';
import ReviewRating from '../Inbox/reviewRating';
import AddCommentModal from '../Inbox/addCommentModal';
import Pagination from '../../../Common/Pagination/pagination';

const MyServices = (props) => {
    const dispatch = useDispatch();
    const { history } = props;
    const { serviceLoader } = useSelector(store => store.loader);
    // page no. set here
    const [currentPage, setCurrentPage] = useState(1)

    // main service api hit
    const handleEffects = async () => {
        try {
            //You may notice that apis corresponding to these actions are not getting called on initial render.
            //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
            //So there is no need to fetch them again on the browser.
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardServicesPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyServices({ page: currentPage, resolve, reject })))
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


    // review open close set here
    const [openReview, setOpenReview] = useState(false);
    const [show, setShow] = useState(false);
    
    // if reviews exists then show
    const toggleReviews = (id, prod) => {

        if(openReview != id) new Promise((resolve, reject) => dispatch(fetchMyReviews({ prod: prod, page: currentPage, type: 'GET', resolve, reject })));

        setOpenReview(openReview == id ? false : id);
    }

    // if view detail then show
    const [isOpen, setIsOpen] = useState(false);
    const toggleDetails = (id) => setIsOpen(isOpen == id ? false : id);

    // if upload then show
    const [uploadShow, setUploadShow] = useState(false);
    const uploadHandelClose = () => setUploadShow(false);
    const uploadHandelShow = () => setUploadShow(true);

    // main api result state here
    const results = useSelector(store => store.dashboardServices);
    const setProductReview = useSelector(store => store.dashboardServices.reviews);
    const oiComments = useSelector(store => store.dashboardServices.oi_comment);

    // comment open close set here
    const [addOpen, setaddOpen] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    // hit api when clicked on add comment
    const addCommentDataFetch = (id) => {
        setaddOpen(addOpen == id ? false : id);
        
        let commVal = {
            oi_id: id,
            type: 'GET'
        }

        if(addOpen != id) dispatch(getoiComment(commVal));
    };

    // console.log(results)

    useEffect(() => {
        handleEffects();
    }, [currentPage])

    return(
        <div>
            {serviceLoader ? <Loader /> : ''}
            <div className="db-my-courses-detail">

            {
                results.pending_resume_items.length > 0 ? 
                    <div class="alert alert-primary py-4 px-5 fs-16 w-100 text-center mb-0" role="alert">To initiate your services.<span className="resume-upload--btn">&nbsp;<strong onClick={uploadHandelShow} className="cursor">Upload Resume</strong></span></div>
                : null
            }

                {results?.data && results.data.length > 0 ?
                    results.data.map((item,index) => {
                        return(
                            <div className="db-white-box w-100" key={index}>
                                <div className="d-flex">
                                    <figure>
                                        <img src={item.img} alt={item.img_alt} />
                                    </figure>

                                    <div className="db-my-courses-detail--wrap">
                                        <div className="d-flex w-100">
                                            <div className="db-my-courses-detail__leftpan">
                                                <div className="db-my-courses-detail__leftpan--box">
                                                    <h3><Link to={item.productUrl ? item.productUrl : '#'}>{item.heading}</Link></h3>
                                                    <div className="db-my-courses-detail__leftpan--info">
                                                        <span>Provider: <strong>{item.vendor}</strong> </span>
                                                        <span>Bought on: <strong>{item.enroll_date}</strong></span>
                                                        {item.duration ? <span>Duration: <strong>{item.duration}</strong></span> : "" }
                                                    </div>

                                                    <div className="db-my-courses-detail__leftpan--alert">
                                                        Hi, the recording for the session you missed is available now
                                                    </div>

                                                    <div className="db-my-courses-detail__leftpan--status mb-2">
                                                        Status:
                                                        <strong className="ml-1">{item.status}
                                                            {results.pending_resume_items.length > 0 ? <Link to={"#"} className="ml-2" onClick={uploadHandelShow}>Upload</Link>
                                                            : null}
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
                                                    {[...(item.remaining_days + '')].map((day, idx) => <span key={idx} className="day-remaning--box">{day}</span>)}
                                                    {/* <span className="day-remaning--box">9</span> */}
                                                    {/* <span className="day-remaning--box">0</span> */}
                                                    <span className="ml-2 day-remaning--text">Days <br/>remaning</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="db-my-courses-detail__bottom">
                                            {item.status !== 'Unpaid' ? <Link
                                                to={"#"}
                                                className="db-comments font-weight-bold"
                                                onClick={() => addCommentDataFetch(item.id)}
                                                aria-controls="addComments"
                                                aria-expanded={`openComment`+item.id}
                                            >
                                                Add comment
                                            </Link>
                                            : null}

                                            {/* ratings start here */}
                                            <div className="d-flex">
                                                <ReviewRating
                                                    item={item}
                                                    handleShow={handleShow}
                                                    toggleReviews={toggleReviews} 
                                                    setOpenReview={setOpenReview}
                                                    openReview={openReview}
                                                    setProductReview={setProductReview}
                                                    name="Service"/>

                                                {/* rate service modal */}
                                                <RateModal handleClose={handleClose} show={show} id={item.id} name="Service"/>
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

                {results?.page?.total > 1 ? <Pagination totalPage={results?.page?.total} currentPage={currentPage} setCurrentPage={setCurrentPage}/> : ''}

            </div>
        </div>
    )
}
   
export default MyServices;