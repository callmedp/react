import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
// import { ProgressBar } from 'react-bootstrap';
import './myCourses.scss';
import '../../SkillPage/NeedHelp/needHelp.scss';
import { startDashboardCoursesPageLoader, stopDashboardCoursesPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMyCourses } from 'store/DashboardPage/MyCourses/actions';
import { siteDomain } from 'utils/domains';
import ViewDetailModal from '../Inbox/viewDetailModal';
import RateModal from '../Inbox/rateModal';
import ReviewModal from '../Inbox/reviewModal';
import AddCommentModal from '../Inbox/addCommentModal';
import { fetchOiComment } from 'store/DashboardPage/AddSubmitComment/actions/index';
import { fetchReviews } from 'store/DashboardPage/AddSubmitReview/actions/index';
import Pagination from '../../../Common/Pagination/pagination';
import EmptyInbox from '../Inbox/emptyInbox';
import { startReviewLoader, stopReviewLoader } from 'store/Loader/actions/index';
import { startCommentLoader, stopCommentLoader } from 'store/Loader/actions/index';
import BreadCrumbs from '../Breadcrumb/Breadcrumb';
import {Toast} from '../../../Common/Toast/toast';
import {boardNeoUser} from 'store/DashboardPage/MyCourses/actions/index';
import { getCandidateId } from 'utils/storage.js';
import { getVendorUrl } from 'store/DashboardPage/StartCourse/actions/index';

