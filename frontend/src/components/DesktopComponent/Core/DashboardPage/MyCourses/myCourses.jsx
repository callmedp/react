import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ProgressBar } from 'react-bootstrap';
import { Collapse } from 'react-bootstrap';
import { Button } from 'react-bootstrap';
import { Modal } from 'react-bootstrap';
import NoCourses from './noCourses';
import './myCourses.scss';
import '../../SkillPage/NeedHelp/needHelp.scss';
import { startDashboardCoursesPageLoader, stopDashboardCoursesPageLoader } from 'store/Loader/actions/index';
import Loader from '../../../Common/Loader/loader';
import { useDispatch, useSelector } from 'react-redux';
import { fetchMyCourses } from 'store/DashboardPage/MyCourses/actions';
   
const MyCourses = (props) => {
    const [addOpen, setaddOpen] = useState('comment-1');
    // const [open, setOpen] = useState(false);
    // const [openReview, setOpenReview] = useState(false);
    // const [openViewDetail, setOpenViewDetail] = useState(-1);
    let [rating, setRating] = useState(-1);
    let [clicked, setClicked] = useState(false);
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const [results, setResults] = useState({});
    const dispatch = useDispatch();
    const { history } = props;
    const { coursesLoader } = useSelector(store => store.loader);
    const [isOpen, setIsOpen] = useState(false);
    const toggleDetails = (id) => setIsOpen(isOpen == id ? false : id);
    
    console.log(results);

    
    const handleEffects = async () => {
        try {
            //You may notice that apis corresponding to these actions are not getting called on initial render.
            //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
            //So there is no need to fetch them again on the browser.
            if (!(window && window.config && window.config.isServerRendered)) {
                dispatch(startDashboardCoursesPageLoader());
                const result = await new Promise((resolve, reject) => dispatch(fetchMyCourses({ resolve, reject })))
                setResults(result);
                dispatch(stopDashboardCoursesPageLoader());
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

    // fill starts of already rated courses
    const fillStarForCourse = (star) => {
        if(star === '*') return "icon-fullstar";
        else if(star === '+') return "icon-halfstar";
        else return "icon-blankstar";
      };

    // new rating
    const fillNewStar = (star) => {
        if (star <= rating) return "icon-fullstar";
        else return "icon-blankstar";
    };
    
    const setStars = (e, className = "blankstar") => {
        let data = typeof e == "number" ? e : parseInt(e.target.getAttribute("value")) - 1;
        let children = document.getElementsByClassName("rating-review")[0].children;
        for (let i = 0; i <= data; i++) {
            children[i].setAttribute("class", `icon-${className}`);
        }
    };

    const mouseOver = (e) => {
        setStars(4);
        setStars(e, "fullstar");
    };

    const wrapper = React.useRef(null);
    console.log(wrapper);
    
    const mouseOut = (e) => (!clicked ? setStars(e) : null);
        const onClickEvent = (e, val = 0) => {
        setRating(
            parseInt(e.target.getAttribute("value"))
            ? parseInt(e.target.getAttribute("value"))
            : val
        );
        setStars(e, "fullstar");
        setClicked(true);
    };

    useEffect(() => {
        handleEffects();
    }, [])

    return(
        <div>
            {/* <NoCourses /> */}
            { coursesLoader ? <Loader /> : ''}

            <div className="db-my-courses-detail">

                {results?.data?.length > 0 ?
                    results.data.map((item, index) => {
                        return (
                            <div className="db-white-box w-100" key={index}>
                                <div className="d-flex">
                                    <figure>
                                        <img src={item.img} alt={item.img_alt} />
                                    </figure>

                                    <div className="db-my-courses-detail--wrap">
                                        <div className="d-flex w-100">
                                            <div className="db-my-courses-detail__leftpan">
                                                <div className="db-my-courses-detail__leftpan--box">
                                                    <h3><Link to={item.url}>{item.heading}</Link></h3>
                                                    <div className="db-my-courses-detail__leftpan--info">
                                                        <span>Provider: <Link to={"#"}>{item.provider}</Link></span>
                                                        <span>Enrolled on: <strong>27 Oct 2020</strong></span>
                                                        <span>Duration: <strong>90 days</strong></span>
                                                        <span>Mode: <strong>Online</strong></span>
                                                        <span>Jobs: <strong>2892</strong></span>
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
                                                        <strong className="ml-1">Course yet to start</strong> 
                                                    </div>

                                                    <Link 
                                                        className="font-weight-bold"
                                                        onClick={() => toggleDetails(item.id)}
                                                        aria-controls="addComments"
                                                        aria-expanded={`openViewDetail`+index}
                                                        to={'#'}
                                                    >
                                                        View Details
                                                    </Link>

                                                    {/* course detail modal open */}
                                                    <Collapse in={isOpen == item.id}>
                                                        <div className="db-view-detail arrow-box left-big" id={`openViewDetail`+index}>
                                                        <span className="btn-close" onClick={() => toggleDetails(item.id)}>&#x2715;</span>
                                                            <ul className="db-timeline-list">
                                                                <li>
                                                                    <i className="db-timeline-list--dot"></i>
                                                                    <span>Dec. 11, 2020    |   By Amit Kumar {index}</span>
                                                                    <p className="db-timeline-list--text">Need help to understand this service.</p>
                                                                </li>
                                                                
                                                                <li>
                                                                    <i className="db-timeline-list--dot"></i>
                                                                    <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                                                    <p className="db-timeline-list--text">We will call you for detailed info of this service</p>
                                                                </li>
                                                                
                                                                <li>
                                                                    <i className="db-timeline-list--dot"></i>
                                                                    <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                                                    <p className="db-timeline-list--text">Thanks for your confirmation!</p>
                                                                </li>
                                                                <li>
                                                                    <i className="db-timeline-list--dot"></i>
                                                                    <span>Dec. 11, 2020    |   By Amit Kumar</span>
                                                                    <p className="db-timeline-list--text">Need help to understand this service.</p>
                                                                </li>
                                                                
                                                                <li>
                                                                    <i className="db-timeline-list--dot"></i>
                                                                    <span>Dec. 12, 2020    |   By Sumit Sharme</span>
                                                                    <p className="db-timeline-list--text">We will call you for detailed info of this service</p>
                                                                </li>
                                                                
                                                                <li>
                                                                    <i className="db-timeline-list--dot"></i>
                                                                    <span>Dec. 18, 2020    |   By Amit Kumar</span>
                                                                    <p className="db-timeline-list--text">Thanks for your confirmation!</p>
                                                                </li>
                                                            </ul>
                                                        </div>
                                                    </Collapse>
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
                                                    <span className="day-remaning--box">9</span>
                                                    <span className="day-remaning--box">0</span>
                                                    <span className="ml-2 day-remaning--text">Days <br/>remaning</span>
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
                                                onClick={() => setaddOpen(!addOpen)}
                                                aria-controls="addComments"
                                                aria-expanded={addOpen}
                                                to={"#"}
                                            >
                                                Add comment
                                            </Link>

                                            <div className="d-flex">
                                                <div className="card__rating">
                                                    <span 
                                                        className="cursor-pointer mr-2 font-weight-bold"
                                                        onClick={handleShow}
                                                    >
                                                        Rate course
                                                    </span>

                                                    <span className="rating">
                                                        {item.stars.map((val,ind) => {
                                                            return (
                                                                <i
                                                                key={ind}
                                                                value={val}
                                                                className={fillStarForCourse(val)}
                                                                ></i>
                                                            );
                                                        })}
                                                    </span>
                                                </div>

                                                {/* rate service modal */}
                                                <Modal show={show} onHide={handleClose} className="db-modal">
                                                    <Modal.Header closeButton>
                                                    </Modal.Header>
                                                    <Modal.Body>
                                                        <div className="text-center db-rate-services need-help">
                                                            <img src="/media/images/rate-services.png" className="img-fluid" alt=""/>
                                                            <p className="db-rate-services--heading">Rate service</p>
                                                            
                                                            <span className="rating-review">
                                                                {[1, 2, 3, 4, 5].map((value,indx) => {
                                                                    return (
                                                                        <i
                                                                        key={indx}
                                                                        value={value}
                                                                        ref={wrapper}
                                                                        className={fillNewStar(value)}
                                                                        // onMouseOver={(e) => mouseOver(e)}
                                                                        // onMouseOut={(e) => mouseOut(e)}
                                                                        onClick={(e) => onClickEvent(e)}
                                                                        ></i>
                                                                    );
                                                                })}
                                                            </span>
                                                            <p className="db-rate-services--subheading">Click on rate to scale of 1-5</p>
                                                            <form action="">
                                                                <div className="form-group">
                                                                    <input type="email" className="form-control" id="email" name="email" placeholder=" "
                                                                        value="" aria-required="true" aria-invalid="true" />
                                                                    <label htmlFor="">Email</label>
                                                                </div>
                                                                
                                                                <div className="form-group">
                                                                    <textarea  className="form-control" name="review" id="review" cols="30" rows="3" placeholder=" "></textarea>
                                                                    <label htmlFor="">Review</label>
                                                                </div>

                                                                <button className="btn btn-primary px-5">Submit</button>
                                                            </form>
                                                        </div>
                                                    </Modal.Body>
                                                </Modal>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        )
                    })
                : 
                <NoCourses /> 
                }
            </div>
        </div>
    )
}
   
export default MyCourses;