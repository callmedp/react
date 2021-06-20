import React from 'react';
import './Banner.scss';
import Slider from "react-slick";
import { categoryList } from 'utils/constants';
import { MyGA } from 'utils/ga.tracking.js';
import useLearningTracking from 'services/learningTracking';

const HomeBanner = (props) => {
    const { setShowSearch } = props;
    const sendLearningTracking = useLearningTracking();

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

    const bannerTracking = (title, ln_title, event_clicked, name, val, val1, val2, indx) => {
        let name_joined = name.replace(/ /g, '_');
        MyGA.SendEvent(title, ln_title, event_clicked, name_joined, val, val1, val2);

        sendLearningTracking({
            productId: '',
            event: `homepage_${name_joined}${indx ? '_' + indx : ''}_banner_clicked`,
            pageTitle:`homepage`,
            sectionPlacement:'banner',
            eventCategory: name_joined,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: indx,
        })
    }

    return (
        <div className="m-container mt-0 mb-0 m-home-header">
            <div className="m-top-search-header-home" onClick={() => setShowSearch(true)}>
                <form id="searchForm" className="form-inline w-100 ml-auto">
                    <button className="m-btn-search-black d-flex align-items-center"><figure className="micon-search-black d-flex"></figure></button>
                    <input className="m-search-input" type="search" placeholder="Search course, assessment..." name="query" id="transcript" aria-label="Search" autoComplete="off" />
                    <button className="m-btn-voice-search">
                        <figure className="micon-voice-search d-flex"></figure>
                    </button>
                </form>
            </div>
            {/* <SearchPage crossSearch={false} placeholder="Try Digital marketing certificate"/> */}

            <div className="m-header-nav">
                <figure className="micon-home-nav"></figure>
                    <Slider {...settings}>
                        {
                            categoryList?.map((category, idx) => {
                                return (
                                    <a href={ category?.url } key={ category?.id } onClick = { () => bannerTracking('ln_new_homepage','ln_search_course', 'ln_search_initiated', category?.name,'', false, true, idx) }>{ category?.name }</a>
                                )
                            })
                        }
                    </Slider>
            </div>
        </div>
    )
}

export default HomeBanner;