import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import './myCourses.scss';
import AddCommentModal from '../AddCommentModal/addCommentModal';
import RateProductModal from '../RateProductModal/rateProductModal'
import Pagination from '../../../Common/Pagination/pagination';
import Loader from '../../../Common/Loader/loader';
import { fetchMyCourses } from 'store/DashboardPage/MyCourses/actions/index'
import { startDashboardCoursesPageLoader, stopDashboardCoursesPageLoader } from 'store/Loader/actions/index';
import { siteDomain } from 'utils/domains';

const MyCourses = (props) => {
    const [showCommentModal, setShowCommentModal] = useState(false)
    const [showRateModal, setShowRateModal] = useState(false)
    const [currentPage, setCurrentPage] = useState(1)
    const [showOrderDetailsID, setShowOrderDetailsID] = useState('')
    const [oiCommentId, setOiCommentId] = useState('')
    const [oiReviewId, setOiReviewId] = useState({})
    
    const dispatch = useDispatch();
    const { myCourses, page } = useSelector(store => store?.dashboardCourses);
    const { coursesLoader } = useSelector(store => store.loader);

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

    const handleEffects = async () => {
        if (!(window && window.config && window.config.isServerRendered)) {
            dispatch(startDashboardCoursesPageLoader());
            await new Promise((resolve, reject) => dispatch(fetchMyCourses({ page: currentPage, resolve, reject })));
            dispatch(stopDashboardCoursesPageLoader());
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
            <div>
                <div className="m-courses-detail db-warp">
                    {
                        myCourses?.map((course, index) => {
                            return(
                                <div className="m-card pl-0" key={index}>
                                    <div className="m-share" aria-haspopup="true">
                                        <i className="icon-share"></i>
                                        <div className="m-share__box m-arrow-box m-top">
                                            <a target="_blank" href={`https://www.facebook.com/sharer/sharer.php?u=${siteDomain}${course?.productUrl}`} className="m-facebook-icon"></a>
                                            <a target="_blank" href={`https://www.linkedin.com/shareArticle?mini=true&url=${siteDomain}${course?.productUrl}&title=${course?.title}&summary=${course.name}&source=`} className="m-linkedin-icon"></a>
                                            <a target="_blank" href={`https://twitter.com/intent/tweet?url=${siteDomain}${course?.productUrl}/&text=${course.name}`} className="m-twitter-iocn"></a>
                                            <Link to={"#"} className="m-whatsup-icon"></Link>
                                        </div>
                                    </div>

                                    <div className="d-flex">
                                        <figure>
                                            <img src={course?.img} alt={course?.title} />
                                        </figure>
                                        <div className="m-courses-detail__info">
                                            <h2>{course?.name}</h2>
                                            <p className="m-pipe-divides mb-5">Provider: <Link to={"#"} className="font-weight-bold">{course?.vendor}</Link></p>
                                            <p className="m-pipe-divides mb-5"><span>Enrolled on: <strong>{course?.enroll_date}</strong> </span> <span>Mode: <strong>{course?.mode}</strong> </span></p>
                                            <p className="m-pipe-divides mb-5">{ course?.status === 'Cancelled' || course?.status === 'Unpaid' || course.status === 'Yet to Update' ? '' : <span> Duration: <strong>{course?.oi_duration} {course?.oi_duration > 1 ? 'days' : 'day'}</strong> </span> } <span>Jobs: <strong>{course?.jobs}</strong> </span></p>
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
                                                Status: <strong> { course?.status } </strong>
                                                {/* <Link to={"#"} className="d-block font-weight-bold">View Details</Link> */}
                                                {
                                                    course?.datalist?.length ?
                                                        <div className="my-order__order-detail">
                                                            <a onClick={(e) => { e.preventDefault(); showDetails(course?.id) }} className={(showOrderDetailsID === course?.id) ? "d-block font-weight-bold open arrow-icon" : "d-block font-weight-bold arrow-icon"}>View Details</a>
                                                            {(showOrderDetailsID === course?.id) && getOrderDetails(course?.datalist)}

                                                        </div> : ''
                                                }
                                            </div>

                                            <div className="pl-15">
                                                <div className="m-courses-detail__bottomWrap" style={{ paddingBottom: '0' }}>
                                                    <div>
                                                        <div className="m-day-remaning mb-20">
                                                            {
                                                                course?.remaining_days?.toString().split('').map((digit, index) => {
                                                                    return (
                                                                        <span className="m-day-remaning--box" key={index}> { digit}</span>
                                                                    )
                                                                })
                                                            }
                                                            <span className="ml-2 m-day-remaning--text">{course?.remaining_days > 1 ? 'Days' : 'Day'} <br />remaning</span>
                                                        </div>

                                                        {/* <div className="m-db-status">
                                                    <p className="mb-0 pb-1">Status: <strong>(0% Complete)</strong> </p>

                                                    <div className="m-progress">
                                                        <div role="progressbar" className="m-progress-bar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style={{width: "0"}}></div>
                                                    </div>
                                                </div> */}
                                                    </div>

                                                    {/* <Link to={"#"} className="m-db-start-course font-weight-bold pr-10">Start course</Link> */}
                                                </div>
                                            </div>

                                        <div className="m-courses-detail__userInput">
                                            <Link className="m-db-comments font-weight-bold" to={'#'} onClick={(e) => {e.preventDefault();setShowCommentModal(true);setOiCommentId(course?.id)}}>
                                                { course?.no_of_comments ? course?.no_of_comments > 1 ? `${course?.no_of_comments} Comments` : `${course?.no_of_comments} Comment` : 'Add Comment' }
                                            </Link>
                                            <div className="d-flex" onClick={()=>{setShowRateModal(true);setOiReviewId({'prdId' :course?.product, 'orderId':course?.id})}}>
                                                {
                                                    course?.no_review ? 
                                                        <>
                                                            <span className="m-rating">
                                                                {
                                                                    course?.rating?.map((star, index) => starRatings(star, index))
                                                                }
                                                                <span className="ml-5">{course?.avg_rating?.toFixed(1)}/5</span>
                                                            </span>
                                                            <Link to={"#"} className="font-weight-bold ml-10">{ course?.no_review }</Link>
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
                            )
                        })
                    }

                    {/* <div className="m-card pl-0">
                        <div className="m-share" aria-haspopup="true">
                            <i className="icon-share"></i>
                            <div className="m-share__box m-arrow-box m-top">
                                <Link to={"#"} className="m-facebook-icon"></Link>
                                <Link to={"#"} className="m-linkedin-icon"></Link>
                                <Link to={"#"} className="m-twitter-iocn"></Link>
                                <Link to={"#"} className="m-whatsup-icon"></Link>
                            </div>
                        </div>

                        <div className="d-flex">
                            <figure>
                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                            </figure>
                            <div className="m-courses-detail__info">
                                <h2>Certified Digital Marketing Master Certification</h2>
                                <p className="m-pipe-divides mb-5">Provider: <Link to={"#"} className="font-weight-bold">Vskills</Link></p>
                                <p className="m-pipe-divides mb-5"><span>Enrolled on: <strong>27 Oct 2020</strong> </span> <span>Mode: <strong>Online</strong> </span></p>
                                <p className="m-pipe-divides mb-5"><span>Duration: <strong>90 days</strong> </span> <span>Jobs: <strong>2892</strong> </span></p>
                            </div>
                        </div>


                        <div className="pl-15 mt-15 fs-12">
                            Status: <strong>Course yet to start</strong>
                            <Link to={"#"} className="d-block font-weight-bold">View Details</Link>
                        </div>

                        <div className="pl-15">
                            <div className="m-courses-detail__bottomWrap">
                                <div>
                                    <div className="m-db-status">
                                        <p className="mb-0 pb-1">Status: <strong>(100% Complete)</strong> 
                                            <i className="m-db-green-tick"></i> 
                                        </p>

                                        <div className="m-progress">
                                            <div role="progressbar" className="m-progress-bar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style={{width: "100%"}}></div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div className="d-flex align-items-center justify-content-end">
                                    <Link to={"#"} className="font-weight-bold fs-13 mr-30">View result</Link>
                                    <Link to={"#"} className="m-db-certificate-icon"></Link>
                                </div>
                            </div>

                            <div className="m-courses-detail__userInput">
                                <Link to={"#"} className="m-db-comments font-weight-bold">3 Comment</Link>
                                <div className="d-flex">
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span className="ml-5">4/5</span>
                                    </span>
                                    <Link to={"#"} className="font-weight-bold ml-10">2</Link>
                                </div>
                            </div>
                        </div>

                        <div className="m-mycourse-highlighter">Next course to take: <Link to={"#"} className="font-weight-bold ml-2">Seo Specialist</Link> </div>
                    </div>

                    <div className="m-card pl-0">
                        <div className="m-share" aria-haspopup="true">
                            <i className="icon-share"></i>
                            <div className="m-share__box m-arrow-box m-top">
                                <Link to={"#"} className="m-facebook-icon"></Link>
                                <Link to={"#"} className="m-linkedin-icon"></Link>
                                <Link to={"#"} className="m-twitter-iocn"></Link>
                                <Link to={"#"} className="m-whatsup-icon"></Link>
                            </div>
                        </div>

                        <div className="d-flex">
                            <figure>
                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                            </figure>
                            <div className="m-courses-detail__info">
                                <h2>Certified Digital Marketing Master Certification</h2>
                                <p className="m-pipe-divides mb-5">Provider: <Link to={"#"} className="font-weight-bold">Vskills</Link></p>
                                <p className="m-pipe-divides mb-5"><span>Enrolled on: <strong>27 Oct 2020</strong> </span> <span>Mode: <strong>Online</strong> </span></p>
                                <p className="m-pipe-divides mb-5"><span>Duration: <strong>90 days</strong> </span> <span>Jobs: <strong>2892</strong> </span></p>
                            </div>
                        </div>

                        <div className="pl-15 mt-15 fs-12">
                            Status: <strong>Course in progress</strong>
                            <Link to={"#"} className="d-block font-weight-bold">View Details</Link>
                        </div>

                        <div className="pl-15">
                            <div className="m-courses-detail__bottomWrap">
                                <div>
                                    <div className="m-day-remaning mb-20">
                                        <span className="m-day-remaning--box">3</span>
                                        <span className="m-day-remaning--box">0</span>
                                        <span className="ml-2 m-day-remaning--text">Days <br/>remaning</span>
                                    </div>

                                    <div className="m-db-status">
                                        <p className="mb-0 pb-1">Status: <strong>(0% Complete)</strong> </p>

                                        <div className="m-progress">
                                            <div role="progressbar" className="m-progress-bar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style={{width: "0"}}></div>
                                        </div>
                                    </div>
                                </div>

                                <Link to={"#"} className="m-db-resume-course font-weight-bold mt-30">Resume course</Link>
                            </div>

                            <div className="m-courses-detail__userInput">
                                <Link to={"#"} className="m-db-comments font-weight-bold">3 Comment</Link>
                                <div className="d-flex">
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span className="ml-5">4/5</span>
                                    </span>
                                    <Link to={"#"} className="font-weight-bold ml-10">2</Link>
                                </div>
                            </div>
                        </div>
                    </div> */}
                </div>
                {
                    showCommentModal && <AddCommentModal setShowCommentModal = {setShowCommentModal} oi_id={oiCommentId}/>
                }
                {
                    showRateModal && <RateProductModal setShowRateModal={setShowRateModal} idDict={oiReviewId}/>
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

export default MyCourses;