import React from 'react';
import './servicesForYou.scss';
import { useSelector } from 'react-redux';
import { imageUrl, siteDomain } from 'utils/domains';

const JobAssistanceServices = (props) => {

    const { jobAssistanceServices } = useSelector(store => store.jobAssistance)

    return (
        <aside id="services" className="container-fluid lightblue-bg" data-aos="fade-up">
            <div className="row">
                <div className="container mt-40 mb-0">
                    <div className="row d-block">
                        <h2 className="heading2 text-center mb-5">Job assistance services</h2>
                        <p className="mb-30 text-center">Find your next job faster by using our services.</p>
                        <div className="col-sm-12 d-flex">
                            <div className="flex-1">
                                <div className="d-flex flex-wrap mb-40">
                                    {
                                        jobAssistanceServices?.map((service, index) => {
                                            return (
                                                <div className="col-sm-6" key={service.id}>
                                                    <div className="services-foryou">
                                                        <h3 className="heading3">{service.heading}</h3>
                                                        <p>{ service.description.length > 100 ? service.description.slice(0,100)+"..." : service.description }</p>
                                                        <span className="d-flex">
                                                            <a href={`${siteDomain}${service.url}`}>Know more</a>
                                                            {/* <figure className="icon-service1"></figure> */}
                                                            <figure >
                                                                <img src={service.img} className="img-fluid" alt={service.img_alt} />
                                                            </figure>
                                                        </span>
                                                    </div>
                                                </div>
                                            )
                                        })
                                    }
                                </div>
                            </div>
                            <div className="services-img">
                                <span className="services-tween1" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100">
                                    <img src={`${imageUrl}desktop/services-tween1.svg`} />
                                </span>
                                <span className="services-tween2" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="200">
                                    <img src={`${imageUrl}desktop/services-tween2.svg`} />
                                </span>
                                <span className="services-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300">
                                    <img src={`${imageUrl}desktop/services-tween3.svg`} />
                                </span>
                                <span className="services-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="400">
                                    <img src={`${imageUrl}desktop/services-tween4.svg`} />
                                </span>
                                <span className="services-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500">
                                    <img src={`${imageUrl}desktop/services-tween5.svg`} />
                                </span>
                                <span className="services-tween6" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="600">
                                    <img src={`${imageUrl}desktop/services-tween6.svg`} />
                                </span>
                                <span className="services-tween7" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700">
                                    <img src={`${imageUrl}desktop/services-tween7.svg`} />
                                </span>
                                <span className="services-tween8" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="800">
                                    <img src={`${imageUrl}desktop/services-tween8.svg`} />
                                </span>
                                <span className="services-tween9" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="900">
                                    <img src={`${imageUrl}desktop/services-tween9.svg`} />
                                </span>
                                <span className="services-tween10" data-aos="fade-up" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="1000" data-aos-anchor="#bounce">
                                    <img src={`${imageUrl}desktop/services-tween10.svg`} />
                                </span>
                                <span className="services-tween11" id="bounce" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="1100">
                                    <img src={`${imageUrl}desktop/services-tween11.svg`} />
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </aside>
    )
}

export default JobAssistanceServices;