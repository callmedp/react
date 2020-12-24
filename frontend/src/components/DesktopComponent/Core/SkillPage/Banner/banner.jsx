import React, { useEffect } from 'react';
import './banner.scss';
import Breadcrumb from 'react-bootstrap/Breadcrumb';
import Carousel from 'react-bootstrap/Carousel';
import { useDispatch, useSelector } from 'react-redux';

import { siteDomain, imageUrl } from 'utils/domains'; 


const BannerSkill = (props) => {
    

    const { name, breadcrumbs, featuresList } = useSelector( store => store.skillBanner )
    
    



    return (
       <header className="container-fluid pos-rel">
            <figure className="banner-img">
                <img src={`${imageUrl}desktop/skill-bg-new.png`} className="img-fluid" alt="Digital Marketing Courses & Certifications" alt="Digital Marketing Courses & Certifications" />
                <div className="banner-right">
                    <div className="banner-right-img">
                        <span className="skill-banner-tween1" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="100" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header1.svg`} />
                        </span>
                        <span className="skill-banner-tween2" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="300" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header2.svg`} />
                        </span>
                        <span className="skill-banner-tween3" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="500" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header3.svg`} />
                        </span>
                        <span className="skill-banner-tween4" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="700" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header4.svg`} />
                        </span>
                        <span className="skill-banner-tween5" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="900" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header5.svg`} />
                        </span>
                        <span className="skill-banner-tween6" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="1100" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header6.svg`} />
                        </span>
                        <span className="skill-banner-tween7" data-aos="zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay="1300" data-aos-duration="1000">
                            <img src={`${imageUrl}desktop/skill-animation-header7.svg`} />
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
                            return (<Breadcrumb.Item key={index} href={`${siteDomain}${bread.url}`} >{bread.name}</Breadcrumb.Item>)
                                else
                            return (<Breadcrumb.Item key={index} >{bread.name}</Breadcrumb.Item> )
                            })
                        }
                    </Breadcrumb>
                    <h1 className="heading1" data-aos="fade-right">
                        { name } Courses & Certifications
                    </h1>
                    <Carousel className="header-carousel">
                        {
                            featuresList?.map((feature, index) => {
                                return (
                                    <Carousel.Item key={index} >
                                        <p key={Math.random()}>
                                            <figure className="icon-round-arrow"></figure>
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

export default BannerSkill;