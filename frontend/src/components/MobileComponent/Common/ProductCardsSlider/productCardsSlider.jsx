import React from 'react';
import Slider from "react-slick";
import { siteDomain } from 'utils/domains';
import './productCardsSlider.scss';
import useLearningTracking from 'services/learningTracking';
import { MyGA } from 'utils/ga.tracking.js';

const ProductCards = props => {
    const {
        productList, selectedIndexName, noProvider, showMode
    } = props;
    const sendLearningTracking = useLearningTracking();
    console.log(selectedIndexName)

    const settings = {
        dots: false,
        arrows: false,
        infinite: true,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        variableWidth: true,
    };

    const starRatings = (star, index) => {
        return (
            star === '*' ? <em className="micon-fullstar" key={index}></em> :
                star === '+' ? <em className="micon-halfstar" key={index}></em> :
                    <em className="micon-blankstar" key={index}></em>
        )
    }

    const mostViewedTracking = (name, indx) => {
        let name_joined = name.replace(/ /g, '_');
        
        MyGA.SendEvent('ln_new_homepage','ln_most_viewed_course', 'ln_'+selectedIndexName, name_joined,'', false, true);

        sendLearningTracking({
            productId: '',
            event: `homepage_most_viewed_course_${selectedIndexName}_${name_joined}_${indx}_clicked`,
            pageTitle:`homepage`,
            sectionPlacement:'most_viewed_courses',
            eventCategory: `${name_joined}`,
            eventLabel: `${selectedIndexName}_${name_joined}`,
            eventAction: 'click',
            algo: '',
            rank: indx,
        })
    }

    return (
    // <section className="m-courses mt-0 mb-0 pt-10 pb-0" >
    //     <h2 className="m-heading centered">Popular Courses</h2>
        <Slider {...settings}>
            {
                productList?.map((product, index) => {
                    return (
                        <div className="m-card" key={index} itemProp="itemListElement" itemScope itemType="https://schema.org/ListItem">
                            <div className="m-card__heading" itemProp="image">
                                <figure>
                                    <img src={product?.imgUrl} alt={product?.imgAlt} />
                                </figure>
                                <h3 className="m-heading3" itemProp="item">
                                    <a href={`${siteDomain}${product.url}`} onClick={() => mostViewedTracking(product.name, index)}><span itemProp="name">{(product?.name)?.length > 42 ? (product?.name)?.slice(0, 42) + '...' : (product?.name) }</span></a>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating" itemProp="aggregateRating" itemScope itemType="https://schema.org/AggregateRating">
                                    {
                                        !!noProvider ? '' :
                                            <span className="mr-10">
                                                By { product?.providerName?.split(' ')[0]?.length > 13 ? product?.providerName?.split(' ')[0]?.slice(0, 13) + '...' : product?.providerName?.split(' ')[0] }
                                            </span>
                                    }
                                    <span className="m-rating">
                                        { product?.stars?.map((star, index) => starRatings(star, index)) }
                                        <span itemProp="ratingValue">{product?.rating?.toFixed(1)}/5</span>
                                    </span>
                                    {
                                        !!showMode && product?.mode ? <span className="m-mode">{product.mode}</span> : ''
                                    }
                                </div>
                                <div className="m-card__price">
                                    <strong>{product?.price}/-</strong>
                                </div>
                            </div>
                        </div>
                    )
                })
            }
        </Slider>
        // </section>
    )
}

export default ProductCards;