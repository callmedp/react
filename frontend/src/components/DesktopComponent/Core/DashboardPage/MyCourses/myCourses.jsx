import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ProgressBar } from 'react-bootstrap';
import NoCourses from '../Inbox/emptyInbox';
import './myCourses.scss';
import '../../SkillPage/NeedHelp/needHelp.scss';
import { startDashboardCoursesPageLoader, 
    stopDashboardCoursesPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMyCourses } from 'store/DashboardPage/MyCourses/actions';
import { siteDomain } from 'utils/domains';
import ViewDetailModal from '../Inbox/viewDetailModal';
import RateModal from '../Inbox/rateModal';
import ReviewRating from '../Inbox/reviewRating';
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

    useEffect(() => {
        handleEffects();
    }, [currentPage, filterState])

    const toggleReviews = async (id, prod) => {
        if(openReview != id) {
            dispatch(startReviewLoader());
            await new Promise((resolve, reject) => dispatch(fetchReviews({ payload: { prod: prod, page: currentPage, isDesk: true, ...filterState, type: 'GET'}, resolve, reject })));
            dispatch(stopReviewLoader());
        }
        setOpenReview(openReview == id ? false : id);
    }

    const addCommentDataFetch = async (id) => {
        setAddOpen(addOpen == id ? false : id);
        let commVal = {
            oi_id: id,
            type: 'GET'
        }
        if(addOpen != id){
            dispatch(startCommentLoader())
            await new Promise((resolve, reject) => dispatch(fetchOiComment({payload: commVal, resolve, reject})));
            dispatch(stopCommentLoader())
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

    const handleEffects = async () => {
        try {
            //You may notice that apis corresponding to these actions are not getting called on initial render.
            //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
            //So there is no need to fetch them again on the browser.
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardCoursesPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyCourses({ page: currentPage, isDesk: true, ...filterState, resolve, reject })))
                dispatch(stopDashboardCoursesPageLoader());
            }
            else {
                //isServerRendered is needed to be deleted because when routing is done through react and not on the node,
                //above actions need to be dispatched.
                delete window.config?.isServerRendered
            }
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
            { page.total === 0 ? <EmptyInbox/> : '' }

            <BreadCrumbs filterState={filterState} setfilterState={setfilterState} />

            <div className="db-my-courses-detail">

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
                                                        { !!course.vendor && <span>Provider: <Link className="noLink" to={"#"}>{course.vendor}</Link></span> }
                                                        { !!course.enroll_date && <span>Enrolled on: <strong>{course.enroll_date}</strong></span> }
                                                        { !!course.duration && <span>Duration: <strong>{course.duration}</strong></span> }
                                                        { !!course.mode && <span>Mode: <strong>{course.mode}</strong></span> }
                                                        { !!course.jobs && <span>Jobs: <strong>{course.jobs}</strong></span> }
                                                    </div>

                                                    <div className="db-my-courses-detail__leftpan--session">
                                                        <span>Next session : <strong>Basic of Digital Marketing</strong></span>
                                                        <span className="db-icon-date font-weight-bold">3PM |  29 nov 2020</span>
                                                    </div>

                                                    <div className="db-my-courses-detail__leftpan--alert">
                                                        Hi, the recording for the session you missed is available now <Link to={"#"} className="ml-2">Click here</Link>
                                                    </div>

                                                    <div className="db-my-courses-detail__leftpan--status mb-2">
                                                        { course.status || course.new_oi_status ? 'Status':''}
                                                        <strong className="ml-1">{course.status ?? course.new_oi_status}</strong>
                                                        &emsp;
                                                        {course.product_type_flow === 2 || course.product_type_flow === 14 ?
                                                            <React.Fragment>
                                                                {(course?.vendor === 'neo' && course?.oi_status === 5) ? 
                                                                    course?.BoardOnNeo ? <a className="ml-2" onClick={NeoBoardUser(course.id)}>Board On Neo</a> : 
                                                                    (course?.neo_mail_sent) ? <strong className="ml-1">Please Confirm Boarding on Mail Sent to you</strong> :
                                                                    (course?.updated_from_trial_to_regular) ? <strong className="ml-1">Updated Account from Trial To Regular</strong> 
                                                                    : null
                                                                    : null}
                                                            </React.Fragment>
                                                        : null}

                                                        {/* take test when type flow is 16 */}
                                                        {course?.options?.take_test ? <a className="ml-2" target="_blank" href={ course?.options?.auto_login_url}>Take Test</a> : null}
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
                                                    <ViewDetailModal 
                                                        id={course.id} 
                                                        toggleDetails={toggleDetails}  
                                                        isOpen={isOpen}
                                                        datalist={course.datalist || []}
                                                    />
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

                                                <div className="day-remaning mb-20">
                                                    {[...(course.remaining_days + '')].map((day, idx) => <span key={idx} className="day-remaning--box">{day}</span>)}

                                                    <span className="ml-2 day-remaning--text">{course.remaining_days > 1 ? 'Days' : 'Day'} <br />remaning</span>
                                                </div>

                                                <div className="db-status mt-20">
                                                    <p className="mb-0 pb-1">Status: <strong>(0% Complete)</strong> </p>
                                                    <ProgressBar now={0} />
                                                </div>

                                                <Link to={"#"} className="db-start-course font-weight-bold mt-30">Start course</Link>
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

                                            <div className="d-flex">
                                                <div className="db-certificate">
                                                    <i className="db-certificate-icon"></i>
                                                    <span className="db-certificate--text arrow-box top">Download certificate</span>
                                                </div>
                                                <ReviewRating
                                                    item={course}
                                                    handleShow={handleShow}
                                                    toggleReviews={toggleReviews} 
                                                    setOpenReview={setOpenReview}
                                                    openReview={openReview}
                                                    name="Course"/>

                                                {/* rate service modal */}
                                                <RateModal handleClose={handleClose} show={show} name="Course"/>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <AddCommentModal id={course.id} addCommentDataFetch={addCommentDataFetch} data={oiComments} addOpen={addOpen} />

                                <div className="db-mycourse-highlighter">Next course to take: <Link to={"#"} className="font-weight-bold ml-2">Seo Specialist</Link> </div>
                            </div>
                        )
                    })
                }
                  {/* pagination set here */}
                  { page?.total > 1 ? <Pagination totalPage={ page?.total} currentPage={currentPage} setCurrentPage={setCurrentPage}/> : ''}
            </div>
        </div>
    )
}

export default MyCourses;