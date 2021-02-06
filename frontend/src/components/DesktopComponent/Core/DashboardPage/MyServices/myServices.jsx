import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import '../MyCourses/myCourses.scss';
import './myServices.scss';
import { startDashboardServicesPageLoader, stopDashboardServicesPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMyServices, fetchPendingResume } from 'store/DashboardPage/MyServices/actions';
import { fetchOiComment } from 'store/DashboardPage/AddSubmitComment/actions/index';
import { fetchReviews } from 'store/DashboardPage/AddSubmitReview/actions/index';
import UploadResumeModal from '../Inbox/uploadResumeModal';
import ViewDetailModal from '../Inbox/viewDetailModal';
import RateModal from '../Inbox/rateModal';
import ReviewModal from '../Inbox/reviewModal';
import AddCommentModal from '../Inbox/addCommentModal';
import Pagination from '../../../Common/Pagination/pagination';
import AcceptModal from '../Inbox/acceptModal';
import RejectModal from '../Inbox/rejectModal';
import EmptyInbox from '../Inbox/emptyInbox';
import { startCommentLoader, stopCommentLoader, startUploadLoader, stopUploadLoader, startReviewLoader, stopReviewLoader } from 'store/Loader/actions/index';
import BreadCrumbs from '../Breadcrumb/Breadcrumb';
import { pausePlayResume } from 'store/DashboardPage/MyServices/actions/index';
import {siteDomain, resumeShineSiteDomain} from '../../../../../utils/domains';

