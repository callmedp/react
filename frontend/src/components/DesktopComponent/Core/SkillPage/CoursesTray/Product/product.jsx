import React, { useEffect, useState } from 'react';
import { siteDomain } from 'utils/domains';
import CustomOverlay from 'services/CustomOverlay';
import PopoverDetail from '../PopOverDetail/popOverDetail'


const Product = (props) => {

    const { product: {
        name, jobsAvailable,
        providerName, rating, mode,
        price, imgUrl, url,
        tags, about, skillList,
        highlights, type, level,
        brochure, duration
    },
        index,
        listIdx } = props

    const [halfStar, setHalfStar] = useState(false)

    useEffect(() => {
        if (!Number.isInteger(rating)) {
            setHalfStar(true)
        }
        else {
            setHalfStar(false)
        }
    }, [rating])

    return (

        <CustomOverlay
            component={<PopoverDetail popoverData={{ about, skillList, highlights, jobsAvailable, url, type, level }} />}
            placement={ listIdx === 2  ? 'left' : 'right'}
            onMouseEnter={() => { }}
            delay={200}
        >
            <li className="col-sm-4" key={index}>
                <div className="card" data-aos="fade-zoom-in" data-aos-easing="ease-in-back" data-aos-offset="0" data-aos-delay={index*50+50} data-aos-duration="1000">
                    <div className="card__heading">
                        {tags === 2 && <span className="flag-blue">NEW</span>}
                        {tags === 1 && <span className="flag-red">BESTSELLER</span>}
                        <figure>
                            <img src={imgUrl} alt={name} />
                        </figure>
                        <h3 className="heading3">
                            <a href={`${siteDomain}${url}`} >{name}</a>
                        </h3>
                    </div>
                    <div className="card__box">
                        <div className="card__rating mt-5">
                            <span className="provider mr-10">By {providerName}</span>
                            <span className="rating">

                                {Array(parseInt(rating)).fill().map((_, index) => <em key={index} className="icon-fullstar"></em>)}
                                {halfStar && <em className="icon-halfstar"></em>}
                                {Array(5 - Math.round(rating)).fill().map((_, index) => <em key={index} className="icon-blankstar"></em>)}

                                <span>{rating}/5</span>
                            </span>
                        </div>
                        <div className="card__duration-mode mt-10">
                            Duration: <strong>{duration} days</strong>  |   Mode: <strong>{mode}</strong>
                        </div>
                        <div className="card__price mt-30">
                            <strong>{price}/-</strong>
                            { brochure ? <a href={brochure} className="icon-pdf"></a> : '' }
                        </div>
                    </div>
                </div>
            </li>
        </CustomOverlay>
    )
}
export default Product;
