import React, { useState } from "react";
import { Link } from 'react-router-dom';
import { siteDomain } from 'utils/domains';
import ProductDetails from '../ProductDetails/productDetails';

const Product = (props) =>{
    const { product: {
        name, jobsAvailable,
        providerName, rating, mode,
        price, imgUrl, url,
        tags, about, skillList,
        highlights, type, level,
        brochure, duration, stars
    }, index, compType } = props

    const [showDetails, setShowDetails] = useState(false)
    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+' 
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
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
                    <a href={`${siteDomain}${url}`}>{name}</a>
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
                    <ProductDetails detailsData={{ about, skillList, highlights, jobsAvailable, url, type, level, brochure }} icon='file' setShowDetails={setShowDetails}/>
                    : null
            }
            {
                showDetails ? 
                    <ProductDetails detailsData={{ about, skillList, highlights, jobsAvailable, url, type, level, brochure }} icon='view less' setShowDetails={setShowDetails}/>
                    : null
            }
            
        </div>
    )
}

export default Product;