import React, { useState, useEffect } from 'react';
import {Link} from 'react-router-dom';
import './Banner.scss';
import { siteDomain } from 'utils/domains';

const CourseDetailBanner = (props) => {
    const { product_detail, prdId } = props
    const noOfWords = 250;
    const [showAll, setShowAll] = useState(false)

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
        <div className="m-detail-header ml-15 mt-10">

            <div className="m-detail-heading">
                <div className="m-detail-heading__icon mt-30">
                    <figure>
                        <img src={ product_detail?.prd_img } alt={ product_detail?.prd_img_alt } />
                    </figure>
                </div>
                <div className="m-detail-heading__content">
                    { product_detail?.pTg && <span className="m-flag-yellowB">{ product_detail.pTg }</span> }
                    <h1 className="m-heading1 mt-5">
                        { product_detail?.prd_H1 }
                    </h1>
                    <span className="m-rating">
                    {
                        product_detail?.prd_rating_star?.map((star, index) => starRatings(star, index))
                    }
                        {/* <em className="micon-fullstar"></em>
                        <em className="micon-fullstar"></em>
                        <em className="micon-fullstar"></em>
                        <em className="micon-halfstar"></em>
                        <em className="micon-blankstar"></em> */}
                        <span>{ product_detail?.prd_rating?.toFixed() }/5</span>
                        <span>By { product_detail?.prd_vendor }</span>
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
                </div>
            </div>
            <div className="m-intro-video">
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
                        <p className="m-intro-video__content" dangerouslySetInnerHTML={{__html: product_detail?.prd_about?.replace(/<[^>]*>/g, '').slice(0, noOfWords) + "<a href='#'> ...Read More</a>" }} />
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
            <ul className="m-course-stats mt-10 mb-10 bdr-top pt-20">
                <li>
                    <a href={`${siteDomain}/search/results/?fvid=${product_detail?.pPv}`}>View all</a> courses by {product_detail?.prd_vendor}
                </li>
                <li>
                <Link to={"#"}>+3 more</Link> Course providers  
                </li>
            </ul>
        </div>
    )
}

export default CourseDetailBanner;