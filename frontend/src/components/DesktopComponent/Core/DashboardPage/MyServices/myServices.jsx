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
import ReviewRating from '../Inbox/reviewRating';
import AddCommentModal from '../Inbox/addCommentModal';
import Pagination from '../../../Common/Pagination/pagination';
import AcceptModal from '../Inbox/acceptModal';
import RejectModal from '../Inbox/rejectModal';
import EmptyInbox from '../Inbox/emptyInbox';
import { startCommentLoader, stopCommentLoader } from 'store/Loader/actions/index';
import { startReviewLoader, stopReviewLoader } from 'store/Loader/actions/index';
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

    // review open close set here
    const [openReview, setOpenReview] = useState(false);
    const [show, setShow] = useState(false);

    // if view detail then show
    const [isOpen, setIsOpen] = useState(false);
    const toggleDetails = (id) => setIsOpen(isOpen == id ? false : id);

    // if upload then show
    const [uploadShow, setUploadShow] = useState(false);
    const uploadHandelClose = () => setUploadShow(false);
    const uploadHandelShow = () => setUploadShow(true);

    // comment open close set here
    const [addOpen, setaddOpen] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

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

    // if reviews exists then show
    const toggleReviews = async (id, prod) => {
        if(openReview != id) {
            dispatch(startReviewLoader());
            await new Promise((resolve, reject) => dispatch(fetchReviews({ payload: { prod: prod, page: currentPage}, resolve, reject })));
            dispatch(stopReviewLoader());
        }
        setOpenReview(openReview == id ? false : id);
    }
    
    // hit api when clicked on add comment
    const addCommentDataFetch = async (id) => {
        setaddOpen(addOpen == id ? false : id);
        let commVal = {
            oi_id: id,
            type: 'GET'
        }
        if(addOpen != id){
            dispatch(startCommentLoader());
            await new Promise((resolve, reject) => dispatch(fetchOiComment({payload: commVal, resolve, reject})));
            dispatch(stopCommentLoader());
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
        handleEffects();
        dispatch(fetchPendingResume());
    }, [currentPage, filterState])

    return(
        <React.Fragment>
        <BreadCrumbs filterState={filterState} setfilterState={setfilterState} />

        <div>
            {serviceLoader ? <Loader /> : ''}

            <div className="db-my-courses-detail">
                {
                    results?.data?.length > 0 && pending_resume_items?.length > 0 ? 
                        <div className="alert alert-primary py-4 px-5 fs-16 w-100 text-center mb-0" role="alert">To initiate your services.<span className="resume-upload--btn">&nbsp;<strong onClick={uploadHandelShow} className="cursor">Upload Resume</strong></span></div>
                    : null
                }

                { !results?.page?.total || results?.page?.total === 0 ? <EmptyInbox/> : '' }

                {results?.data && results?.data?.length > 0 ?
                    results?.data?.map((item,index) => {
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
                                                            <strong className="ml-1">{item.new_oi_status ? item.oi_status === 4 ? 'Service has been processed and Document is finalized' : item.oi_status === 101 ? 'Take Test' : item.oi_status == 141 ? 'Your profile to be shared with interviewer is pending -' : item.oi_status === 142 ? 'Service is under progress -' : item.oi_status === 143 ? 'Service has been expired' : item.new_oi_status : "Yet to Update"}
                                                            
                                                            {/* upload link */}
                                                            {item.options?.upload_resume ? <Link to={"#"} className="ml-2" onClick={uploadHandelShow}>Upload</Link>
                                                            : null}

                                                            {/* download option if draft file exists */}
                                                            {item.options?.Download ? <a className="ml-2" target="_blank" href={item.options?.download_url}>Download</a>
                                                            : null}

                                                            {/* take test when type flow is 16 */}
                                                            {item?.options?.take_test ? <a className="ml-2" target="_blank" href={ item?.options?.auto_login_url}>Take Test</a>
                                                            : null}

                                                            {item.product_type_flow === 17 && item?.options?.edit_template ? 
                                                                <React.Fragment>
                                                                    <a className="ml-2" target="_blank" href={createBuilderResumeDownloadLink(item.id, item.product)}>Download</a>

                                                                    <Link className="ml-15" target="_blank" to={{ pathname: `${resumeShineSiteDomain}/resume-builder/edit/?type=profile`}}>Edit Template</Link>
                                                                </React.Fragment>
                                                            : null}

                                                            {item.product_type_flow === 9 ? 
                                                                <React.Fragment>
                                                                    {item.oi_status == 141 ? (
                                                                        <a className="ml-2" target="_blank" href={{pathname: `${siteDomain}/dashboard/roundone/profile/`}}>Complete Profile</a>
                                                                    ) : item.oi_status == 142 ? (
                                                                        <a className="ml-2" target="_blank" href={{pathname: `${siteDomain}/dashboard/roundone/profile/`}}>Edit Profile</a>
                                                                    ) : null}
                                                                </React.Fragment>
                                                            : null}

                                                            {
                                                                (item.oi_status === 24 || item.oi_status === 46) &&
                                                                <React.Fragment>
                                                                    <Link className="accept" to={"#"} onClick={() => {setAcceptModal(true);setAcceptModalId(item?.id)}}>Accept</Link>
                                                                    <Link className="ml-2 reject" to={"#"} onClick={() => {setRejectModal(true);setRejectModalId(item?.id)}}>Reject</Link>
                                                                </React.Fragment>
                                                            }
                                                        </strong> 
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
                                                    { isOpen && <ViewDetailModal id={item.id} toggleDetails={toggleDetails} isOpen={isOpen} datalist={item.datalist || []}/> }
                                                </div>
                                            </div>
                                            <div className="db-my-courses-detail__rightpan">
                                                <div className="share">
                                                    <i className="icon-share"></i>
                                                    <div className="share__box arrow-box top">
                                                        <Link target="_blank" to={{ pathname: `https://www.facebook.com/sharer/sharer.php?u=${siteDomain}${item?.productUrl}`}} className="facebook-icon"></Link>
                                                        <Link target="_blank" to={{ pathname: `https://www.linkedin.com/shareArticle?mini=true&url=${siteDomain}${item?.productUrl}&title=${item?.title}&summary=${item?.name}&source=`}} className="linkedin-icon"></Link>
                                                        <Link target="_blank" to={{ pathname: `https://twitter.com/intent/tweet?url=${siteDomain}${item?.productUrl}/&text=${item?.name}`}} className="twitter-iocn"></Link>
                                                        <Link target="_blank" to={{ pathname: `https://api.whatsapp.com/send?text=Hi! Check this useful product on Shine. ${siteDomain}${item?.productUrl}`}} data-action="share/whatsapp/share" className="whatsup-icon"></Link>
                                                    </div>
                                                </div>

                                                <div className="day-remaning mb-20">
                                                    {[...(item.remaining_days + '')].map((day, idx) => <span key={idx} className="day-remaning--box">{day}</span>)}
                                                    <span className="ml-2 day-remaning--text"> {item?.remaining_days > 1 ? 'Days' : 'Day'} <br/>remaning</span>
                                                </div>

                                                {
                                                item?.options?.pause_service && <Link to={"#"} className="m-db-start-course font-weight-bold pr-10" onClick={() => pauseResumeService(34, item?.id)}>Pause Service</Link>
                                                }
                                                {
                                                    item?.options?.resume_service && <Link to={"#"} className="m-db-start-course font-weight-bold pr-10" onClick={() => pauseResumeService(35, item?.id)}>Resume Service</Link>
                                                }
                                            </div>
                                        </div>

                                        <div className="db-my-courses-detail__bottom">
                                            <Link
                                                to={"#"}
                                                className="db-comments font-weight-bold"
                                                onClick={() => addCommentDataFetch(item.id)}
                                                aria-controls="addComments"
                                                aria-expanded={`openComment`+item.id}
                                                >
                                                    {item.no_of_comments > 0 && item.no_of_comments > 1 ?
                                                        item.no_of_comments + ' Comments'
                                                        :
                                                        item.no_of_comments > 0 && item.no_of_comments < 1 ?
                                                        item.no_of_comments + ' Comment'
                                                        :
                                                        'Add comment'
                                                    }
                                            </Link>
                                            {/* ratings start here */}

                                            { (item.oi_status === 4) && 
                                                <div className="d-flex">
                                                    <ReviewRating
                                                        item={item}
                                                        handleShow={handleShow}
                                                        toggleReviews={toggleReviews} 
                                                        setOpenReview={setOpenReview}
                                                        openReview={openReview}
                                                        name="Service"/>

                                                    {/* rate service modal */}
                                                    <RateModal handleClose={handleClose} show={show} id={item.id} name="Service"/>
                                                </div>
                                            }
                                        </div>
                                    </div>
                                </div>
                                {/* add comment dropdown */}
                                <AddCommentModal id={item.id} addCommentDataFetch={addCommentDataFetch} data={oiComments} addOpen={addOpen} />
                            </div>
                        )
                    })
                    :null
                }

                {
                    uploadShow && <UploadResumeModal uploadHandelClose={uploadHandelClose} show={uploadShow} data={pending_resume_items} />
                }
                {
                    acceptModal && <AcceptModal acceptModal={acceptModal} setAcceptModal={setAcceptModal} oi_id={acceptModalId}/>
                }
                {
                    rejectModal && <RejectModal rejectModal={rejectModal} setRejectModal={setRejectModal} oi_id={rejectModalId}/>
                }

                {/* pagination set here */}
                {results?.page?.total > 1 ? <Pagination totalPage={results?.page?.total} currentPage={currentPage} setCurrentPage={setCurrentPage}/> : ''}
            </div>
        </div>
        </React.Fragment>
    )
}
   
export default MyServices;