// React Core Import
import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Link } from 'react-router-dom';
import Aos from "aos";

// Local Import 
import '../MyCourses/myCourses.scss'
import './myServices.scss';

// API Import
import { fetchServices } from 'store/DashboardPage/Service/actions/index';

function preventDefault(e) {
    e.preventDefault();
  }

const MyServices = (props) => {
    const [showUpload, setShowUpload] = React.useState(false)
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
    } catch(e) {}
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
    const [showSearchPage, setShowSearchPage] = useState(false)
    const myServicesList = useSelector(store => store.allServices?.data);
    const handleEffects = async () => {
        Aos.init({ duration: 2000, once: true, offset: 10, anchorPlacement: 'bottom-bottom' });
        //You may notice that apis corresponding to these actions are not getting called on initial render.
        //This is because initial render is done on node server, which is calling these apis, map the data and send it to the browser.
        //So there is no need to fetch them again on the browser.
        if (!(window && window.config && window.config.isServerRendered)) {
            await new Promise((resolve, reject) => dispatch(fetchServices({ resolve, reject })));
        }
        else {
            //isServerRendered is needed to be deleted because when routing is done through react and not on the node,
            //above actions need to be dispatched.
            delete window.config?.isServerRendered
        }

    };

    useEffect(() => {
        handleEffects();
    }, [])

    return (
        <div>

            <main className="mb-0">
                <div className="m-courses-detail db-warp">
                    {
                        myServicesList?.map((service, key) => {
                            if (key == 10 || key == 11) {
                                return (
                                    <>
                                    </>
                                )

                            }
                            else {
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
                                                <img src={ service?.img } alt={ service?.heading } />
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
                                                                <span className="m-day-remaning--box">9</span>
                                                                <span className="m-day-remaning--box">0</span>
                                                                <span className="ml-2 m-day-remaning--text">Days <br />remaning</span>
                                                            </div>
                                                        </div>
                                                        <Link to={"#"} className="m-db-start-course font-weight-bold pr-10">Start Service</Link>
                                                    </div>

                                                    <div className="m-courses-detail__userInput">
                                                        <Link to="/404" className="m-db-comments font-weight-bold">3 Comment</Link>
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
                                            </>
                                        }

                                    </div>
                                )
                            }
                        })
                    }
                </div>

                <div className="m-slide-modal">
                    <div className="text-center" style={{ display: 'none' }}>
                        <span className="m-db-close">&#x2715;</span>
                        <h2 className="mt-15">Get a Better resume by sharing us the feedback for resume</h2>
                        <div className="m-enquire-now mt-15">
                            <div className="m-form-group">
                                <textarea id="addComments" placeholder=" " rows="4"></textarea>
                                <label htmlFor="addComments">Enter feedback here</label>
                            </div>

                            <button className="btn btn-blue">Submit</button>
                        </div>
                    </div>

                    <div className="text-center" style={showUpload ? { display: 'block' } : { display: 'none' }}>
                        <span onClick={showUploadToggle} className="m-db-close">&#x2715;</span>
                        <h2>Upload Resume </h2>
                        <p>To initiate your services, <strong>upload resume</strong></p>
                        <div className="d-flex align-items-center justify-content-center mt-20">
                            <div className="m-upload-btn-wrapper">
                                <button className="btn btn-blue-outline">Upload a file</button>
                                <input type="file" name="myfile" />
                            </div>

                            <span className="mx-4">Or</span>

                            <div className="m-custom">
                                <input type="checkbox" id="shineResume" />
                                <label className="m-custom--label font-weight-bold mb-0" htmlFor="shineResume">Use shine resume</label>
                            </div>
                        </div>

                        <hr className="my-20" />

                        <div className="m-db-upload-resume">
                            <strong>Select services</strong> for which you want to use this resume
                        <ul className="m-db-upload-resume--list">
                                <li className="m-custom">
                                    <input type="checkbox" id="resumeBooster" />
                                    <label className="font-weight-bold" htmlFor="resumeBooster">Resume Booster 5-10 years</label>
                                </li>

                                <li className="m-custom">
                                    <input type="checkbox" id="resumeBuilder" />
                                    <label className="font-weight-bold" htmlFor="resumeBuilder">Resume Builder 5-10 yrs</label>
                                </li>

                                <li className="m-custom">
                                    <input type="checkbox" id="services" />
                                    <label className="font-weight-bold" htmlFor="services">For all services</label>
                                </li>
                            </ul>
                        </div>

                        <button className="btn btn-primary px-5 mt-30">Save</button>
                    </div>

                </div>
            </main>
        </div>
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