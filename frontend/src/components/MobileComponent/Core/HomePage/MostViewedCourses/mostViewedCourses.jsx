import React, { useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
import './mostViewedCourses.scss';
import { categoryTabs } from 'utils/constants';
import { fetchMostViewedCourses } from 'store/HomePage/actions';
import ProductCardsSlider from '../../../Common/ProductCardsSlider/productCardsSlider';
import { startHomePageLoader, stopHomePageLoader } from 'store/Loader/actions/index';
import useLearningTracking from 'services/learningTracking';

const MostViewedCourses = () => {
    const settings = {
        dots: false,
        arrows: false,
        infinite: false,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        variableWidth: true,
    };

    const dispatch = useDispatch()
    const [selectedIndex, setSelectedIndex] = useState('-1');
    const [selectedIndexName, setSelectedIndexName] = useState('all')

    const { mostViewedCourses } = useSelector(store => store.mostViewed);
    const sendLearningTracking = useLearningTracking();

    const handleCategory = async (tabType, tabName, key) => {
        try {
            if (!mostViewedCourses[tabType] || mostViewedCourses[tabType].length === 0) {
                dispatch(startHomePageLoader());
                await new Promise((resolve, reject) => dispatch(fetchMostViewedCourses({ payload: {categoryId: tabType}, resolve, reject })))
                dispatch(stopHomePageLoader());
            }
        }
        catch (e) {
            dispatch(stopHomePageLoader());
        }
        setSelectedIndex(tabType);
        setSelectedIndexName(tabName);
        
        sendLearningTracking({
            productId: '',
            event: `homepage_most_viewed_course_${tabType}_${key}_tab_clicked`,
            pageTitle:`homepage`,
            sectionPlacement:'most_viewed_courses',
            eventCategory: tabType,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: key,
        })
    }


    return (
        <section className="m-container mt-0 mb-0 m-lightblue-bg pr-0 ml-10n" data-aos="fade-up">
            <div className="m-recomend-courses">
                <h2 className="m-heading2-home text-center">Most Viewed Courses</h2>
                <Slider {...settings}>
                    {
                        categoryTabs?.map((category, index) => {
                            return (
                                <div className="m-recomend-courses__tab" key={category?.id} >
                                    <Link className={selectedIndex === category.id ? 'selected' : ''} to={'#'} onClick={() => handleCategory(category.id, category?.name, index)}>{category?.name}</Link>
                                </div>
                            )
                        })
                    }
                </Slider>
                <div className="m-courses m-recent-courses">
                    {
                        <ProductCardsSlider productList={mostViewedCourses[selectedIndex]} selectedIndexName={selectedIndexName} noProvider={true} showMode={true} />
                    }
                </div>
            </div>
        </section>
    )
}

export default MostViewedCourses;