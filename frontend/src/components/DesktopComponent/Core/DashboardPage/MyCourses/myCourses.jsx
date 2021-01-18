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
    // const [addOpen, setaddOpen] = useState('comment-1');
    // const [open, setOpen] = useState(false);
    // const [openReview, setOpenReview] = useState(false);
    // const [openViewDetail, setOpenViewDetail] = useState(-1);
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const [results, setResults] = useState({});
    const dispatch = useDispatch();
    const { history } = props;
    const { coursesLoader } = useSelector(store => store.loader);
    console.log(results);

    const [isOpen, setIsOpen] = useState(false);
    const toggleDetails = (id) => setIsOpen(isOpen == id ? false : id);
    
    
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

    useEffect(() => {
        handleEffects();
    }, [])

    return(
        <div>
            {/* <NoCourses /> */}
            { coursesLoader ? <Loader /> : ''}

            <div className="db-my-courses-detail">

                {results?.length > 0 ?
                    results.map((item, index) => {
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