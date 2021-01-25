import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ProgressBar } from 'react-bootstrap';
import NoCourses from './noCourses';
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
import { Collapse } from 'react-bootstrap';

const MyCourses = (props) => {
    
    const [addOpen, setAddOpen] = useState(false);
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const handleComment = (id) => setAddOpen( addOpen === id ? false : id );
    const dispatch = useDispatch();
    const { history } = props;
    const { coursesLoader } = useSelector(store => store.loader);
    const { myCourses } = useSelector(store => store.dashboardCourses);
    const [isOpen, setIsOpen] = useState(false);
    const toggleDetails = (id) => setIsOpen(isOpen === id ? false : id);
    const [openReview, setOpenReview] = useState(false);
    const toggleReviews = (id) => setOpenReview(openReview == id ? false : id);

    useEffect(() => {
        handleEffects();
    }, [])

    const handleEffects = async () => {
        try {
            //You may notice that apis corresponding to these actions are not getting called on initial render.
            //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
            //So there is no need to fetch them again on the browser.
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardCoursesPageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMyCourses({ resolve, reject })))
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

            <div className="db-my-courses-detail">

                {
                    myCourses?.map((course, index) => {
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
                                                        Status:
                                                        <strong className="ml-1">{course.oi_status}</strong>
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
                                                        datalist={course.datalist}
                                                    />
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
                                                    {[...course.remaining_days+''].map((day, idx) => <span key={idx} className="day-remaning--box">{day}</span>)}

                                                    <span className="ml-2 day-remaning--text">Days <br />remaning</span>
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
                                                onClick={() => setAddOpen(!addOpen)}
                                                aria-controls="addComments"
                                                aria-expanded={addOpen}
                                                to={"#"}
                                            >
                                                Add comment
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
                                                    openReview={openReview}/>

                                                {/* rate service modal */}
                                                <RateModal handleClose={handleClose} show={show} />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <Collapse in={addOpen === course.id}>
                                    <div className="db-add-comments lightblue-bg" id={`addComments ${course.id}`}>
                                        <span className="btn-close" onClick={() => handleComment(course.id)}>&#x2715;</span>
                                        <p className="font-weight-semi-bold"> Add comment </p>
                                        <textarea className="form-control" rows="3"></textarea>
                                        <button type="submit" className="btn btn-outline-primary mt-20 px-5">Submit</button>
                                    </div>
                                </Collapse>

                                <div className="db-mycourse-highlighter">Next course to take: <Link to={"#"} className="font-weight-bold ml-2">Seo Specialist</Link> </div>
                            </div>
                        )
                    })
                }
            </div>
        </div>
    )
}

export default MyCourses;