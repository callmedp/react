// React Core Import
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import Aos from "aos";

// Local Import 
import '../MyCourses/myCourses.scss'
import './myServices.scss';
import AddCommentModal from '../AddCommentModal/addCommentModal';
import RateProductModal from '../RateProductModal/rateProductModal';
import UploadResume from '../UploadResume/uploadResume';
import Loader from '../../../Common/Loader/loader';
import { startDashboardWalletPageLoader, stopDashboardWalletPageLoader } from 'store/Loader/actions/index';

// API Import
import { fetchMyServices } from 'store/DashboardPage/MyServices/actions/index';

function preventDefault(e) {
    e.preventDefault();
}

const MyServices = (props) => {
    const [showUpload, setShowUpload] = React.useState(false)
    const [showCommentModal, setShowCommentModal] = useState(false) 
    const [showRateModal, setShowRateModal] = useState(false) 
    const [isActive, setActive] = useState(false);
    const [datalist, setDatalist] = useState([]);
    const [data_id, setDataid] = useState(null);
    const [service_id, setServiceId] = useState(null);
    const showDetailtoggle = (data, id) => {
        setDataid(id);
        setDatalist(data);
        setActive(!isActive);
    };
    var supportsPassive = false;
    try {
        window.addEventListener("test", null, Object.defineProperty({}, 'passive', {
            get: function () { supportsPassive = true; }
        }));
    } catch (e) { }
    var wheelOpt = supportsPassive ? { passive: false } : false;
    const showUploadToggle = (id) => {
        setServiceId(id);
        setShowUpload(!showUpload);
        if (!showUpload) {
            window.addEventListener('touchmove', preventDefault, wheelOpt); // mobile
        }
        else {
            window.removeEventListener('touchmove', preventDefault, wheelOpt); // mobile
        }
    };
    const dispatch = useDispatch();
    const { data, page } = useSelector(store => store?.dashboardServices);
    const { walletLoader } = useSelector(store => store.loader);
    const myServicesList = data
    const handleEffects = async () => {
        if (!(window && window.config && window.config.isServerRendered)) {
            dispatch(startDashboardWalletPageLoader());
            await new Promise((resolve, reject) => dispatch(fetchMyServices({ resolve, reject })));
            dispatch(stopDashboardWalletPageLoader());
        }
        else {
            delete window.config?.isServerRendered
        }

    };

    useEffect(() => {
        handleEffects();
    }, [])

    return (
        <>
        { walletLoader && <Loader />}
        <div>

            <main className="mb-0">
                <div className="m-courses-detail db-warp">
                    {
                        myServicesList?.map((service, key) => {
                            return (
                                <div className="m-card pl-0" key={key}>
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
                                            {/* <img src="https://learning-media-staging-189607.storage.googleapis.com/l/m/product_image/1/1532923787_9385.png" alt={service?.heading} /> */}
                                            <img src={service?.img} alt={service?.heading} />
                                        </figure>
                                        <div className="m-courses-detail__info">
                                            <Link to={service?.productUrl}><h2>{service?.name}</h2></Link>
                                            <p className="m-pipe-divides mb-5">Provider: <strong>{service?.vendor}</strong> </p>
                                            <p className="m-pipe-divides mb-5"><span>Bought on: <strong>{service?.enroll_date}</strong> </span> <span>Duration: <strong>{service?.duration}</strong> </span></p>
                                        </div>
                                    </div>

                                    <StatusFlow product_flow={service?.product_type_flow} status={service?.status} history={service?.datalist} />

                                    { service?.status === 'Cancelled' ? '' :
                                        <div className="m-courses-detail--alert mt-15">
                                            To initiate your service upload your latest resume
                                            </div>
                                    }
                                    { service?.status === 'Cancelled' ?

                                        <div className="pl-15 mt-15 fs-12">
                                            Status: <strong>{service?.status}</strong>


                                            <div className="my-order__order-detail">
                                                <a onClick={() => showDetailtoggle(service?.datalist, key)} className={`arrow-icon ${isActive && key === data_id ? 'open' : ''} font-weight-bold`}>Views Details</a>
                                                <ul className="my-order__order-detail--info mt-15" style={isActive && key === data_id ? { display: 'block' } : { display: 'none' }}>
                                                    {
                                                        datalist.map((data, key) =>
                                                            <li key={key}>
                                                                {/* <Link to={"#"} className="d-block mb-0"> { data } </Link> */}
                                                                <span> <strong> {data} </strong></span>
                                                            </li>)
                                                    }
                                                </ul>
                                            </div>

                                        </div>
                                        :
                                        <>
                                            <div className="pl-15 mt-15 fs-12">
                                                Status: <strong> {service?.datalist} </strong>

                                                {/* { service?.options } */}
                                                {Object.keys(service?.options).length === 0 && service?.options.constructor === Object ? '' : service?.options['Upload Resume'] === true ?
                                                    <a onClick={() => showUploadToggle(service?.id)} className="font-weight-bold">Upload</a> : ''
                                                }
                                                <div className="my-order__order-detail">
                                                    <a onClick={() => showDetailtoggle(service?.datalist, key)} className={`arrow-icon ${isActive && key === data_id ? 'open' : ''} font-weight-bold`}>Views Details</a>
                                                    <ul className="my-order__order-detail--info mt-15" style={isActive && key === data_id ? { display: 'block' } : { display: 'none' }}>
                                                        {
                                                            datalist.map((data, key) =>
                                                                <li key={key}>
                                                                    {/* <Link to={"#"} className="d-block mb-0"> { data } </Link> */}
                                                                    <span> <strong> {data} </strong></span>
                                                                </li>)
                                                        }
                                                    </ul>
                                                </div>
                                            </div>
                                            <div className="pl-15">
                                                <div className="m-courses-detail__bottomWrap">
                                                    <div>
                                                        <div className="m-day-remaning">
                                                            {
                                                                service.remaining_days.toString().split('').map((digit) => {
                                                                    return (
                                                                        <span className="m-day-remaning--box"> { digit }</span>
                                                                    )
                                                                })
                                                            }
                                                            <span className="ml-2 m-day-remaning--text">Days <br />remaning</span>
                                                        </div>
                                                    </div>
                                                    <Link to={"#"} className="m-db-start-course font-weight-bold pr-10">Start Service</Link>
                                                </div>

                                                <div className="m-courses-detail__userInput">
                                                    <Link to={'#'} onClick={(e) => {e.preventDefault();setShowCommentModal(true)}} className="m-db-comments font-weight-bold">3 Comment</Link>
                                                    <div className="d-flex" onClick={()=>{setShowRateModal(true)}}>
                                                        <span className="m-rating">
                                                            <em className="micon-fullstar"></em>
                                                            <em className="micon-fullstar"></em>
                                                            <em className="micon-fullstar"></em>
                                                            <em className="micon-fullstar"></em>
                                                            <em className="micon-blankstar"></em>
                                                            <span className="ml-5">4/5</span>
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </>
                                    }

                                </div>
                            )
                        })
                    }
                </div>
                
                <UploadResume showUpload={showUpload} showUploadToggle={showUploadToggle}/>
                
            </main>
            {
                showCommentModal && <AddCommentModal setShowCommentModal = {setShowCommentModal} />
            }
            {
                showRateModal && <RateProductModal setShowRateModal={setShowRateModal} />
            }
        </div>
        </>
    )
}

const StatusFlow = (props) => {

    if (props.product_flow === 1 || props.product_flow === 12 || props.product_flow) {
        return (
            <>
            </>
        )
    }
    else {
        return (
            <>

            </>
        )
    }
}


export default MyServices;