const MyServices = (props) => {
    const dispatch = useDispatch();
    const { history } = props;
    const { serviceLoader } = useSelector(store => store.loader);
    
    // page no. set here
    const [currentPage, setCurrentPage] = useState(1);
    const [filterState, setfilterState] = useState({ 'last_month_from': 'all', 'select_type' : 'all' });
    
    // main api result state here
    const results = useSelector(store => store.dashboardServices);
    const oiComments = useSelector(store => store.getComment);
    const pending_resume_items = useSelector(store => store.dashboardPendingResume.data);

    // rating modal handling
    const [showRatingModal, setShowRatingModal] = useState(false) 
    const toggleRatingsModal = (id) => setShowRatingModal(showRatingModal == id ? false : id);
   
    //Rate Modal Handling
    const [showRateModal, setShowRateModal] = useState(false) 
    const [oiReviewId, setOiReviewId] = useState('');

    //set review data
    const [reviewData, setReviewData] = useState([]);

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+' 
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    // if view detail then show
    const [isOpen, setIsOpen] = useState(false);
    const toggleDetails = (id) => setIsOpen(isOpen == id ? false : id);

    // if upload then show
    const [uploadShow, setUploadShow] = useState(false);
    const uploadHandelClose = () => setUploadShow(false);

    const uploadToggleService = async () => {
        setUploadShow(true);
        dispatch(startUploadLoader());
        await new Promise((resolve, reject) => dispatch(fetchPendingResume({payload : {}, resolve, reject})));
        dispatch(stopUploadLoader());
    }

    // comment open close set here
    const [addOpen, setAddOpen] = useState(false);

    // accept/reject
    const [acceptModal, setAcceptModal] = useState(false)
    const [acceptModalId, setAcceptModalId] = useState(false)
    const [rejectModal, setRejectModal] = useState(false)
    const [rejectModalId, setRejectModalId] = useState(false)

    // main service api hit
    const handleEffects = async () => {
        try {
            //You may notice that apis corresponding to these actions are not getting called on initial render.
            //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
            //So there is no need to fetch them again on the browser.
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardServicesPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyServices({ page: currentPage, isDesk: true, ...filterState, resolve, reject })))
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
    
    // hit api when clicked on add comment
    const addCommentDataFetch = async (id) => {
        setAddOpen(addOpen == id ? false : id);
        let commVal = {
            oi_id: id,
            type: 'GET'
        }
        if(addOpen != id) {
            try {
                if(!addOpen) {
                    dispatch(startCommentLoader())
                    await new Promise((resolve, reject) => dispatch(fetchOiComment({payload: commVal, resolve, reject})));
                    dispatch(stopCommentLoader())
                }
            }
            catch{
                dispatch(stopCommentLoader())
            }
        }
    };

    //Pause service
    const pauseResumeService = (oiStatus, orderId) => {
        let pausePlayValues = {
            oi_status: oiStatus,
            order_item_id: orderId
        }
        dispatch(pausePlayResume(pausePlayValues))
    }

    // download resume builder resume
    const createBuilderResumeDownloadLink = (orderId, productId) =>
  `${siteDomain}/api/v1/resumetemplatedownload/?order_pk=${orderId}&product_id=${productId}`;

    useEffect(() => {
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth"
        });
        handleEffects();
    }, [currentPage, filterState])

    return(
        <React.Fragment>
        <BreadCrumbs filterState={filterState} setfilterState={setfilterState} filterStateShow={true}/>
        <div>
            {serviceLoader ? <Loader /> : ''}

            <div className="db-my-courses-detail">
                {/* {
                    results?.data?.length > 0 && pending_resume_items?.length > 0 ? 
                        <div className="alert alert-primary py-4 px-5 fs-16 w-100 text-center mb-0" role="alert">To initiate your services.<span className="resume-upload--btn">&nbsp;<strong onClick={uploadHandelShow} className="cursor">Upload Resume</strong></span></div>
                    : null
                } */}

                {  results.page.total === 0 ? <EmptyInbox inboxButton="Go To Home" redirectUrl={resumeShineSiteDomain} inboxText="There is no service added to your profile!"/> : '' }

                {results?.data && results?.data?.length > 0 ?
                    results?.data?.map((service,index) => {
                        return(
                            <div className="db-white-box w-100" key={index}>
                                <div className="d-flex">
                                    <figure>
                                        <img src={service.img} alt={service.img_alt} />
                                    </figure>

                                    <div className="db-my-courses-detail--wrap">
                                        <div className="d-flex w-100">
                                            <div className="db-my-courses-detail__leftpan">
                                                <div className="db-my-courses-detail__leftpan--box">
                                                    <h3><Link to={service.productUrl ? service.productUrl : '#'}>{service.heading}</Link></h3>
                                                    <div className="db-my-courses-detail__leftpan--info">
                                                        <span>Provider: <strong>{service.vendor}</strong> </span>
                                                        <span>Bought on: <strong>{service.enroll_date}</strong></span>
                                                        {
                                                            service?.duration_in_days && 
                                                                <span>Duration: <strong>{service?.duration_in_days > 1 ? service?.duration_in_days + ' days' : service?.duration_in_days + ' day' } </strong> </span>
                                                        }
                                                    </div>

                                                    {/* <div className="db-my-courses-detail__leftpan--alert">
                                                        Hi, the recording for the session you missed is available now
                                                    </div> */}

                                                    <div className="db-my-courses-detail__leftpan--status mb-2">
                                                        Status:
                                                        <strong className="ml-1">{ service?.updated_status?.status }
                                                            {
                                                                service?.updated_status?.upload_resume && <Link to={"#"} className="ml-2" onClick={() => uploadToggleService()}>Upload</Link> 
                                                            }
                                                            {
                                                                service?.updated_status?.download_url && <a href={`${service?.updated_status?.download_url}`} target="_blank" className="ml-2"> Download</a> 
                                                            }
                                                            {
                                                                service?.updated_status?.download_credentials_url && <a href={`${siteDomain}${service?.updated_status?.download_credentials_url}`} target="_blank" className="ml-2"> Download Credential</a> 
                                                            }
                                                            {
                                                                service?.updated_status?.edit_your_profile && <a href={`${siteDomain}/dashboard/roundone/profile/`} target="_blank" className="ml-2"> Edit Profile</a>
                                                            }
                                                            {
                                                                service?.updated_status?.complete_profile && <a href={`${siteDomain}/dashboard/roundone/profile/`} target="_blank" className="ml-2"> Complete Profile</a>
                                                            }
                                                            {
                                                                service?.updated_status?.edit_template &&
                                                                    <>
                                                                        <a href={createBuilderResumeDownloadLink(service?.order_id, service?.product)} target="_blank" className="ml-2"> Download</a>
                                                                        <a className="ml-15" target="_blank" href={`${resumeShineSiteDomain}/resume-builder/edit/?type=profile`}>Edit Template</a>
                                                                    </>
                                                            }
                                                            {
                                                                (service?.oi_status === 24 || service?.oi_status === 46) &&
                                                                <>
                                                                    <a className="accept" href="/" onClick={(e) => {e.preventDefault();setAcceptModal(true);setAcceptModalId(service?.id)}}>Accept</a>
                                                                    <a className="ml-2 reject" href="/" onClick={(e) => {e.preventDefault();setRejectModal(true);setRejectModalId(service?.id)}}>Reject</a>
                                                                </>
                                                            }
                                                        </strong>
                                                    </div>

                                                    <Link 
                                                        to={'#'}
                                                        className="font-weight-bold"
                                                        onClick={() => toggleDetails(service.id)}
                                                        aria-controls="addComments"
                                                        aria-expanded={`openViewDetail`+service.id}
                                                    >
                                                        View Details
                                                    </Link>

                                                    {/* course detail modal open */}
                                                    {
                                                        (isOpen === service?.id) && <ViewDetailModal id={service.id} toggleDetails={toggleDetails} isOpen={isOpen}/>
                                                    }
                                                </div>
                                            </div>
                                            <div className="db-my-courses-detail__rightpan">
                                                <div className="share">
                                                    <i className="icon-share"></i>
                                                    <div className="share__box arrow-box top">
                                                        <Link target="_blank" to={{ pathname: `https://www.facebook.com/sharer/sharer.php?u=${siteDomain}${service?.productUrl}`}} className="facebook-icon"></Link>
                                                        <Link target="_blank" to={{ pathname: `https://www.linkedin.com/shareArticle?mini=true&url=${siteDomain}${service?.productUrl}&title=${service?.title}&summary=${service?.name}&source=`}} className="linkedin-icon"></Link>
                                                        <Link target="_blank" to={{ pathname: `https://twitter.com/intent/tweet?url=${siteDomain}${service?.productUrl}/&text=${service?.name}`}} className="twitter-iocn"></Link>
                                                        <Link target="_blank" to={{ pathname: `https://api.whatsapp.com/send?text=Hi! Check this useful product on Shine. ${siteDomain}${service?.productUrl}`}} data-action="share/whatsapp/share" className="whatsup-icon"></Link>
                                                    </div>
                                                </div>

                                                {
                                                    (service?.updated_status?.day_remaining || service?.updated_status?.pause_service || service?.updated_status?.resume_service) &&
                                                    <>
                                                        <div className="day-remaning mb-20">
                                                            {
                                                                service?.updated_status?.day_remaining &&
                                                                <>
                                                                    {
                                                                        (service?.updated_status?.day_remaining > 0 ? service?.updated_status?.day_remaining : '00')?.toString()?.split('')?.map((digit, index) => {
                                                                            return (
                                                                                <span className="day-remaning--box" key={index}> { digit }</span>
                                                                            )
                                                                        })
                                                                    }
                                                                    <span className="ml-2 day-remaning--text">
                                                                        { service?.updated_status?.day_remaining > 1 ? 'Days' : 'Day'} <br />remaining
                                                                    </span>
                                                                </>
                                                            }
                                                        </div>
                                                        {
                                                        service?.updated_status?.pause_service && <Link to={"#"} className="db-start-course font-weight-bold pr-10" onClick={() => pauseResumeService(34, service?.id)}>Pause Service</Link>
                                                        }
                                                        {
                                                            service?.updated_status?.resume_service && <Link to={"#"} className="db-resume-course font-weight-bold pr-10" onClick={() => pauseResumeService(35, service?.id)}>Resume Service</Link>
                                                        }
                                                    </>
                                                }
                                            </div>
                                        </div>

                                        <div className="db-my-courses-detail__bottom">
                                            <Link
                                                to={"#"}
                                                className="db-comments font-weight-bold"
                                                onClick={() => addCommentDataFetch(service.id, service.no_of_comments)}
                                                aria-controls="addComments"
                                                aria-expanded={`openComment`+service.id}
                                                >
                                                    {service.no_of_comments > 0 && service.no_of_comments > 1 ?
                                                        service.no_of_comments + ' Comments'
                                                        :
                                                        service.no_of_comments > 0 && service.no_of_comments < 1 ?
                                                        service.no_of_comments + ' Comment'
                                                        :
                                                        'Add comment'
                                                    }
                                            </Link>
                                            
                                            {/* ratings start here */}
                                            { 
                                                (service?.updated_status?.your_feedback) && 
                                                    <div className="d-flex" id={service?.id}>
                                                        {
                                                            service?.len_review ?
                                                                <div onClick={()=>{
                                                                    toggleRatingsModal(service?.id);
                                                                }}>
                                                                    <span className="rating">
                                                                        {
                                                                            service?.rating?.map((star, index) => starRatings(star, index))
                                                                        }
                                                                        <span className="ml-5">
                                                                            { service?.avg_rating?.toFixed() }/5 
                                                                        </span>
                                                                    </span>
                                                                    <a className="font-weight-bold ml-10">
                                                                        { service?.len_review > 1 ? service?.len_review + ' Reviews' : service?.len_review + ' Review' }
                                                                    </a>
                                                                </div> : 
                                                                <div onClick={()=>{
                                                                    setShowRateModal(true);
                                                                    setOiReviewId(service?.id);
                                                                    setReviewData(service?.review_data)
                                                                }}>
                                                                    <span className="">Rate Service&nbsp;</span>
                                                                    <span className="rating">
                                                                        {
                                                                            [1, 2, 3, 4, 5].map((item, index) => {
                                                                                return <em className="icon-blankstar" key={index} />
                                                                            })
                                                                        }
                                                                    </span>
                                                                </div>

                                                            
                                                        }
                                                        {showRatingModal && <ReviewModal showRatingModal={showRatingModal} toggleRatingsModal={toggleRatingsModal} setShowRateModal={setShowRateModal} oi_id={service?.id} reviewData={service?.review_data} />}
                                                    </div>
                                            }
                                        </div>
                                    </div>
                                </div>
                                {/* add comment dropdown */}
                                <AddCommentModal id={service.id} addCommentDataFetch={addCommentDataFetch} data={oiComments} addOpen={addOpen} type="myservices" />
                            </div>
                        )
                    })
                    :null
                }

                {
                    uploadShow && <UploadResumeModal uploadHandelClose={uploadHandelClose} show={uploadShow} pending_resume_items={pending_resume_items} />
                }
                {
                    acceptModal && <AcceptModal acceptModal={acceptModal} setAcceptModal={setAcceptModal} oi_id={acceptModalId} filterState={filterState} currentPage={currentPage} />
                }
                {
                    rejectModal && <RejectModal rejectModal={rejectModal} setRejectModal={setRejectModal} oi_id={rejectModalId} filterState={filterState } currentPage={currentPage} />
                }

                {
                    showRateModal && <RateModal showRateModal={showRateModal} setShowRateModal={setShowRateModal} oi_id={oiReviewId} name="Service" />
                }

                {/* pagination set here */}
                {results?.page?.total > 1 ? <Pagination totalPage={results?.page?.total} currentPage={currentPage} setCurrentPage={setCurrentPage}/> : ''}
            </div>
        </div>
        </React.Fragment>
    )
}
   
export default MyServices;