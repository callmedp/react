import React, { useState } from "react";
import { Link } from 'react-router-dom';
import { useDispatch, connect } from 'react-redux';
import { siteDomain } from 'utils/domains';
import ProductDetails from '../ProductDetails/productDetails';
import { MyGA } from 'utils/ga.tracking.js';
import { getTrackingInfo, getTrackingParameters } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';

const Product = (props) =>{
    const { product: {
        name, jobsAvailable,
        providerName, rating, mode,
        price, imgUrl, url,
        tags, about, skillList,
        highlights, type, level,
        brochure, duration, stars,
        u_courses_benefits, u_desc
    }, index, compType } = props

    const [showDetails, setShowDetails] = useState(false)
    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+' 
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    const tracking_data = getTrackingInfo();
    const dispatch = useDispatch();
    const { trackUser } = props;

    const handleTracking = () => {
        MyGA.SendEvent('SkillAllCourses', 'ln_course_click', 'ln_all_' + name, 'ln_' + name,'', false, true);
        trackUser({"query" :tracking_data, "action" :'exit_skill_page'});
    }

    return (
        <div className={compType === 'For You'?"m-card":"m-card-more"} key={index}>
            <div className="m-card__heading">
                {tags === 2 && <span className="m-flag-blue">NEW</span>}
                {tags === 1 && <span className="m-flag-red">BESTSELLER</span>}
                <figure>
                    <img src={imgUrl} alt={name} />
                </figure>
                <h3 className="m-heading3">
                    <a href={`${siteDomain}${url}`} onClick={handleTracking} >{name}</a>
                </h3>
            </div>
            <div className="m-card__box">
                <div className="m-card__rating">
                <span className="mr-10">By {providerName}</span>
                <span className="m-rating">
                    { stars?.map((star, index) => starRatings(star, index)) }
                    <span>{rating?.toFixed(1)}/5</span>
                </span>
                </div>
                <div className="m-card__duration-mode">
                    Duration: <strong>{duration} days</strong>  |   Mode: <strong>{mode}</strong>
                </div>
                <div className="m-card__price">
                    <strong>{price}/-</strong> 
                    {(compType === "More Courses") && !showDetails ? <span onClick={()=>setShowDetails(true)} className="m-view-more ml-auto" >View more</span>: null}
                </div>
            </div>
            {
                compType === 'For You' ?
                    <ProductDetails detailsData={{ about, skillList, highlights, jobsAvailable, url, type, level, brochure, u_courses_benefits, u_desc }} icon='file' setShowDetails={setShowDetails}/>
                    : null
            }
            {
                showDetails ? 
                    <ProductDetails detailsData={{ about, skillList, highlights, jobsAvailable, url, type, level, brochure, u_courses_benefits, u_desc }} icon='view less' setShowDetails={setShowDetails}/>
                    : null
            }
            
        </div>
    )
}

const mapDispatchToProps = (dispatch) => {
    return {
        "trackUser": (data) => {
            return dispatch(trackUser(data))
        }
    }
}

export default connect(null, mapDispatchToProps)(Product);
