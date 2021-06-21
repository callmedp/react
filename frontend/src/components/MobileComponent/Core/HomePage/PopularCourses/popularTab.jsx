// React-Core Import
import React, { useState } from 'react';
import Slider from "react-slick";
import { siteDomain } from 'utils/domains';
import { useDispatch } from 'react-redux';
import { MyGA } from 'utils/ga.tracking.js';
import {stringReplace} from 'utils/stringReplace.js';

// API Import 
import { fetchInDemandProducts } from 'store/HomePage/actions';
import useLearningTracking from 'services/learningTracking';

const PopularTab = props => {
    const [pageId, updatePageId] = useState(2)
    const dispatch = useDispatch()
    const {
        productList, tabType, total_page
    } = props;
    const sendLearningTracking = useLearningTracking();

    const settings = {
        dots: false,
        arrows: false,
        infinite: false,
        speed: 500,
        slidesToShow: 1,
        autoplay: false,
        slidesToScroll: 1,
        swipeToSlide: true,
        variableWidth: true,
        afterChange: function(index) {
            if ((index % 3 === 0 && pageId < index ) && pageId <= total_page) {
                new Promise((resolve, reject) => dispatch(fetchInDemandProducts({ payload:{ pageId: pageId, tabType, device: 'mobile'}, resolve, reject })));
                updatePageId(pageId + 1);

                sendLearningTracking({
                    productId: '',
                    event: `homepage_popular_courses_${tabType}_${pageId}_next_clicked`,
                    pageTitle:`homepage`,
                    sectionPlacement:'popular_courses',
                    eventCategory: tabType,
                    eventLabel: '',
                    eventAction: 'click',
                    algo: '',
                    rank: pageId,
                })
            }
          }
    };


    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+'
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    const setTracking = (name, indx) => {

        sendLearningTracking({
            productId: '',
            event: `homepage_popular_courses_${stringReplace(name)}_${indx}_clicked`,
            pageTitle:`homepage`,
            sectionPlacement: 'popular_courses',
            eventCategory: stringReplace(name),
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: indx,
        })
    }

    return (
        <Slider {...settings}>
            {   
                productList?.map((product, index) => {
                    return (
                        <div className="m-card" key={index} onClick={() => tabType == 'master' ? MyGA.SendEvent('ln_new_homepage', 'ln_popular_course_select', 'ln_masters_course_click', product.name, '', false, true) : MyGA.SendEvent('ln_new_homepage', 'ln_popular_course_select', 'ln_certification_course_click', product.name, '', false, true)}
                        >
                            <div className={`m-card__heading colbg${index > 4 ? index % 4 + 1 : index + 1 }`} onClick={() => tabType == 'master' ? MyGA.SendEvent('ln_new_homepage', 'ln_popular_course_select', 'ln_masters_course_click', product.name, '', false, true) : MyGA.SendEvent('ln_new_homepage', 'ln_popular_course_select', 'ln_certification_course_click', product.name, '', false, true)}>
                                {/* <span className="m-flag-yellow">BESTSELLER</span> */}
                                {product.tags === 2 && <span className="m-flag-yellow">NEW</span>}
                                {product.tags === 1 && <span className="m-flag-yellow">BESTSELLER</span>}
                                <figure>
                                    <img src={product.imgUrl} alt={product.imageAlt} itemProp="image" />
                                </figure>
                                <h3 className="m-heading3">
                                    <a href={`${siteDomain}${product.url}`} onClick={() => setTracking(product?.name, index)} itemProp="url"> {product?.name?.length > 22 ? product?.name?.slice(0, 22) + '...' : product?.name} </a>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating mt-5">
                                    <span className="m-rating">
                                        {product.stars?.map((star, index) => starRatings(star, index))}
                                        <span>{product.rating?.toFixed(1)}/5</span>
                                    </span>
                                    {/* <span className="m-mode">Online</span> */}
                                    {product.mode ? <span className="m-mode">{product.mode}</span> : ''}
                                </div>
                                <div className="m-card__duration-mode mt-10">
                                    {product.jobsAvailable ? <> <strong>{product.jobsAvailable}</strong> Jobs available </> : ''} {product.jobsAvailable && product.duration ? '|' : ''} {product.duration ? <>Duration: <strong>{product.duration}</strong> </> : <strong>&nbsp;</strong>}
                                </div>
                                <a className="m-view-program mt-10" href={`${siteDomain}${product.url}`} onClick={() => tabType == 'master' ? MyGA.SendEvent('ln_new_homepage', 'ln_popular_course_select', 'ln_masters_course_click', product.name, '', false, true) : MyGA.SendEvent('ln_new_homepage', 'ln_popular_course_select', 'ln_certification_course_click', product.name, '', false, true)}>View program</a>
                            </div>
                        </div>
                    )
                })
            }
        </Slider>
    )
}

export default PopularTab;