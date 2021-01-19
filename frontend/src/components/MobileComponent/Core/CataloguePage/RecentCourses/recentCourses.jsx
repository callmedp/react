import React from 'react';
// import 'slick-carousel/slick/slick.css';
import './recentCourses.scss'
import { useSelector } from 'react-redux';
import ProductCards from '../../../Common/ProductCardsSlider/productCardsSlider';

const RecentCourses = (props) => {
    const { recentCoursesList } = useSelector(store => store.recentCourses);

    return(
        <section className="m-container m-lightblue-bg mt-0 mb-0" data-aos="fade-up">
            <div className="m-courses m-recent-courses">
                <h2 className="m-heading2 text-center">Recently added courses</h2>
                <ProductCards productList={recentCoursesList?.slice(0,4)} />
            </div>
        </section>
    )
}

export default RecentCourses;