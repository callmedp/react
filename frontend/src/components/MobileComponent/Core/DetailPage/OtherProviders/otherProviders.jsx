import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
// import 'slick-carousel/slick/slick.css';
import '../../CataloguePage/RecentCourses/recentCourses.scss';
import ProductCardsSlider from '../../../Common/ProductCardsSlider/productCardsSlider';

const OtherProviders = () => {
    const { pop_list } = useSelector(store => store.recommendedCourses);

    return(
        <section className="m-container mt-0 mb-0 pr-0" data-aos="fade-up">
            <h2 className="m-heading2 mb-10 mt-10">Courses by other providers</h2>
            <div className="m-courses m-recent-courses ml-10n">
                {
                    pop_list?.length > 0 ? <ProductCardsSlider productList = {pop_list}/> : ''
                }
            </div>
        </section>
    )
}

export default OtherProviders;