import React, { useEffect, useState } from 'react';
import { siteDomain } from 'utils/domains';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import PopOverDetail from '../PopOverDetail/popOverDetail';

const Product = (props) => {

    const { product: {
                        newlyAdded, bestSeller,
                        name, providerName,
                        rating, mode,
                        price, imgUrl,
                        url
                        },
            index } = props

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
        <li className="col" key={index}>
        <OverlayTrigger trigger={["hover", "focus"]} placement="left" overlay={<PopOverDetail/>} >
            <div className="card">
                <div className="card__heading">
                    {newlyAdded && <span className="flag-blue">NEW</span>}
                    {bestSeller && <span className="flag-red">BESTSELLER</span>}
                    <figure>
                        <img src={ imgUrl } alt={name} />
                    </figure>
                    <h3 className="heading3">
                        <a href={`${siteDomain}${url}`} >{name}</a>
                    </h3>
                </div>
                <div className="card__box">
                    <div className="card__rating mt-5">
                        <span className="mr-10">By {providerName}</span>
                        <span className="rating">

                            { Array(parseInt(rating)).fill().map((_,index) =>  <em key={index} className="icon-fullstar"></em>) }
                            { halfStar && <em className="icon-halfstar"></em> }
                            { Array(5-parseInt(rating)).fill().map((_,index) =>  <em key={index} className="icon-blankstar"></em>) }
  
                            <span>{rating}/5</span>
                        </span>
                    </div>
                    <div className="card__duration-mode mt-10">
                        Duration: <strong>90 days</strong>  |   Mode: <strong>{ mode }</strong>
                    </div>
                    <div className="card__price mt-30">
    <strong>{price}/-</strong>
                        <a href={`${siteDomain}${url}`} className="icon-pdf"></a>
                    </div>
                </div>
            </div>
        </OverlayTrigger>
        </li>
    )
}

export default Product;