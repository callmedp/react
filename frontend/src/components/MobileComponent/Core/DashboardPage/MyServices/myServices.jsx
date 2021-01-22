// React Core Import
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';

// Local Import 
import '../MyCourses/myCourses.scss'
import './myServices.scss';
import AddCommentModal from '../AddCommentModal/addCommentModal';
import RateProductModal from '../RateProductModal/rateProductModal';
import UploadResume from '../UploadResume/uploadResume';
import Loader from '../../../Common/Loader/loader';
import { startDashboardServicesPageLoader, stopDashboardServicesPageLoader } from 'store/Loader/actions/index';

// API Import
import { fetchMyServices } from 'store/DashboardPage/MyServices/actions/index';

const MyServices = (props) => {

    const dispatch = useDispatch();
    const { data, page } = useSelector(store => store?.dashboardServices);
    const { serviceLoader } = useSelector(store => store.loader);
    const myServicesList = data
    
    const [showUpload, setShowUpload] = useState(false)
    const [showCommentModal, setShowCommentModal] = useState(false) 
    const [showRateModal, setShowRateModal] = useState(false) 
    const [showOrderDetailsID, setShowOrderDetailsID] = useState('')
    const [ordPageNo, setOrdPageNo] = useState(1)
    const [oiId, setOiId] = useState('')

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

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+' 
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    const handleEffects = async () => {
        if (!(window && window.config && window.config.isServerRendered)) {
            dispatch(startDashboardServicesPageLoader());
            await new Promise((resolve, reject) => dispatch(fetchMyServices({page: ordPageNo, resolve, reject })));
            dispatch(stopDashboardServicesPageLoader());
        }
        else {
            delete window.config?.isServerRendered
        }

    };

    useEffect(() => {
        handleEffects();
    }, [ordPageNo])

    return (
        <>
        { serviceLoader && <Loader />}
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
                                            <img src={service?.img} alt={service?.heading} />
                                        </figure>
                                        <div className="m-courses-detail__info">
                                            <Link to={service?.productUrl}><h2>{service?.name}</h2></Link>
                                            <p className="m-pipe-divides mb-5">Provider: <strong>{service?.vendor}</strong> </p>
                                            <p className="m-pipe-divides mb-5"><span>Bought on: <strong>{service?.enroll_date}</strong> </span> {service?.oi_duration && <span>Duration: <strong>{service?.oi_duration > 1 ? service?.oi_duration + ' days' : service?.oi_duration + ' day' } </strong> </span>}</p>
                                        </div>
                                    </div>

                                    { service?.options?.upload_resume &&
                                        <div className="m-courses-detail--alert mt-15">
                                            To initiate your service upload your latest resume
                                        </div>
                                    }
                                    { service?.status === 'Cancelled' ?

                                        <div className="pl-15 mt-15 fs-12">
                                            Status: <strong>{service?.status}</strong>


                                            {
                                                service?.datalist?.length ? 
                                                    <div className="my-order__order-detail">
                                                        <a onClick={(e) => {e.preventDefault();showDetails(service?.id)}} className={(showOrderDetailsID === service?.id) ? "font-weight-bold open arrow-icon" : "font-weight-bold arrow-icon"}>View Details</a>
                                                        { (showOrderDetailsID === service?.id) && getOrderDetails(service?.datalist) }
                                                    </div> : ''
                                            }

                                        </div>
                                        :
                                        <>
                                            <div className="pl-15 mt-15 fs-12">
                                                Status: <strong> {service?.status} </strong>

                                                {
                                                    service?.options?.upload_resume && <a onClick={() => setShowUpload(true)} className="font-weight-bold">Upload</a> 
                                                }
                                                {
                                                    service?.datalist?.length ? 
                                                        <div className="my-order__order-detail">
                                                            <a onClick={(e) => {e.preventDefault();showDetails(service?.id)}} className={(showOrderDetailsID === service?.id) ? "font-weight-bold open arrow-icon" : "font-weight-bold arrow-icon"}>View Details</a>
                                                            { (showOrderDetailsID === service?.id) && getOrderDetails(service?.datalist) }
                                                            
                                                        </div> : ''
                                                }
                                            </div>
                                            <div className="pl-15">
                                            {
                                                service?.oi_duration &&
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
                                                            <span className="ml-2 m-day-remaning--text">{ service?.remaining_days > 1 ? 'Days' : 'Day'}<br />remaining</span>
                                                        </div>
                                                    </div>
                                                    <Link to={"#"} className="m-db-start-course font-weight-bold pr-10">Start Service</Link>
                                                </div>
                                            }

                                                <div className="m-courses-detail__userInput">
                                                    <Link to={'#'} onClick={(e) => {e.preventDefault();setShowCommentModal(true);setOiId(service?.id)}} className="m-db-comments font-weight-bold">Add Comments</Link>
                                                    <div className="d-flex" onClick={()=>{setShowRateModal(true)}}>
                                                        <span className="m-rating">
                                                            { service?.rating?.map((star, index) => starRatings(star, index)) }
                                                            <span className="ml-5">{service?.avg_rating?.toFixed(1)}/5</span>
                                                        </span>
                                                        <Link to={"#"} className="font-weight-bold ml-10">2</Link>
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
                
            </main>
            {
                showCommentModal && <AddCommentModal setShowCommentModal = {setShowCommentModal} oi_id={oiId} />
            }
            {
                showRateModal && <RateProductModal setShowRateModal={setShowRateModal} />
            }
            {
                showUpload && <UploadResume setShowUpload={setShowUpload}/>
            }
            <span onClick={()=>setOrdPageNo(ordPageNo + 1)}>&emsp; &emsp; &emsp;{ ordPageNo }</span>
        </div>
        </>
    )
}


export default MyServices;