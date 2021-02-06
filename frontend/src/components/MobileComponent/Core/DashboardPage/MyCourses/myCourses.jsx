//React Core Import
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';

//Local Import
import './myCourses.scss';
import AddCommentModal from '../InboxModals/addCommentModal';
import RateProductModal from '../InboxModals/rateProductModal'
import ShowRatingsModal from '../InboxModals/showRatingsModal'
import Pagination from '../../../Common/Pagination/pagination';
import Loader from '../../../Common/Loader/loader';
import EmptyInbox from '../InboxModals/emptyInbox';
import { fetchMyCourses, boardNeoUser } from 'store/DashboardPage/MyCourses/actions/index'
import { startDashboardCoursesPageLoader, stopDashboardCoursesPageLoader } from 'store/Loader/actions/index';
import { siteDomain } from 'utils/domains';
import { showSwal } from 'utils/swal';
import ViewDetails from '../MyServices/oiViewDetails';
import { getCandidateId } from 'utils/storage.js';
import { getVendorUrl } from 'store/DashboardPage/StartCourse/actions/index';


const MyCourses = (props) => {
    const { history } = props;
    const [showCommentModal, setShowCommentModal] = useState(false)
    const [showRateModal, setShowRateModal] = useState(false)
    const [showRatingsModal, setShowRatingsModal] = useState(false)
    const [currentPage, setCurrentPage] = useState(1)
    const [showOrderDetailsID, setShowOrderDetailsID] = useState('')
    const [oiCommentId, setOiCommentId] = useState('')
    const [oiReviewId, setOiReviewId] = useState({})
    const [showIframe, setShowIframe] = useState(false);
    const [openIframe, setOpenIframe] = useState(false);
    const toggleIframe = (id) => setOpenIframe(id);
    const handleIframeShow = () => setShowIframe(true);
    const handleIframeClose = () => setShowIframe(false);
    
    const dispatch = useDispatch();
    const { data, page } = useSelector(store => store?.dashboardCourses);
    const { coursesLoader } = useSelector(store => store.loader);

    //set review data
    const [reviewData, setReviewData] = useState([])

    const showDetails = (id) => {
        id == showOrderDetailsID ?
            setShowOrderDetailsID('') : setShowOrderDetailsID(id)
    }

    const boardOnNeo = async (event, oiId) => {
        event.preventDefault();
        try {
            const response = await new Promise((resolve, reject) => { dispatch(boardNeoUser({ payload: { oi_pk: oiId }, resolve, reject }));
            });
            if (response["error"]) {
                return showSwal('error', response['error'])
            }
            return showSwal('success', response.data)
        } 
        catch (e) {
            return showSwal('error', e)
        }
    }

    const handleEffects = async () => {
        if (!(window && window.config && window.config.isServerRendered)) {
            try{
                dispatch(startDashboardCoursesPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyCourses({ page: currentPage, resolve, reject })));
                dispatch(stopDashboardCoursesPageLoader());
            }
            catch{
                dispatch(stopDashboardCoursesPageLoader());
            }
        }
        else {
            delete window.config?.isServerRendered
        }

    };

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+'
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    //Iframe function
    const autoLogin = async (oi, ci, lm) => {
        try {
           dispatch(startDashboardCoursesPageLoader());
           const response = await new Promise((resolve, reject) => {
           dispatch(
               getVendorUrl({
               payload: {
                   candidate_id: getCandidateId(),
                   //candidate_id: "5ebacd1472bebb294db0b7cd",
                   order_id: oi,
                   course_id: ci,
               },
               resolve,
               reject,
               })
           );
           });
           dispatch(stopDashboardCoursesPageLoader());
           let url = response?.vendor_url;
           if(url === undefined || url === '' || !url){
               return showSwal('error', "Technical Issue, Please try after Sometime")
           }
           if (lm === 2) { window.open(url); return };
           if (lm === 1) { history.push({ pathname : '/dashboard/startcourse/' , url : url}); return };
           return showSwal('error', "Technical Issue, Please try after Sometime")
        }catch (e) {
           dispatch(stopDashboardCoursesPageLoader());
           return null
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

    return(
        <>
            { coursesLoader && <Loader />}
            {
                page?.total === 0 ? <EmptyInbox inboxType="courses"/> :

            <div>
                <div className="m-courses-detail db-warp">
                    {
                        data?.map((course, index) => {
                            return(
                                <div className="m-card pl-0" key={index}>
                                    <div className="m-share" aria-haspopup="true">
                                        <i className="icon-share"></i>
                                        <div className="m-share__box m-arrow-box m-top">
                                            <a target="_blank" href={`https://www.facebook.com/sharer/sharer.php?u=${siteDomain}${course?.productUrl}`} className="m-facebook-icon"></a>
                                            <a target="_blank" href={`https://www.linkedin.com/shareArticle?mini=true&url=${siteDomain}${course?.productUrl}&title=${course?.title}&summary=${course.name}&source=`} className="m-linkedin-icon"></a>
                                            <a target="_blank" href={`https://twitter.com/intent/tweet?url=${siteDomain}${course?.productUrl}/&text=${course.name}`} className="m-twitter-iocn"></a>
                                            <a target="_blank" href={`https://api.whatsapp.com/send?text=Hi! Check this useful product on Shine. ${siteDomain}${course?.productUrl}`} data-action="share/whatsapp/share" className="m-whatsup-icon"></a>
                                        </div>
                                    </div>

                                    <div className="d-flex">
                                        <figure>
                                            <img src={course?.img} alt={course?.title} />
                                        </figure>
                                        <div className="m-courses-detail__info">
                                            <h2>{course?.name}</h2>
                                            <p className="m-pipe-divides mb-5">Provider: <Link to={"#"} className="font-weight-bold">{course?.vendor}</Link></p>
                                            <p className="m-pipe-divides mb-5">{ !!course?.enroll_date && <span>Enrolled on: <strong>{course?.enroll_date}</strong> </span> } { !!course?.mode && <span>Mode: <strong>{course?.mode}</strong> </span> }</p>
                                            <p className="m-pipe-divides mb-5">{ !!course?.duration_in_days && <span> Duration: <strong>{ course?.duration_in_days } { course?.duration_in_days > 1 ? 'days' : 'day' }</strong> </span> } { !!course?.jobs && <span>Jobs: <strong>{course?.jobs}</strong> </span>}</p>
                                        </div>
                                    </div>
                                    {/* <div className="m-courses-detail--session pl-15 d-flex mb-15 mt-10">
                                        <span>Next session :</span> 
                                        <strong>Basic of Digital Marketing 3PM |  29 nov 2020</strong> 
                                    </div> */}

                                    {/* <div className="m-courses-detail--alert">
                                    Hi, the recording for the session you missed is available now <Link to={"#"} className="font-weight-semi-bold">Check here</Link>
                                    </div> */}
                                            <div className="pl-15 mt-15 fs-12">
                                            {
                                                course?.updated_status?.status && 
                                                    <>
                                                        Status: <strong> 
                                                        { course?.updated_status?.status } 

                                                        {
                                                            course?.updated_status?.take_test && <a href={course?.options?.auto_login_url} target="_blank" className="font-weight-bold"> Take test</a>
                                                        }
                                                        {
                                                            course?.updated_status?.BoardOnNeo && <a href='/' className="font-weight-bold" onClick={(event) => {event.preventDefault();boardOnNeo(event, course?.id)}}> :- Board on Neo</a>
                                                        }
                                                        {
                                                            course?.updated_status?.neo_mail_sent && ':- Please Confirm Boarding on Mail Sent to you'
                                                        }
                                                        {
                                                            course?.updated_status?.updated_from_trial_to_regular && ':- Updated Account from Trial To Regular'
                                                        }
                                                        {
                                                            course?.updated_status?.download_url && <a href={`${siteDomain}${course?.updated_status?.download_url}`} target="_blank" className="font-weight-bold"> Download</a> 
                                                        }
                                                        {
                                                            course?.updated_status?.download_credentials_url && <a href={`${siteDomain}${course?.updated_status?.download_credentials_url}`} target="_blank" className="font-weight-bold"> Download Credential</a> 
                                                        }
                                                        </strong>
                                                    </>
                                            }
                                                
                                                {/* <Link to={"#"} className="d-block font-weight-bold">View Details</Link> */}

                                                <div className="my-order__order-detail">
                                                    <a onClick={(e) => { e.preventDefault(); showDetails(course?.id) }} className={(showOrderDetailsID === course?.id) ? "d-block font-weight-bold open arrow-icon" : "d-block font-weight-bold arrow-icon"}>View Details</a>
                                                    {   
                                                        (showOrderDetailsID === course?.id) && <ViewDetails id={course?.id} />
                                                    }
                                                </div> 

                                            </div>

                                            
                                                    <div className="pl-15">
                                                        <div className="m-courses-detail__bottomWrap" style={{ paddingBottom: '0' }}>
                                                        {
                                                            course?.updated_status?.day_remaining &&
                                                            <div>
                                                                <div className="m-day-remaning mb-20">
                                                                    {
                                                                        (course?.updated_status?.day_remaining > 0 ? course?.options?.day_remaining : '0')?.toString()?.split('')?.map((digit, index) => {
                                                                            return (
                                                                                <span className="m-day-remaning--box" key={index}> { digit }</span>
                                                                            )
                                                                        })
                                                                    }
                                                                    <span className="ml-2 m-day-remaning--text">
                                                                        { course?.updated_status?.day_remaining > 1 ? 'Days' : 'Day'} <br />remaining
                                                                    </span>
                                                                </div>
                                                            </div>
                                                            }
                                                            { 
                                                                [1,2].includes(course?.auto_login_method)  ?
                                                                    <Link to={"#"} className="m-db-start-course font-weight-bold pr-10" onClick={()=>autoLogin(course?.order_id, course?.product, course?.auto_login_method )}>Start course</Link> : null
                                                            }
                                                        </div>
                                                    </div>

                                            {/*<div className="pl-15">
                                                <div className="m-courses-detail__bottomWrap" style={{ paddingBottom: '0' }}>
                                                    <div>
                                                        <div className="m-day-remaning mb-20">
                                                            {
                                                                (course?.options?.day_remaining > 0 ? course?.options?.day_remaining : '00')?.toString().split('').map((digit, index) => {
                                                                    return (
                                                                        <span className="m-day-remaning--box" key={index}> { digit}</span>
                                                                    )
                                                                })
                                                            }
                                                            <span className="ml-2 m-day-remaning--text">{course?.options?.day_remaining > 1 ? 'Days' : 'Day'} <br />remaning</span>
                                                        </div>

                                                        <div className="m-db-status">
                                                            <p className="mb-0 pb-1">Status: <strong>(0% Complete)</strong> </p>

                                                            <div className="m-progress">
                                                                <div role="progressbar" className="m-progress-bar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style={{width: "0"}}></div>
                                                            </div>
                                                        </div> 
                                                    </div>

                                                    <Link to={"#"} className="m-db-start-course font-weight-bold pr-10">Start course</Link>
                                                </div>
                                            </div>*/}

                                        <div className="pl-15">
                                            <div className="m-courses-detail__userInput">
                                                <Link className="m-db-comments font-weight-bold" to={'#'} onClick={(e) => {e.preventDefault();setShowCommentModal(true);setOiCommentId(course?.id)}}>
                                                    {/* { course?.no_of_comments ? course?.no_of_comments > 1 ? `${course?.no_of_comments} Comments` : `${course?.no_of_comments} Comment` : 'Add Comment' } */}
                                                    { course?.no_of_comments === 0 || !course?.no_of_comments ? 'Add Comment' : course?.no_of_comments === 1 ? course?.no_of_comments + ' Comment' : course?.no_of_comments + ' Comments' }
                                                </Link>
                                                {
                                                    course?.updated_status?.your_feedback &&
                                                        <div className="d-flex">
                                                            {
                                                                course?.len_review ? 
                                                                    <>
                                                                        <span className="m-rating" onClick={()=>{setShowRatingsModal(true);setOiReviewId({'prdId' :course?.product, 'orderId':course?.id});setReviewData(course?.review_data);}}>
                                                                            {
                                                                                course?.rating?.map((star, index) => starRatings(star, index))
                                                                            }
                                                                            <span className="ml-5">{course?.avg_rating?.toFixed(1)}/5</span>
                                                                        </span>
                                                                        <Link to={"#"} className="font-weight-bold ml-10">{ course?.len_review }</Link>
                                                                    </> :
                                                                    <>
                                                                        <span className="">Rate</span>
                                                                        <span className="m-rating" onClick={()=>{setShowRateModal(true);setOiReviewId({'prdId' :course?.product, 'orderId':course?.id})}}>
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
                                            </div>
                                        </div>
                                </div>
                            )
                        })
                    }
                </div>
                {
                    showCommentModal && <AddCommentModal setShowCommentModal = {setShowCommentModal} oi_id={oiCommentId} type="mycourses"/>
                }
                {
                    showRateModal && <RateProductModal setShowRateModal={setShowRateModal} idDict={oiReviewId} />
                }
                {
                    showRatingsModal && <ShowRatingsModal setShowRateModal={setShowRateModal} setShowRatingsModal={setShowRatingsModal} idDict={oiReviewId} reviewData={reviewData}/>
                }
                {
                    page?.total > 1 ?
                        <Pagination
                            totalPage={page?.total}
                            currentPage={currentPage}
                            setCurrentPage={setCurrentPage} /> : ''
                }
            </div>
            }
        </>
    )
}

export default MyCourses;