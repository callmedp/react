import React, { useRef, useEffect } from 'react';
import './banner.scss';
import Breadcrumb from 'react-bootstrap/Breadcrumb';
// import {Link} from 'react-router-dom';
import { Link as LinkScroll } from 'react-scroll';

const BannerCourseDetail = (props) => {
    const {product_detail} = props;
    const reqLength = 365;
    const inputCheckbox = useRef(null);
    const regex = /<(.|\n)*?>/g;

    // console.log(props);

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+' 
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    useEffect(() => {
        inputCheckbox.current && (inputCheckbox.current.checked = false)
    })

    const changeMode = (e) => {
        console.log(e);
    }

    return (
       <header className="container-fluid pos-rel course-detail-bg">
            <div className="row">
                <div className="container detail-header-content">
                    <div className="flex-1">
                        <Breadcrumb>
                            {
                                product_detail?.breadcrumbs?.map((bread, inx) => {
                                    return <Breadcrumb.Item key={inx} href={bread.url}>{bread.name}</Breadcrumb.Item>
                                })
                            }
                            {/* <Breadcrumb.Item href="#">Home</Breadcrumb.Item>
                            <Breadcrumb.Item href="#">
                                Sales and Marketing
                            </Breadcrumb.Item>
                            <Breadcrumb.Item active>Digital Marketing</Breadcrumb.Item> */}
                        </Breadcrumb>
                        <div className="detail-heading" data-aos="fade-right">
                            <div className="detail-heading__icon">
                                <figure>
                                    <img src={product_detail?.prd_img} alt={product_detail?.prd_img_alt} />
                                </figure>
                            </div>
                            <div className="detail-heading__content">
                                { product_detail?.pTg && <span className="flag-yellowB">{product_detail?.pTg}</span> }
                                <h1 className="heading1">
                                    {product_detail?.prd_H1}
                                </h1>
                                <div className="d-flex mt-15">
                                    <span className="rating">
                                        {
                                            product_detail?.prd_rating_star?.map((star, index) => starRatings(star, index))
                                        }
                                        <span>{product_detail?.prd_rating?.toFixed()}/5</span>
                                    </span>
                                    {
                                        <>
                                        {product_detail?.prd_num_rating && <span className="review-jobs">
                                        <LinkScroll to={"#"}>
                                            <figure className="icon-reviews-link"></figure> <strong> {product_detail?.prd_num_rating}</strong> Reviews
                                        </LinkScroll>
                                        </span>}
                                        {product_detail?.prd_num_jobs && <span className="review-jobs">
                                            <LinkScroll to={"#"}>
                                                <figure className="icon-jobs-link"></figure> <strong>{product_detail?.prd_num_jobs}</strong> Jobs available
                                            </LinkScroll>
                                        </span>}
                                        </>
                                    }
                                </div>
                            </div>
                        </div>
                        <ul className="course-stats mt-30 mb-30">
                            <li>
                                <strong>By {product_detail?.prd_vendor}</strong> <LinkScroll to={"#"}>View all</LinkScroll> courses by {product_detail?.prd_vendor}  
                            </li>
                            <li>
                            <LinkScroll className="d-block" to={"popListTemplate"}>+{product_detail?.pop_list?.length} more</LinkScroll> Course providers  
                            </li>
                            <li className="d-flex align-items-center">
                                <figure className="icon-course-duration mr-10"></figure>
                                <p>
                                    Course Duration <strong>{product_detail?.duration} Days</strong>
                                </p>
                            </li>
                            <li className="d-flex align-items-center">
                                <figure className="icon-access-duration mr-10"></figure>
                                <p>
                                    Access Duration <strong>{product_detail?.access_duration}</strong>
                                </p>
                            </li>
                        </ul>
                        <div className="intro-video">
                            <figure className="intro-video__img">
                                <a target="_blank" href={product_detail?.prd_video}>
                                    <img src={product_detail?.prd_vendor_img} alt="Intro Video" />
                                    <i className="icon-play-video"></i>
                                    <strong>Intro video</strong>
                                </a>
                            </figure>

                            <p className="intro-video__content">
                                { product_detail?.prd_about ? <div id="module" className="row about-course">
                                    {product_detail?.prd_about.replace(regex, '')?.length > reqLength ? (
                                        <input type="checkbox" className="read-more-state" id="post-10" ref={inputCheckbox} itemProp="about" />
                                        ) : (
                                            ""
                                            )}
                                            
                                    <p className="read-more-wrap">
                                        <span dangerouslySetInnerHTML={{__html:product_detail?.prd_about?.replace(regex, '').slice(0, reqLength)}} />
                                        <span className="read-more-target" dangerouslySetInnerHTML={{__html: product_detail?.prd_about?.replace(regex, '').slice(reqLength)}} />
                                    </p>
                                    <label htmlFor="post-10" className="read-more-trigger"></label>
                                </div> : "" }
                            </p>
                        </div>
                    </div>
                    <div className="banner-detail">
                        <div className="course-enrol">
                            <div className="course-enrol__mode">
                                <form>
                                    Mode 
                                    {
                                        product_detail?.var_list?.map((varList, indx) => {
                                            return (
                                            <label key={indx} for={varList.mode+varList.id}>
                                                <input type="radio" name="mode" id={varList.mode+varList.id} checked={product_detail?.selected_var?.id === varList.id} onClick={(event) => changeMode(event)} />
                                                {varList.mode === 'OL' ? 'Online' : varList.mode === 'CA' ? 'Class room' : 'Other'}
                                            </label> 
                                            )
                                        })
                                    }
                                </form>
                            </div>
                            <div className="course-enrol__price">
                                <strong className="mt-20 mb-10">{product_detail?.selected_var?.inr_price}/- <del>{product_detail?.start_price}/-</del></strong>
                                <LinkScroll to={"#"} className="btn btn-secondary mt-10">Enroll now</LinkScroll>
                                <LinkScroll to={"#"} className="btn btn-outline-primary mt-10">Enquire now</LinkScroll>
                            </div>
                            <div className="course-enrol__offer lightblue-bg2">
                                <strong className="mt-10 mb-5">Offers</strong>
                                <ul className="pb-0">
                                    <li><figure className="icon-offer-pay"></figure> Buy now & <strong>pay within 14 days using ePayLater</strong> </li>
                                    <li><figure className="icon-offer-test"></figure> Take <strong>free practice test</strong> to enhance your skill</li>
                                    <li><figure className="icon-offer-badge"></figure> <strong>Get badging</strong> on your Shine profile</li>
                                    <li><figure className="icon-offer-global"></figure> <strong>Global</strong> Education providers</li>
                                </ul>
                                <LinkScroll to={"#"}>+2 more</LinkScroll>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
       </header> 
    )
}

export default BannerCourseDetail;