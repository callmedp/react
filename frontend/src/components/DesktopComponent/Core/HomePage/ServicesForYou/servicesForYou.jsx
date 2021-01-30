import React, {useState} from 'react';
import './servicesForYou.scss';
import { Link } from 'react-router-dom';

   
const OurVendors = (props) => {
    return(
        <aside id="services" className="container-fluid lightblue-bg" data-aos="fade-up">
            <div className="row">
                <div className="container mt-40 mb-0"> 
                    <div className="row d-block">
                        <h2 className="heading2 text-center mb-5">Job assistance services</h2>
                        <p className="mb-30 text-center">Find your next job faster by using our services.</p>
                        <div className="col-sm-12 d-flex">    
                            <div className="flex-1">
                                <div className="d-flex flex-wrap mb-40">
                                    <div className="col-sm-6">
                                        <div className="services-foryou">
                                            <h3 className="heading3">Resume Writing</h3>
                                            <p>Resume written by experts to increase your profile visibility</p>
                                            <span className="d-flex">
                                                <Link to={"#"}>Know more</Link>
                                                <figure className="icon-service1"></figure>
                                            </span>
                                        </div>
                                    </div>
                                    <div className="col-sm-6">
                                        <div className="services-foryou">
                                            <h3 className="heading3">Featured Profile</h3>
                                            <p>Appear on top when Recruiters search for best candidates</p>
                                            <span className="d-flex">
                                                <Link to={"#"}>Know more</Link>
                                                <figure className="icon-service2"></figure>
                                            </span>
                                        </div>
                                    </div>
                                    <div className="col-sm-6">
                                        <div className="services-foryou">
                                            <h3 className="heading3">Jobs on the Move</h3>
                                            <p>Get personalized job recommend -ations from all the job portals on your Whatsapp</p>
                                            <span className="d-flex">
                                                <Link to={"#"}>Know more</Link>
                                                <figure className="icon-service3"></figure>
                                            </span>
                                        </div>
                                    </div>
                                    <div className="col-sm-6">
                                        <div className="services-foryou">
                                            <h3 className="heading3">Application Highlighter</h3>
                                            <p>Get your Job Application noticed among others</p>
                                            <span className="d-flex">
                                                <Link to={"#"}>Know more</Link>
                                                <figure className="icon-service4"></figure>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="services-img">
                                <span className="services-tween1" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100">
                                    <img src="./media/images/services-tween1.svg" />
                                </span>
                                <span className="services-tween2" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="200">
                                    <img src="./media/images/services-tween2.svg" />
                                </span>
                                <span className="services-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300">
                                    <img src="./media/images/services-tween3.svg" />
                                </span>
                                <span className="services-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="400">
                                    <img src="./media/images/services-tween4.svg" />
                                </span>
                                <span className="services-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500">
                                    <img src="./media/images/services-tween5.svg" />
                                </span>
                                <span className="services-tween6" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="600">
                                    <img src="./media/images/services-tween6.svg" />
                                </span>
                                <span className="services-tween7" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700">
                                    <img src="./media/images/services-tween7.svg" />
                                </span>
                                <span className="services-tween8" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="800">
                                    <img src="./media/images/services-tween8.svg" />
                                </span>
                                <span className="services-tween9" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="900">
                                    <img src="./media/images/services-tween9.svg" />
                                </span>
                                <span className="services-tween10" data-aos="fade-up" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="1000" data-aos-anchor="#bounce">
                                    <img src="./media/images/services-tween10.svg" />
                                </span>
                                <span className="services-tween11" id="bounce" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="1100">
                                    <img src="./media/images/services-tween11.svg" />
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </aside>
    )
}
   
export default OurVendors;