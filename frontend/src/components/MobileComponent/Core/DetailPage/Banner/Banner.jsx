import React, { useState, useEffect } from 'react';
import {Link} from 'react-router-dom';
import './Banner.scss';
import { siteDomain } from 'utils/domains';
import { Link as LinkScroll } from "react-scroll";
import { getStudyMode } from 'utils/detailPageUtils/studyMode';
import { getStudyLevel } from 'utils/detailPageUtils/studyLevel';

const CourseDetailBanner = (props) => {
    const { 
        product_detail,
        prdId,
        varChecked,
        showReviewModal 
    } = props

    const noOfWords = 250;
    const [showAll, setShowAll] = useState(false);
    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="micon-fullstar" key={index}></em> :
                star === '+' ? <em className="micon-halfstar" key={index}></em> :
                    <em className="micon-blankstar" key={index}></em>
        )
    }

    const controlContent = (content, state) =>{
        return (
            <a href={"#"} onClick={(e) => {e.preventDefault(); setShowAll(state)}}>
                {content}
            </a>
        )
    }

    useEffect(() => {
        setShowAll(false)
    }, [prdId])

    return (
        <div className="m-detail-header ml-15 mt-10" itemProp="Course" itemScope itemType="https://schema.org/Course">

            <div className="m-detail-heading">
                <div className="m-detail-heading__icon mt-30" itemProp="image">
                    <figure>
                        <img src={ product_detail?.prd_img } alt={ product_detail?.prd_img_alt } />
                    </figure>
                </div>
                <div className="m-detail-heading__content" itemProp="name">
                    { product_detail?.pTg && product_detail.pTg !== 'None' && <span className="m-flag-yellowB">{ product_detail.pTg }</span> }
                    <h1 className="m-heading1 mt-5">
                        { product_detail?.prd_H1 }
                    </h1>
                    <span className="m-rating">
                        {
                            product_detail?.prd_num_rating ? 
                                <>
                                    {
                                        product_detail?.prd_rating_star?.map((star, index) => starRatings(star, index))
                                    }
                                    <span itemProp="ratingValue">{ product_detail?.prd_rating?.toFixed() }/5</span>
                                </>
                                :
                                ''
                        }
                        <span>By <span itemProp="provider">{ product_detail?.prd_vendor }</span></span>
                    </span>
                    <div className="d-flex mt-10">
                        {
                            product_detail?.prd_num_rating > 0 ?
                                <span className="m-review-jobs">
                                    <LinkScroll to="review" offset={-120}>
                                        <Link to={"#"}>
                                            <figure className="micon-reviews-link"></figure> <strong>{ product_detail?.prd_num_rating }</strong> Reviews
                                        </Link>
                                    </LinkScroll>
                                </span>
                                :
                                <span className="m-review-jobs">
                                    <Link to={"#"} onClick={ () => showReviewModal(true) }>
                                        <figure className="micon-reviews-link"></figure> Write a Review
                                    </Link>
                                </span>
                        }

                        {
                            product_detail?.prd_num_jobs > 0 &&
                                <span className="m-review-jobs">
                                    <a href={product_detail?.num_jobs_url}>
                                        <figure className="micon-jobs-link"></figure> <strong>{ product_detail?.prd_num_jobs }</strong> Jobs available
                                    </a>
                                </span>

                        }
                        
                    </div>
                    <ul className="m-course-stats mt-20 mb-20">
                        {
                            (varChecked?.dur_days || product_detail?.selected_var?.dur_days) && 
                                <li className="d-flex align-items-center">
                                    <figure className="micon-course-duration mr-10"></figure>
                                    <p>
                                        Course Duration <strong>{ varChecked?.dur_days || product_detail?.selected_var?.dur_days } Days</strong>
                                    </p>
                                </li>
                        }

                        {
                            product_detail?.access_duration && 
                                <li className="d-flex align-items-center">
                                    <figure className="micon-access-duration mr-10"></figure>
                                    <p>
                                        Access Duration <strong>{product_detail?.access_duration}</strong>
                                    </p>
                                </li>
                        }
                        
                    </ul>

                    <ul className="m-course-stats mt-20 mb-20">
                        {
                            product_detail?.prd_asft &&
                            <>
                                <li className="d-flex align-items-center">
                                    <figure className="micon-course-duration mr-10"></figure>
                                    <p>
                                        Test Duration <strong>{product_detail?.prd_asft?.test_duration}</strong>
                                    </p>
                                </li>
                                <li className="d-flex align-items-center">
                                    <figure className="micon-question-no mr-10"></figure>
                                    <p>
                                    No. of questions <strong>{product_detail?.prd_asft?.number_of_questions}</strong>
                                    </p>
                                </li>
                            </>
                        }
                    </ul>
                </div>
            </div>

            {
                (product_detail?.selected_var?.type || product_detail?.selected_var?.level) &&
                    <ul className="m-course-stats mb-10 bdr-top pt-10">
                        {
                            <li>
                                Type: <strong className="d-inline">{getStudyMode(varChecked?.type || product_detail?.selected_var?.type)}</strong>
                            </li>
                        }
                        
                        {
                            <li>
                                Level: <strong className="d-inline">{getStudyLevel(varChecked?.level || product_detail?.selected_var?.level)}</strong>
                            </li>
                        }

                        <li>
                            Certification: <strong className="d-inline">{(varChecked?.certify || product_detail?.selected_var?.certify) === 0 ? 'No' : (varChecked?.certify || product_detail?.selected_var?.certify) === false ? 'No' : 'Yes' }</strong>
                        </li>
                        
                    </ul>
            }

            <div className="m-intro-video" itemProp="embedUrl">
                <strong className="mb-10">Course intro</strong>
                <div className="d-flex">
                    {
                        product_detail?.prd_video && 
                            <figure className="m-intro-video__img">
                                <a href={`https://${product_detail?.prd_video}`} target="_blank">
                                    <iframe src={`https://${product_detail?.prd_video}`} frameBorder="0" />
                                    <i className="micon-play-video"></i>
                                </a>
                            </figure>
                    }

                    {
                        product_detail?.prd_about && 
                        <p className="m-intro-video__content">
                            <span itemProp="description" dangerouslySetInnerHTML={{__html: product_detail?.prd_about?.replace(/<[^>]*>/g, '').slice(0, showAll ? product_detail?.prd_about?.length : noOfWords) }} />
                            <span>
                                {
                                    (!showAll && product_detail?.prd_about?.length > noOfWords) ? 
                                            controlContent(" ... Read More", true) : controlContent(" ... Show less", false)
                                } 
                            </span>
                        </p>
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