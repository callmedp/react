import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import './Banner.scss';
import { siteDomain } from 'utils/domains';
import { Link as LinkScroll } from "react-scroll";
import { getStudyMode } from 'utils/detailPageUtils/studyMode';
import { getStudyLevel } from 'utils/detailPageUtils/studyLevel';
import { MyGA } from 'utils/ga.tracking.js';
import { getTrackingInfo, getCandidateId } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import { useDispatch } from 'react-redux';

const CourseDetailBanner = (props) => {
    const {
        product_detail,
        prdId,
        varChecked,
        showReviewModal,
        providerCount,
        pUrl,
        prd_review_list,
        completeDescription,
        noOfWords,
        setVideoModal,
    } = props;

    const dispatch = useDispatch();
    const [showAll, setShowAll] = useState(false);

    // chatbot course details
    window["course_duration"] = product_detail?.selected_var?.learning_duration ? (varChecked?.learning_duration || product_detail?.selected_var?.learning_duration) : (varChecked?.dur_days || product_detail?.selected_var?.dur_days);

    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="micon-fullstar" key={index}></em> :
                star === '+' ? <em className="micon-halfstar" key={index}></em> :
                    <em className="micon-blankstar" key={index}></em>
        )
    }

    const controlContent = (content, state) => {
        return (
            <a href={"#"} onClick={(e) => { e.preventDefault(); setShowAll(state) }}>
                {content}
            </a>
        )
    }

    const getVideoId = (link) => {
        try{
            return new URL("https://"+link).searchParams.get('v');
        }catch{
            return ''
        }
    }

    useEffect(() => {
        setShowAll(false)
    }, [prdId])

    const trackJobs = () => {
        let tracking_data = getTrackingInfo();

        dispatch(trackUser({ "query": tracking_data, "action": 'jobs_available' }));
        dispatch(trackUser({ "query": tracking_data, "action": 'exit_product_page' }));
        MyGA.SendEvent('ln_course_details', 'ln_course_details', 'ln_jobs_available', 'Jobs available', '', '', true);
    }

    const viewAllCourses = () => {
        let tracking_data = getTrackingInfo();

        MyGA.SendEvent('Search', `${product_detail?.prd_vendor}`, 'ViewAllProductVendor');
        dispatch(trackUser({ "query": tracking_data, "action": 'all_courses_or_certifications' }));
        dispatch(trackUser({ "query": tracking_data, "action": 'exit_product_page' }));
    }

    const handleVideoModal = (eve) => {
        eve.preventDefault();
        console.log("video modal set")
        setVideoModal(true);
    }

    return (
        <div className="m-detail-header ml-15 mt-10 of-vis">

            <div className="m-detail-heading">
                <div className="m-detail-heading__icon mt-30">
                    <figure>
                        <img itemProp="image" src={product_detail?.prd_img} alt={product_detail?.prd_img_alt} />
                    </figure>
                </div>
                <div className="m-detail-heading__content" itemProp="aggregateRating" itemScope itemType="https://schema.org/AggregateRating">
                    {product_detail?.pTg && product_detail.pTg !== 'None' && <span className="m-flag-yellowB">{product_detail.pTg}</span>}
                    <h1 className="m-heading1 mt-5" itemProp="name">
                        {product_detail?.prd_H1}
                    </h1>
                    <span className="m-rating">
                        {
                            product_detail?.prd_num_rating ?
                                <span>
                                    {
                                        product_detail?.prd_rating_star?.map((star, index) => starRatings(star, index))
                                    }
                                    <span itemProp="ratingValue">{product_detail?.prd_rating?.toFixed()}/5</span>
                                </span>
                                :
                                ''
                        }
                        <span>By <span onClick={() => MyGA.SendEvent('ln_course_provider', 'ln_course_provider', 'ln_click_course_provider', `${product_detail?.prd_vendor}`, '', false, true)}>{product_detail?.prd_vendor}</span></span>
                    </span>
                    <div className="d-flex mt-10">
                        {
                            (product_detail?.prd_num_rating > 0 && prd_review_list && prd_review_list?.length) ?
                                <span className="m-review-jobs">
                                    <LinkScroll to="reviews" offset={-120}>
                                        <Link to={"#"}>
                                            <figure className="micon-reviews-link"></figure> <strong itemProp="reviewCount" content={product_detail?.prd_num_rating}>{product_detail?.prd_num_rating}</strong> {product_detail?.prd_num_rating > 1 ? 'Reviews' : 'Review'}
                                        </Link>
                                    </LinkScroll>
                                </span>
                                :
                                getCandidateId() ?
                                    <span className="m-review-jobs" itemProp="reviewCount" content="1">
                                        <Link to={"#"} onClick={() => showReviewModal(true)}>
                                            <figure className="micon-reviews-link"></figure> Write a Review
                                        </Link>
                                    </span>
                                    :
                                    <span className="m-review-jobs" itemProp="reviewCount" content="1">
                                        <a href={`${siteDomain}/login/?next=${pUrl}?sm=true`}>
                                            <figure className="micon-reviews-link"></figure> Write a Review
                                        </a>
                                    </span>

                        }

                        {
                            product_detail?.prd_num_jobs > 0 &&
                            <span className="m-review-jobs">
                                <a href={product_detail?.num_jobs_url} onClick={() => trackJobs()}>
                                    <figure className="micon-jobs-link"></figure> <strong>{product_detail?.prd_num_jobs}</strong> Jobs available
                                    </a>
                            </span>

                        }

                    </div>
                    <ul className="m-course-stats mt-20 mb-20">
                        {
                            (varChecked?.dur_days || product_detail?.selected_var?.dur_days) ?
                                <li className="d-flex align-items-center">
                                    <figure className="micon-course-duration mr-10"></figure>
                                    <p>
                                        Course Duration <strong>{varChecked?.dur_days || product_detail?.selected_var?.dur_days} Days</strong>
                                    </p>
                                </li> : ''
                        }

                        {
                            product_detail?.access_duration &&
                            <li className="d-flex align-items-center nobdr">
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
                                {
                                    product_detail?.prd_asft?.test_duration ?
                                        <li className="d-flex align-items-center">
                                            <figure className="micon-course-duration mr-10"></figure>
                                            <p>
                                                Test Duration <strong>{product_detail?.prd_asft?.test_duration}</strong>
                                            </p>
                                        </li> : ''
                                }

                                {
                                    product_detail?.prd_asft?.number_of_questions ?
                                        <li className="d-flex align-items-center">
                                            <figure className="micon-question-no mr-10"></figure>
                                            <p>
                                                No. of questions <strong>{product_detail?.prd_asft?.number_of_questions}</strong>
                                            </p>
                                        </li> : ''
                                }
                            </>
                        }
                    </ul>
                </div>

                {/* brand meta tag */}
                <span itemProp="brand" itemType="http://schema.org/Brand" itemScope>
                    <span itemProp="name" content={product_detail?.prd_vendor}></span>
                </span>
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
                        Certification: <strong className="d-inline">{(varChecked?.certify || product_detail?.selected_var?.certify) === 0 ? 'No' : (varChecked?.certify || product_detail?.selected_var?.certify) === false ? 'No' : 'Yes'}</strong>
                    </li>

                </ul>
            }

            {
                (product_detail?.prd_video || completeDescription) &&
                <div className="m-intro-video">
                    <strong className="mb-10">Course intro</strong>
                    <div className="d-flex">
                        {
                            product_detail?.prd_video &&
                            <figure className="m-intro-video__img">
                                <a onClick={handleVideoModal}>
                                    <iframe src={`https://www.youtube.com/embed/${getVideoId(product_detail?.prd_video)}`} frameBorder="0" />
                                    <i className="micon-play-video"></i>
                                </a>
                            </figure>
                        }

                        {
                            completeDescription &&
                            <p className="m-intro-video__content">
                                <span itemProp="description" content={product_detail?.prd_about} dangerouslySetInnerHTML={{ __html: product_detail?.prd_about?.slice(0, showAll ? product_detail?.prd_about?.length : noOfWords) }} />
                                <span>
                                    {
                                        (!showAll && product_detail?.prd_about?.length > noOfWords) ?
                                            controlContent(" ... Read More", true) : showAll ? controlContent(" Show less", false) : ''
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
            }

            {
                product_detail?.prd_service === 'course' &&
                <ul className="m-course-stats mt-10 mb-10 bdr-top pt-20">
                    <li>
                        <a href={`${siteDomain}/search/results/?fvid=${product_detail?.pPv}`} onClick={() => viewAllCourses()}>View all</a> courses by {product_detail?.prd_vendor}
                    </li>
                    {
                        providerCount > 0 ?
                            <li>
                                <LinkScroll to={'otherProviders'} offset={-150} >+{providerCount} more</LinkScroll> Course providers
                                </li> : ''
                    }
                </ul>
            }
        </div>
    )
}

export default CourseDetailBanner;