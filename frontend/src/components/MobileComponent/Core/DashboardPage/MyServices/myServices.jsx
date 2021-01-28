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
import Loader from '../../../Common/Loader/loader';
import Pagination from '../../../Common/Pagination/pagination';
import { startDashboardServicesPageLoader, stopDashboardServicesPageLoader } from 'store/Loader/actions/index';
import { siteDomain } from 'utils/domains';
import AcceptModal from '../InboxModals/acceptModal';
import RejectModal from '../InboxModals/rejectModal';

// API Import
import { fetchMyServices, fetchPendingResumes } from 'store/DashboardPage/MyServices/actions/index';

const MyServices = (props) => {

    const dispatch = useDispatch();
    const serviceData= useSelector(store => store?.dashboardServices);
    const { serviceLoader } = useSelector(store => store.loader);
    const myServicesList = serviceData?.data
    const page = serviceData?.page
    
    const [showUpload, setShowUpload] = useState(false)
    const [showCommentModal, setShowCommentModal] = useState(false) 
    const [showRateModal, setShowRateModal] = useState(false) 
    const [showOrderDetailsID, setShowOrderDetailsID] = useState('')
    const [currentPage, setCurrentPage] = useState(1)
    const [oiCommentId, setOiCommentId] = useState('')
    const [oiReviewId, setOiReviewId] = useState('')
    const [acceptModal, setAcceptModal] = useState(false)
    const [acceptModalId, setAcceptModalId] = useState(false)
    const [rejectModal, setRejectModal] = useState(false)
    const [rejectModalId, setRejectModalId] = useState(false)
    

    const showDetails = (id) => {
        id == showOrderDetailsID ?
            setShowOrderDetailsID('') : setShowOrderDetailsID(id)
    }

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

    const handleEffects = async () => {
        try{
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardServicesPageLoader());
                new Promise((resolve, reject) => dispatch(fetchPendingResumes({ resolve, reject })));
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

    useEffect(() => {
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth"
        });
        handleEffects();
    }, [currentPage])

    return (
        <>
        { serviceLoader && <Loader />}
        <div>
            {
                serviceData?.pending_resume_items &&
                    <div>
                        <strong><center>To initiate your service <br /><a href="/" onClick={(e) => {e.preventDefault();setShowUpload(true)}}>Upload your latest resume</a></center></strong><br />
                    </div>
            }

            <main className="mb-0">
                <div className="m-courses-detail db-warp">
                    {
                        myServicesList?.map((service, key) => {
                            return (
                                <div className="m-card pl-0" key={key}>
                                    <div className="m-share" aria-haspopup="true">
                                        <i className="icon-share"></i>
                                        <div className="m-share__box m-arrow-box m-top">
                                            <a target="_blank" href={`https://www.facebook.com/sharer/sharer.php?u=${siteDomain}${service?.productUrl}`} className="m-facebook-icon"></a>
                                            <a target="_blank" href={`https://www.linkedin.com/shareArticle?mini=true&url=${siteDomain}${service?.productUrl}&title=${service?.title}&summary=${service?.name}&source=`} className="m-linkedin-icon"></a>
                                            <a target="_blank" href={`https://twitter.com/intent/tweet?url=${siteDomain}${service?.productUrl}/&text=${service?.name}`} className="m-twitter-iocn"></a>
                                            <a target="_blank" href={`https://api.whatsapp.com/send?text=Hi! Check this useful product on Shine. ${siteDomain}${service?.productUrl}`} data-action="share/whatsapp/share" className="m-whatsup-icon"></a>
                                        </div>
                                    </div>

                                    <div className="d-flex">
                                        <figure>
                                            <img src={service?.img} alt={service?.heading} />
                                        </figure>
                                        <div className="m-courses-detail__info">
                                            <Link to={service?.productUrl}><h2>{service?.name}</h2></Link>
                                            <p className="m-pipe-divides mb-5">Provider: <strong>{service?.vendor}</strong> </p>
                                            <p className="m-pipe-divides mb-5"><span>Bought on: <strong>{service?.enroll_date}</strong> </span> {service?.oi_duration && <span>Duration: <strong>{service?.oi_duration > 1 ? service?.oi_duration + ' days' : service?.oi_duration + ' day' } </strong> </span>}</p>
                                        </div>
                                    </div>

                                    { service?.options?.upload_resume &&
                                        <div className="m-courses-detail--alert mt-15">
                                            To initiate your service upload your latest resume
                                        </div>
                                    }

                                            <div className="pl-15 mt-15 fs-12">
                                                Status: <strong> {service?.status ? service?.status : service?.new_oi_status} </strong>
                                                {
                                                    false &&
                                                        <div className="d-flex justify-content-center mt-10">
                                                            <button className="btn-blue mr-20" onClick={() => {setAcceptModal(true);setAcceptModalId(service?.id)}}>
                                                                Accept
                                                            </button>{" "}
                                                            <button className="btn-blue ml-20" onClick={() => {setRejectModal(true);setRejectModalId(service?.id)}}>
                                                                Reject
                                                            </button>
                                                        </div>
                                                }

                                                {
                                                    service?.options?.upload_resume && <a href="/" onClick={(e) => {e.preventDefault();setShowUpload(true)}} className="font-weight-bold">Upload</a> 
                                                }
                                                {
                                                    service?.options?.Download && <a href={service?.options?.download_url} target="_blank" className="font-weight-bold">Download</a> 
                                                }
                                                {
                                                    service?.datalist?.length ? 
                                                        <div className="my-order__order-detail">
                                                            <a onClick={(e) => {e.preventDefault();showDetails(service?.id)}} className={(showOrderDetailsID === service?.id) ? "font-weight-bold open arrow-icon" : "font-weight-bold arrow-icon"}>View Details</a>
                                                            { (showOrderDetailsID === service?.id) && getOrderDetails(service?.datalist) }
                                                            
                                                        </div> : ''
                                                }
                                            </div>
                                            <div className="pl-15">

                                            <div className="m-courses-detail__bottomWrap">
                                                <div>
                                                    <div className="m-day-remaning">
                                                        {
                                                            service.remaining_days.toString().split('').map((digit, index) => {
                                                                return (
                                                                    <span className="m-day-remaning--box" key={index}> { digit }</span>
                                                                )
                                                            })
                                                        }
                                                        <span className="ml-2 m-day-remaning--text">{ service?.remaining_days > 1 ? 'Days' : 'Day'}<br />remaining</span>
                                                    </div>
                                                </div>
                                                {/* <Link to={"#"} className="m-db-start-course font-weight-bold pr-10">Start Service</Link> */}
                                            </div>

                                                <div className="m-courses-detail__userInput">
                                                    <Link to={'#'} onClick={(e) => {e.preventDefault();setShowCommentModal(true);setOiCommentId(service?.id)}} className="m-db-comments font-weight-bold">
                                                        { service?.no_of_comments ? service?.no_of_comments > 1 ? `${service?.no_of_comments} Comments` : `${service?.no_of_comments} Comment` : 'Add Comment' }
                                                    </Link>
                                                    
                                                    <div className="d-flex" onClick={()=>{setShowRateModal(true);setOiReviewId(service?.product)}} id={service?.product}>
                                                        {
                                                            service?.no_review ?
                                                                <>
                                                                    
                                                                        <span className="m-rating">
                                                                            { service?.rating?.map((star, index) => starRatings(star, index)) }
                                                                            <span className="ml-5">{service?.avg_rating?.toFixed(1)}/5</span>
                                                                        </span>
                                                                        <Link to={"#"} className="font-weight-bold ml-10">{ service?.no_review }</Link>
                                                                    
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
                                                </div>
                                            </div>

                                </div>
                            )
                        })
                    }
                </div>
                
            </main>
            {
                showCommentModal && <AddCommentModal setShowCommentModal = {setShowCommentModal} oi_id={oiCommentId} />
            }
            {
                showRateModal && <RateProductModal setShowRateModal={setShowRateModal} oi_id={oiReviewId}/>
            }
            {
                showUpload && <UploadResume setShowUpload={setShowUpload} data={serviceData?.pending_resume_items} />
            }
            {
                acceptModal && <AcceptModal setAcceptModal={setAcceptModal} oi_id={acceptModalId}/>
            }
            {
                rejectModal && <RejectModal setRejectModal={setRejectModal} oi_id={rejectModalId}/>
            }
            {
                page?.total > 1 ? 
                    <Pagination 
                        totalPage={page?.total}
                        currentPage={currentPage}
                        setCurrentPage={setCurrentPage} /> : ''
            }
        </div>
        </>
    )
}


export default MyServices;