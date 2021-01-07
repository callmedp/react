import React, { useEffect } from 'react';
import './banner.scss';
import Breadcrumb from 'react-bootstrap/Breadcrumb';
import Carousel from 'react-bootstrap/Carousel';
import { useDispatch, useSelector, connect } from 'react-redux';

import { siteDomain, imageUrl } from 'utils/domains'; 
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';


const BannerSkill = (props) => {
    
    const { name, breadcrumbs, featuresList } = useSelector( store => store.skillBanner );
    const { userTrack } = props;
    const tracking_data = getTrackingInfo();
    const dispatch = useDispatch();
    
    return (
       <header className="container-fluid pos-rel">
            <figure className="banner-img">
                <img src={`${imageUrl}desktop/skill-bg-new.png`} className="img-fluid" alt={`${ name } Courses & Certifications`} />
                <div className="banner-right">
                    <div className="banner-right-img">
                        <span className="skill-banner-tween1" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header1.svg`} alt={`${ name } Courses Banner`}/>
                        </span>
                        <span className="skill-banner-tween2" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header2.svg`} alt={`${ name } Courses Banner`}/>
                        </span>
                        <span className="skill-banner-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header3.svg`} alt={`${ name } Courses Banner`}/>
                        </span>
                        <span className="skill-banner-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header4.svg`} alt={`${ name } Courses Banner`}/>
                        </span>
                        <span className="skill-banner-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="900" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header5.svg`} alt={`${ name } Courses Banner`}/>
                        </span>
                        <span className="skill-banner-tween6" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="1100" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header6.svg`} alt={`${ name } Courses Banner`}/>
                        </span>
                        <span className="skill-banner-tween7" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="1300" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header7.svg`} alt={`${ name } Courses Banner`}/>
                        </span>
                    </div>
                </div>
            </figure>
            <div className="container header-content">
                <div className="row">
                    <Breadcrumb>
                        {
                            breadcrumbs?.map((bread, index) => {
                                if(!!bread.url)
                            return (<Breadcrumb.Item key={index} href={`${siteDomain}${bread.url}`} onClick={ () => userTrack({"query" : tracking_data,"action": "exit_skill_page"})} >{bread.name}</Breadcrumb.Item>)
                                else
                            return (<Breadcrumb.Item key={index} >{bread.name}</Breadcrumb.Item> )
                            })
                        }
                    </Breadcrumb>
                    <h1 className="heading1" data-aos="fade-right">
                        { name } Courses & Certifications
                    </h1>
                    <Carousel className={ featuresList?.length ? "header-carousel" : "header-carousel noslide" }>
                        {/* <figure className="icon-round-arrow"></figure> */}
                        {
                            featuresList?.map((feature, index) => {
                                return (
                                    <Carousel.Item key={index} >
                                        <p key={Math.random()}>
                                            <span className="flex-1">{ feature }</span>
                                        </p>
                                    </Carousel.Item>
                                )
                            })
                        }
                    </Carousel>
                </div>
            </div>
       </header> 
    )
}

const mapDispatchToProps = (dispatch) => {
    return {
        "userTrack": (data) => {
            dispatch(trackUser(data))
        }
    }
}

export default connect(null, mapDispatchToProps)(BannerSkill);