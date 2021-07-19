import React, { useState } from 'react';
import {Link} from 'react-router-dom';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import './recommendedCourses.scss';
import { useSelector } from 'react-redux';
import ProductCards from '../../../Common/ProductCardsSlider/productCardsSlider';
import { TrendingCategoryList } from 'utils/constants';
import { siteDomain } from 'utils/domains';
import useLearningTracking from 'services/learningTracking';

const RecommendedCourses = (props) => {
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

    const sendLearningTracking = useLearningTracking();
    const { SnMCourseList, ITCourseList, BnFCourseList } = useSelector( store => store.popularCategories );
    const [selectedId, setSelectedId] = useState(0)
    const [category, setCategory] = useState('sales_and_marketing_category')

    const setSelectedClass = (event, index) => {
        event.preventDefault();

        if( index !== selectedId ){
            setSelectedId(index)
            let category = index === 0 ?   'sales_and_marketing_category' :
            index === 1 ?   'information_technology_category' :
                            'banking_and_finance_category' 
            setCategory(category)
            sendLearningTracking({
                productId: '',
                event: `catalogue_page_${category}_tab`,
                pageTitle:'catalogue_page',
                sectionPlacement: 'course_tray',
                eventCategory: category,
                eventLabel: '',
                eventAction: 'click',
                algo: '',
                rank: index
            })
        } 

    }

    const handleTracking = (category) => {
        sendLearningTracking({
            productId: '',
            event: `catalogue_page_${category}_view_all_courses`,
            pageTitle:'catalogue_page',
            sectionPlacement: 'course_tray',
            eventCategory: category,
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: ''
        })
    }

    return(
        <section className="m-container mt-0 mb-0 pr-0">
            <div className="m-recomend-courses">
                <h2 className="m-heading2 text-center">Recommended Courses</h2>
                <Slider {...settings}>
                    {
                        TrendingCategoryList?.map((category, index) =>{
                            return (
                                <div className="m-recomend-courses__tab" key={index}>
                                    <a className={selectedId === index ? 'selected':''} href="#" onClick={(event) => setSelectedClass(event, index)} >{category.name}</a>
                                </div>
                            )
                        })
                    }
                </Slider>
                <div className="m-courses m-recent-courses">
                {
                    category === 'sales_and_marketing_category' && 
                        <>
                            <ProductCards productList={SnMCourseList}
                                category="sales_and_marketing_category" />
                            <a href={`${siteDomain}/courses/sales-and-marketing/17/`} onClick = {() => handleTracking('sales_and_marketing_category')} className="m-load-more mt-5">View all courses</a>
                        </>
                }

                {
                    category === 'information_technology_category' &&
                        <>
                            <ProductCards productList={ITCourseList} 
                                category="information_technology_category"/>
                            <a href={`${siteDomain}/courses/it-information-technology/22/`} onClick = {() => handleTracking('information_technology_category')} className="m-load-more mt-5">View all courses</a>
                        </>
                }

                {
                    category === 'banking_and_finance_category' &&
                        <>
                            <ProductCards productList={BnFCourseList}
                                category="banking_and_finance_category" />
                            <a href={`${siteDomain}/courses/banking-and-finance/20/`} onClick = {() => handleTracking('banking_and_finance_category')} className="m-load-more mt-5">View all courses</a>
                        </>
                }
                </div>
            </div>
        </section>
    )
}
   
export default RecommendedCourses;