const MyCourses = (props) => {
    const [addOpen, setAddOpen] = useState(false);
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const handleComment = (id) => setAddOpen( addOpen === id ? false : id );
    const dispatch = useDispatch();
    const { history } = props;
    const { coursesLoader } = useSelector(store => store.loader);
    const { data, page } = useSelector(store => store.dashboardCourses);
    const [isOpen, setIsOpen] = useState(false);
    const toggleDetails = (id) => setIsOpen(isOpen === id ? false : id);
    const [openReview, setOpenReview] = useState(false);
    const oiComments = useSelector(store => store.getComment);
    const [currentPage, setCurrentPage] = useState(1);
    const [filterState, setfilterState] = useState({ 'last_month_from': 'all', 'select_type' : 'all' });
    const [showIframe, setShowIframe] = useState(false);
    const handleIframeShow = () => setShowIframe(true);
    const handleIframeClose = () => setShowIframe(false);
    const [openIframe, setOpenIframe] = useState(false);
    const toggleIframe = (id) => setOpenIframe(id);

    // rating modal handling
    const [showRatingModal, setShowRatingModal] = useState(false) 
    const toggleRatingsModal = (id) => setShowRatingModal(showRatingModal == id ? false : id);

    //Rate Modal Handling
    const [showRateModal, setShowRateModal] = useState(false) 
    const [oiReviewId, setOiReviewId] = useState('')

     //set review data
     const [reviewData, setReviewData] = useState([]);

     const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+' 
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    useEffect(() => {
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: "smooth"
        });
        handleEffects();
    }, [currentPage, filterState])

    // const toggleReviews = async (id, prod) => {
    //     if(openReview != id) {
    //         dispatch(startReviewLoader());
    //         await new Promise((resolve, reject) => dispatch(fetchReviews({ payload: { prod: prod}, resolve, reject })));
    //         dispatch(stopReviewLoader());
    //     }
    //     setOpenReview(openReview == id ? false : id);
    // }

    const addCommentDataFetch = async (id) => {
        setAddOpen(addOpen == id ? false : id);
        let commVal = {
            oi_id: id,
            type: 'GET'
        }
        if(addOpen != id){
            try{
                dispatch(startCommentLoader())
                await new Promise((resolve, reject) => dispatch(fetchOiComment({payload: commVal, resolve, reject})));
                dispatch(stopCommentLoader())
            }
            catch{
                dispatch(stopCommentLoader())
            }
            
        }
    };

    // for neo products
    const NeoBoardUser = async (oi) => {
        try {
            const response = await new Promise((resolve, reject) => {
            dispatch(
                boardNeoUser({
                payload: {
                    oi_pk: oi,
                },
                resolve,
                reject,
                })
            );
            });
            if (response["error"]) {
            return Toast("error", response["error"]);
            }
            Toast("success", response.data);
            // dispatch(fetchInboxOiDetails({ cid: cid, id: oi }));
        
            return;
        } catch (e) {
            return Toast("error",e);
        }
        };
    
    const autoLogin = async (oi, ci, lm) => {
        try {
           dispatch(startDashboardCoursesPageLoader());
           const response = await new Promise((resolve, reject) => {
           dispatch(
               getVendorUrl({
               payload: {
                   candidate_id: getCandidateId(),
                   order_id: oi,
                   course_id: ci,
               },
               resolve,
               reject,
               })
           );
           });
           dispatch(stopDashboardCoursesPageLoader());
           let url = response?.data?.vendor_url;
           let error_message = response?.error_message;
           if(error_message){
               Toast.fire({
                   type: 'error',
                   title: error_message
               });
               return;
           }
           if(url === undefined || url === '' || !url){
               Toast.fire({
                   type: 'error',
                   title: 'Something went wrong! Try Again'
               });
               return;
           } 
           if(lm === 1){ history.push({ pathname : '/dashboard/startcourse/' , url : url}); return; }
           if(lm === 2){ window.open(url); return; }
           Toast.fire({
                   type: 'error',
                   title: 'Something went wrong! Try Again'
               });
           return;
        }catch (e) {
           dispatch(stopDashboardCoursesPageLoader());
           Toast.fire({
                   type: 'error',
                   title: 'Something went wrong! Try Again'
               });
           return;
       }
    };

    const handleEffects = async () => {
        try {
          
                dispatch(startDashboardCoursesPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyCourses({ page: currentPage, ...filterState, resolve, reject })))
                dispatch(stopDashboardCoursesPageLoader());
                
        } catch (error) {
            dispatch(stopDashboardCoursesPageLoader());
            if (error?.status == 404) {
                history.push('/404');
            }
        }
    };


    return (
        <div>
            { coursesLoader ? <Loader /> : ''}

            <BreadCrumbs filterState={filterState} setfilterState={setfilterState} filterStateShow={true}/>

            <div className="db-my-courses-detail">


                { page.total === 0 ? <EmptyInbox inboxButton="Browse Courses" redirectUrl={`${siteDomain}/online-courses.html`} inboxText="Seems like no courses / certification added to your profile"/> : '' }
                {
                    data?.map((course, index) => {
                        return (
                            <div className="db-white-box w-100" key={index}>
                                <div className="d-flex">
                                    <figure>
                                        <img src={course.img} alt={course.heading} />
                                    </figure>

                                    <div className="db-my-courses-detail--wrap">
                                        <div className="d-flex w-100">
                                            <div className="db-my-courses-detail__leftpan">
                                                <div className="db-my-courses-detail__leftpan--box">
                                                    <h3><a href={`${siteDomain}${course.productUrl}`}>{course.heading}</a></h3>
                                                    <div className="db-my-courses-detail__leftpan--info">
                                                        { !!course.vendor && <span>Provider: <strong className="text-gray-dark noLink" to={"#"}>{course.vendor}</strong></span> }
                                                        { !!course.enroll_date && <span>Enrolled on: <strong>{course.enroll_date}</strong></span> }
                                                        { !!course?.duration_in_days && <span>Duration: <strong>{course?.duration_in_days} {course?.duration_in_days > 1 ? 'days': 'day'}</strong></span> }
                                                        { !!course.mode && <span>Mode: <strong>{course.mode}</strong></span> }
                                                        { !!course.jobs && <span>Jobs: <strong>{course.jobs}</strong></span> }
                                                    </div>

                                                    {/* <div className="db-my-courses-detail__leftpan--session">
                                                        <span>Next session : <strong>Basic of Digital Marketing</strong></span>
                                                        <span className="db-icon-date font-weight-bold">3PM |  29 nov 2020</span>
                                                    </div> */}

                                                    {/* <div className="db-my-courses-detail__leftpan--alert">
                                                        Hi, the recording for the session you missed is available now <Link to={"#"} className="ml-2">Click here</Link>
                                                    </div> */}

                                                    <div className="db-my-courses-detail__leftpan--status mb-2">
                                                    {
                                                            <>
                                                                <strong> 
                                                                { course?.updated_status?.status && course?.updated_status?.status !== 'Default' && <> <span className="font-weight-normal">Status:</span> {course?.updated_status?.status} </>} 
                                                                {
                                                                    course?.updated_status?.take_test && <a href={course?.updated_status?.auto_login_url} target="_blank" className="font-weight-bold"> Take test</a>
                                                                }
                                                                {
                                                                    course?.updated_status?.BoardOnNeo && <a href='/' className="font-weight-bold" onClick={NeoBoardUser(course?.id)}> :- Board on Neo</a>
                                                                }
                                                                {
                                                                    course?.updated_status?.neo_mail_sent && ':- Please Confirm Boarding on Mail Sent to you'
                                                                }
                                                                {
                                                                    course?.updated_status?.updated_from_trial_to_regular && ':- Updated Account from Trial To Regular'
                                                                }
                                                                {
                                                                    course?.updated_status?.download_url && <a href={`${course?.updated_status?.download_url}`} target="_blank" className="font-weight-bold"> Download</a> 
                                                                }
                                                                {
                                                                    course?.updated_status?.download_credentials_url && <a href={`${course?.updated_status?.download_credentials_url}`} target="_blank" className="font-weight-bold"> Download Credential</a> 
                                                                }
                                                                </strong>
                                                            </>
                                                        }
                                                    </div>
                                                    <Link
                                                        className="font-weight-bold"
                                                        onClick={() => toggleDetails(course.id)}
                                                        aria-controls="addComments"
                                                        aria-expanded={`openViewDetail` + index}
                                                        to={'#'}
                                                    >
                                                        View Details
                                                    </Link>

                                                    {/* course detail modal open */}
                                                    {
                                                        (isOpen === course?.id) && <ViewDetailModal 
                                                        id={course.id} 
                                                        toggleDetails={toggleDetails}  
                                                        isOpen={isOpen}
                                                        />
                                                    }
                                                </div>
                                            </div>

                                            <div className="db-my-courses-detail__rightpan">
                                                <div className="share">
                                                    <i className="icon-share"></i>
                                                    <div className="share__box arrow-box top">
                                                        <Link target="_blank" to={{ pathname: `https://www.facebook.com/sharer/sharer.php?u=${siteDomain}${course?.productUrl}`}} className="facebook-icon"></Link>
                                                        <Link target="_blank" to={{ pathname: `https://www.linkedin.com/shareArticle?mini=true&url=${siteDomain}${course?.productUrl}&title=${course?.title}&summary=${course?.name}&source=`}} className="linkedin-icon"></Link>
                                                        <Link target="_blank" to={{ pathname: `https://twitter.com/intent/tweet?url=${siteDomain}${course?.productUrl}/&text=${course?.name}`}} className="twitter-iocn"></Link>
                                                        <Link target="_blank" to={{ pathname: `https://api.whatsapp.com/send?text=Hi! Check this useful product on Shine. ${siteDomain}${course?.productUrl}`}} data-action="share/whatsapp/share" className="whatsup-icon"></Link>
                                                    </div>
                                                </div>

                                                {course?.updated_status?.day_remaining ?
                                                    <div className="day-remaning mb-20">

                                                        {
                                                            (course?.updated_status?.day_remaining > 0 ? course?.updated_status?.day_remaining : '00')?.toString()?.split('')?.map((digit, index) => {
                                                                return (
                                                                    <span className="day-remaning--box" key={index}> { digit }</span>
                                                                )
                                                            })
                                                        }

                                                        <span className="ml-2 day-remaning--text">{ course?.updated_status?.day_remaining > 1 ? 'Days' : 'Day'} <br />remaining<br />remaning</span>
                                                    </div>
                                                : null}

                                                {/* <div className="db-status mt-20">
                                                    <p className="mb-0 pb-1">Status: <strong>(0% Complete)</strong> </p>
                                                    <ProgressBar now={0} />
                                                </div>

                                                <Link to={"#"} className="db-start-course font-weight-bold mt-30">Start course</Link> */}
                                                { [1, 2].includes(course?.auto_login_method) ?
                                                   <Link to={"#"} className="db-start-course font-weight-bold mt-30" onClick={()=>autoLogin(course?.order_id, course?.product, course?.auto_login_method )}>Start course</Link> : null
                                                }
                                            </div>
                                        </div>

                                        <div className="db-my-courses-detail__bottom">
                                            <Link
                                                className="db-comments font-weight-bold"
                                                onClick={() => addCommentDataFetch(course.id)}
                                                aria-controls="addComments"
                                                aria-expanded={addOpen}
                                                to={"#"}
                                            >
                                                  { course.no_of_comments > 0 && course.no_of_comments > 1 ?
                                                        course.no_of_comments + ' Comments'
                                                        :
                                                        course.no_of_comments > 0 && course.no_of_comments < 1 ?
                                                        course.no_of_comments + ' Comment'
                                                        :
                                                        'Add comment'
                                                    }
                                            </Link>
                                            {
                                                (course?.updated_status?.your_feedback) && 
                                                    <div className="d-flex" id={course?.id}>
                                                        {
                                                        course?.len_review ?
                                                            <div onClick={()=>{
                                                                toggleRatingsModal(course?.id);
                                                            }}>
                                                                <span className="rating">
                                                                    {
                                                                        course?.rating?.map((star, index) => starRatings(star, index))
                                                                    }
                                                                    <span className="ml-5">
                                                                        { course?.avg_rating?.toFixed() }/5 
                                                                    </span>
                                                                </span>
                                                                <a className="font-weight-bold ml-10">
                                                                    { course?.len_review > 1 ? course?.len_review + ' Reviews' : course?.len_review + ' Review' }
                                                                </a>
                                                            </div> : 
                                                            <div onClick={()=>{
                                                                setShowRateModal(true);
                                                                setOiReviewId(course?.id);
                                                                setReviewData(course?.review_data)
                                                            }}>
                                                                <span className="">Rate Course&nbsp;</span>
                                                                <span className="rating">
                                                                    {
                                                                        [1, 2, 3, 4, 5].map((item, index) => {
                                                                            return <em className="icon-blankstar" key={index} />
                                                                        })
                                                                    }
                                                                </span>
                                                            </div>
                                                        }
                                                        {showRatingModal && <ReviewModal showRatingModal={showRatingModal} toggleRatingsModal={toggleRatingsModal} setShowRateModal={setShowRateModal} oi_id={course?.id} reviewData={course?.review_data} />}
                                                    </div>
                                            }
                                        </div>
                                    </div>
                                </div>
                                <AddCommentModal id={course.id} addCommentDataFetch={addCommentDataFetch} data={oiComments} addOpen={addOpen} type="mycourses" />

                                {/* <div className="db-mycourse-highlighter">Next course to take: <Link to={"#"} className="font-weight-bold ml-2">Seo Specialist</Link> </div> */}
                            </div>
                        )
                    })
                }

                {
                    showRateModal && <RateModal showRateModal={showRateModal} setShowRateModal={setShowRateModal} oi_id={oiReviewId} name="Course" />
                }

                {
                    showRatingModal && <ReviewModal setShowRateModal={setShowRateModal} showRatingModal={showRatingModal} setShowRatingModal={setShowRatingModal} oi_id={oiReviewId} reviewData={reviewData} />
                }
                {/* pagination set here */}
                { page?.total > 1 ? <Pagination totalPage={ page?.total} currentPage={currentPage} setCurrentPage={setCurrentPage}/> : ''}
            </div>
        </div>
    )
}

export default MyCourses;