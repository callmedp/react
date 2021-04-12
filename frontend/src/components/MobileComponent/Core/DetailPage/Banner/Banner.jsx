import React, { useState, useEffect } from 'react';
import {Link} from 'react-router-dom';
import './Banner.scss';
import { siteDomain } from 'utils/domains';

const CourseDetailBanner = (props) => {
    const { product_detail, prdId, varChecked } = props
    const noOfWords = 250;
    // const [showAll, setShowAll] = useState(false);
    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="micon-fullstar" key={index}></em> :
                star === '+' ? <em className="micon-halfstar" key={index}></em> :
                    <em className="micon-blankstar" key={index}></em>
        )
    }

    // const controlContent = (content, state) =>{
    //     return (
    //         <a href={"#"} onClick={() => setShowAll(state)}>
    //             {content}
    //         </a>
    //     )
    // }
    useEffect(() => {
        // setShowAll(false)
    }, [prdId])

    return (
        <div className="m-detail-header ml-15 mt-10" itemprop="Course" itemscope itemtype="https://schema.org/Course">

            <div className="m-detail-heading">
                <div className="m-detail-heading__icon mt-30" itemprop="image">
                    <figure>
                        <img src={ product_detail?.prd_img } alt={ product_detail?.prd_img_alt } />
                    </figure>
                </div>
                <div className="m-detail-heading__content" itemprop="name">
                    { product_detail?.pTg && <span className="m-flag-yellowB">{ product_detail.pTg }</span> }
                    <h1 className="m-heading1 mt-5">
                        { product_detail?.prd_H1 }
                    </h1>
                    <span className="m-rating">
                        {
                            product_detail?.prd_rating_star?.map((star, index) => starRatings(star, index))
                        }
                        <span itemprop="ratingValue">{ product_detail?.prd_rating?.toFixed() }/5</span>
                        <span>By <span itemprop="provider">{ product_detail?.prd_vendor }</span></span>
                    </span>
                    <div className="d-flex mt-10">
                        {
                            product_detail?.prd_num_rating && 
                                <span className="m-review-jobs">
                                    <Link to={"#"}>
                                        <figure className="micon-reviews-link"></figure> <strong>{ product_detail?.prd_num_rating }</strong> Reviews
                                    </Link>
                                </span>
                        }

                        {
                            product_detail?.prd_num_jobs &&
                                <span className="m-review-jobs">
                                    <Link to={"#"}>
                                        <figure className="micon-jobs-link"></figure> <strong>{ product_detail?.prd_num_jobs }</strong> Jobs available
                                    </Link>
                                </span>

                        }
                        
                    </div>
                    <ul className="m-course-stats mt-20 mb-20">
                        <li className="d-flex align-items-center">
                            <figure className="icon-course-duration mr-10"></figure>
                            <p>
                                Course Duration <strong>{varChecked?.dur_days || product_detail?.selected_var?.dur_days || '--'} Days</strong>
                            </p>
                        </li>
                        <li className="d-flex align-items-center">
                            <figure className="icon-access-duration mr-10"></figure>
                            <p>
                                Access Duration <strong>{product_detail?.access_duration}</strong>
                            </p>
                        </li>
                    </ul>
                </div>
            </div>
            <ul className="m-course-stats mb-10 bdr-top pt-10">
                <li>
                    Type: <strong className="d-inline">Trial</strong>
                </li>
                <li>
                    Level: <strong className="d-inline">Intermediate</strong>
                </li>
                <li>
                    Certification: <strong className="d-inline">Yes</strong>
                </li>
            </ul>
            <div className="m-intro-video" itemprop="embedUrl">
                <strong className="mb-10">Course intro</strong>
                <div className="d-flex">
                    {
                        product_detail?.prd_video && 
                            <figure className="m-intro-video__img">
                                <a href={`https://${product_detail?.prd_video}`} target="_blank">
                                    <img src={product_detail?.prd_vendor_img} alt="Intro Video" />
                                    <i className="micon-play-video"></i>
                                </a>
                            </figure>
                    }

                    {
                        product_detail?.prd_about && 
                        <>
                            <p itemprop="description" className="m-intro-video__content" dangerouslySetInnerHTML={{__html: product_detail?.prd_about?.replace(/<[^>]*>/g, '').slice(0, noOfWords) + "<a href='#'> ...Read More</a>" }} />
                            {/* <span>
                                {
                                    (!showAll && product_detail?.prd_about?.length > noOfWords) ? 
                                            controlContent(" ...Read More", true) : ("") 
                                } 
                            </span> */}
                        </>
                    }

                    {/* {
                        showAll ?
                        <p className="m-intro-video__content" dangerouslySetInnerHTML={{__html: product_detail?.prd_about?.replace(/<[^>]*>/g, '').slice(noOfWords)}} /> : null
                    } */}
                </div>
            </div>
            {
                product_detail?.prd_service === 'course' &&
                    <ul className="m-course-stats mt-10 mb-10 bdr-top pt-20">
                        <li>
                            <a href={`${siteDomain}/search/results/?fvid=${product_detail?.pPv}`}>View all</a> courses by {product_detail?.prd_vendor}
                        </li>
                        <li>
                        <a href={`${siteDomain}/search/results/?fvid=${product_detail?.pPv}`}>+{product_detail?.prd_vendor_count} more</a> Course providers  
                        </li>
                    </ul>
            }
        </div>
    )
}

export default CourseDetailBanner;