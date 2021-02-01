// React Core Import
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import Swal from 'sweetalert2';
import { Link } from 'react-router-dom';

// Local Import 
import '../MyCourses/myCourses.scss'
import './myServices.scss';
import AddCommentModal from '../InboxModals/addCommentModal';
import RateProductModal from '../InboxModals/rateProductModal';
import UploadResume from '../InboxModals/uploadResume';
import AcceptModal from '../InboxModals/acceptModal';
import RejectModal from '../InboxModals/rejectModal';
import Loader from '../../../Common/Loader/loader';
import Pagination from '../../../Common/Pagination/pagination';
import EmptyInbox from '../InboxModals/emptyInbox';
import { siteDomain } from 'utils/domains';
import { startDashboardServicesPageLoader, stopDashboardServicesPageLoader } from 'store/Loader/actions/index';

// API Import
import { fetchMyServices, fetchPendingResume } from 'store/DashboardPage/MyServices/actions/index';
import { pausePlayResume } from 'store/DashboardPage/MyServices/actions/index';

const MyServices = (props) => {

    const dispatch = useDispatch();
    const { serviceLoader } = useSelector(store => store.loader);

    //My Services Api hit
    const handleEffects = async () => {
        try{
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardServicesPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyServices({page: currentPage, resolve, reject })));
                dispatch(stopDashboardServicesPageLoader());
            }
            else {
                delete window.config?.isServerRendered
            }
        }
        catch(e){
            dispatch(stopDashboardServicesPageLoader());
            Swal.fire({
                icon: 'error',
                text: 'Sorry! we are unable to fecth your data.'
            })
        }
    };

    //Data fetch from myservices API
    const serviceData= useSelector(store => store?.dashboardServices);
    const pending_resume_items = useSelector(store => store.dashboardPendingResume.data);
    const myServicesList = serviceData?.data
    const page = serviceData?.page

    //Pagination Handling
    const [currentPage, setCurrentPage] = useState(1)
    
    // File Upload Modal Handling
    const [showUpload, setShowUpload] = useState(false)

    //Comment Modal Handling
    const [showCommentModal, setShowCommentModal] = useState(false) 
    const [oiCommentId, setOiCommentId] = useState('')

    //Rate Modal Handling
    const [showRateModal, setShowRateModal] = useState(false) 
    const [oiReviewId, setOiReviewId] = useState('')
    
    //Accept Modal Handling
    const [acceptModal, setAcceptModal] = useState(false)
    const [acceptModalId, setAcceptModalId] = useState(false)

    //Reject Modal Handling
    const [rejectModal, setRejectModal] = useState(false)
    const [rejectModalId, setRejectModalId] = useState(false)

    //View Details Handling
    const [showOrderDetailsID, setShowOrderDetailsID] = useState('')
    const showDetails = (id) => {
        id == showOrderDetailsID ?
            setShowOrderDetailsID('') : setShowOrderDetailsID(id)
    }

    //Pause service
    const pauseResumeService = (oiStatus, orderId) => {
        let pausePlayValues = {
            oi_status: oiStatus,
            order_item_id: orderId
        }
        dispatch(pausePlayResume(pausePlayValues))
    }

    //View Details Data
    const getOrderDetails = (dataList) => {
        return (
            <ul className="my-order__order-detail--info mt-15">
                {
                    dataList.map((data, index) =>
                        <li key={index}>
                            <span> 
                                <hr />
                                {data?.date} <br />
                                <strong> {data?.status} </strong>
                            </span>
                        </li>)
                }
            </ul>
        )
    }

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+' 
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    useEffect(() => {

        //On New page it will scroll to top smoothly
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth"
        });

        handleEffects();
        dispatch(fetchPendingResume())
    }, [currentPage])

    return (
        <>
        { serviceLoader && <Loader />}
        {
            page?.total === 0 ? <EmptyInbox inboxType="services" /> :

        <div>
            {/* Pending resume block Start*/}
            {
                myServicesList?.length > 0 && pending_resume_items?.length > 0 &&
                    <div>
                        <strong>
                            <center>To initiate your service <br />
                                <a href="/" onClick={(e) => {e.preventDefault();setShowUpload(true)}}>
                                    Upload your latest resume
                                </a>
                            </center>
                        </strong>
                        <br />
                    </div>
            }
            {/* Pending resume block End*/}

            {/* My Services Block Start */}
            <main className="mb-0">
                <div className="m-courses-detail db-warp">
                    {
                        myServicesList?.map((service, key) => {
                            return (
                                <div className="m-card pl-0" key={key}>
                                    {/* Social Sharing Block Start */}
                                    <div className="m-share" aria-haspopup="true">
                                        <i className="icon-share"></i>
                                        <div className="m-share__box m-arrow-box m-top">
                                            <a target="_blank" href={`https://www.facebook.com/sharer/sharer.php?u=${siteDomain}${service?.productUrl}`} className="m-facebook-icon"></a>
                                            <a target="_blank" href={`https://www.linkedin.com/shareArticle?mini=true&url=${siteDomain}${service?.productUrl}&title=${service?.title}&summary=${service?.name}&source=`} className="m-linkedin-icon"></a>
                                            <a target="_blank" href={`https://twitter.com/intent/tweet?url=${siteDomain}${service?.productUrl}/&text=${service?.name}`} className="m-twitter-iocn"></a>
                                            <a target="_blank" href={`https://api.whatsapp.com/send?text=Hi! Check this useful product on Shine. ${siteDomain}${service?.productUrl}`} data-action="share/whatsapp/share" className="m-whatsup-icon"></a>
                                        </div>
                                    </div>
                                    {/* Social Sharing Block End */}

                                    {/* Details of Service Block Start*/}
                                    <div className="d-flex">
                                        <figure>
                                            <img src={service?.img} alt={service?.heading} />
                                        </figure>
                                        <div className="m-courses-detail__info">
                                            <Link to={service?.productUrl}><h2>{service?.name}</h2></Link>
                                            <p className="m-pipe-divides mb-5">Provider: <strong>{service?.vendor}</strong> </p>
                                            <p className="m-pipe-divides mb-5">
                                                <span>Bought on: <strong>{service?.enroll_date}</strong> </span> 
                                                {
                                                    service?.duration_in_days && 
                                                    <span>Duration: <strong>{service?.duration_in_days > 1 ? service?.duration_in_days + ' days' : service?.duration_in_days + ' day' } </strong> </span>
                                                }
                                            </p>
                                        </div>
                                    </div>
                                    {/* Details of Service Block End*/}

                                    { service?.options?.upload_resume &&
                                        <div className="m-courses-detail--alert mt-15">
                                            To initiate your service upload your latest resume
                                        </div>
                                    }
                                    
                                    {/* Status of Service Block */}
                                    <div className="pl-15 mt-15 fs-12">
                                        Status: <strong> {service?.new_oi_status ? service?.oi_status === 4 ? 'Service has been processed and Document is finalized' : service?.new_oi_status : "Yet to Update"}

                                        {
                                            service?.options?.upload_resume && <a href="/" onClick={(e) => {e.preventDefault();setShowUpload(true)}} className="font-weight-bold"> Upload</a> 
                                        }
                                        {
                                            service?.options?.Download && <a href={service?.options?.download_url} target="_blank" className="font-weight-bold"> Download</a> 
                                        }
                                        {
                                            service?.options?.Download_credential && <a href={service?.options?.download_url} target="_blank" className="font-weight-bold"> Download Credential</a> 
                                        }
                                        {
                                            service?.options?.edit_your_profile && <a href={`${siteDomain}/dashboard/roundone/profile/`} target="_blank" className="font-weight-bold"> Edit Profile</a>
                                        }
                                        {
                                            service?.options?.complete_profile && <a href={`${siteDomain}/dashboard/roundone/profile/`} target="_blank" className="font-weight-bold"> Complete Profile</a>
                                        }
                                        {
                                            (service?.oi_status === 24 || service?.oi_status === 46) &&
                                            <>
                                                <br /><br />
                                                <a className="m-accept" href="/" onClick={(e) => {e.preventDefault();setAcceptModal(true);setAcceptModalId(service?.id)}}>Accept</a>
                                                <a className="ml-2 m-reject" href="/" onClick={(e) => {e.preventDefault();setRejectModal(true);setRejectModalId(service?.id)}}>Reject</a>
                                            </>
                                        }
                                        </strong>

                                        {/* View Details Block */}
                                        {
                                            service?.datalist?.length > 0 &&
                                                <div className="my-order__order-detail">
                                                    <a onClick={(e) => {
                                                            e.preventDefault();
                                                            showDetails(service?.id)
                                                        }} 
                                                        className={(showOrderDetailsID === service?.id) 
                                                            ? "font-weight-bold open arrow-icon" : "font-weight-bold arrow-icon"
                                                        }> View Details
                                                    </a>
                                                    {
                                                        (showOrderDetailsID === service?.id) && getOrderDetails(service?.datalist)
                                                    }
                                                </div>
                                        }
                                    </div>
                                    {/* End of Status Service Block */}

                                    <div className="pl-15">

                                        {/* Days Reamianing and Start Stop Service Block */}
                                        <div className="m-courses-detail__bottomWrap">
                                            <div>
                                                <div className="m-day-remaning">
                                                    {
                                                        service?.remaining_days?.toString()?.split('')?.map((digit, index) => {
                                                            return (
                                                                <span className="m-day-remaning--box" key={index}> { digit }</span>
                                                            )
                                                        })
                                                    }
                                                    <span className="ml-2 m-day-remaning--text">
                                                        { service?.remaining_days > 1 ? 'Days' : 'Day'} <br />remaining
                                                    </span>
                                                </div>
                                            </div>
                                            {
                                                service?.options?.pause_service && <Link to={"#"} className="m-db-start-course font-weight-bold pr-10" onClick={() => pauseResumeService(34, service?.id)}>Pause Service</Link>
                                            }
                                            {
                                                service?.options?.resume_service && <Link to={"#"} className="m-db-start-course font-weight-bold pr-10" onClick={() => pauseResumeService(35, service?.id)}>Resume Service</Link>
                                            }
                                        </div>
                                        
                                        {/* Comment and Rating Block start */}
                                        <div className="m-courses-detail__userInput">

                                            {/* Comment Block start */}
                                            <Link to={'#'} onClick={(e) => {
                                                    e.preventDefault();
                                                    setShowCommentModal(true);
                                                    setOiCommentId(service?.id)
                                                }} 
                                                className="m-db-comments font-weight-bold">
                                                { 
                                                    service?.no_of_comments ? 
                                                        service?.no_of_comments > 1 ? 
                                                            `${service?.no_of_comments} Comments` : 
                                                            `${service?.no_of_comments} Comment` : 'Add Comment' 
                                                }
                                            </Link>
                                            {/* Comment Block end */}

                                            {/* Rating Block start*/}    
                                            {
                                                (service?.oi_status === 4) && 
                                                    <div className="d-flex" onClick={()=>{
                                                            setShowRateModal(true);
                                                            setOiReviewId(service?.product)
                                                        }} id={service?.product} >
                                                        {
                                                            service?.no_review ?
                                                                <>
                                                                    <span className="m-rating">
                                                                        {
                                                                            service?.rating?.map((star, index) => starRatings(star, index))
                                                                        }
                                                                        <span className="ml-5">
                                                                            { service?.avg_rating?.toFixed(1) }/5 
                                                                        </span>
                                                                    </span>

                                                                    <Link to={"#"} className="font-weight-bold ml-10">
                                                                        { service?.no_review }
                                                                    </Link>
                                                                </> : 
                                                                <>
                                                                    <span className="">Rate</span>
                                                                    <span className="m-rating">
                                                                        {
                                                                            [1, 2, 3, 4, 5].map((item, index) => {
                                                                                return <em className="micon-blankstar" key={index} />
                                                                            })
                                                                        }
                                                                    </span>
                                                                </>
                                                        }
                                                    </div>
                                            }
                                            {/* Rating Block start*/}  
                                                    
                                        </div>
                                        {/* Comment and Rating Block end */}
                                    </div>

                                </div>
                            )
                        })
                    }
                </div>

            </main>
            {/* My Services Block End */}
            
            {/* Comment Modal */}
            { showCommentModal && <AddCommentModal setShowCommentModal = {setShowCommentModal} oi_id={oiCommentId} /> }

            {/* Rate Modal */}
            { showRateModal && <RateProductModal setShowRateModal={setShowRateModal} oi_id={oiReviewId}/> }

            {/* Upload Modal */}
            { showUpload && <UploadResume setShowUpload={setShowUpload} data={pending_resume_items} /> }

            {/* Accept Reject Modal */}
            { acceptModal && <AcceptModal setAcceptModal={setAcceptModal} oi_id={acceptModalId}/> }
            { rejectModal && <RejectModal setRejectModal={setRejectModal} oi_id={rejectModalId}/> }

            {/* Pagination */}
            { page?.total > 1 && <Pagination totalPage={page?.total} currentPage={currentPage} setCurrentPage={setCurrentPage} /> }

        </div>
        }
        </>
    )
}


export default MyServices;