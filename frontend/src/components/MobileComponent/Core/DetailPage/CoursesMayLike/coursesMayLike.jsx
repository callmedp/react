import React, { useEffect }  from 'react';
import { useSelector, useDispatch } from 'react-redux';
import '../../CataloguePage/RecentCourses/recentCourses.scss';
import ProductCards from '../ProductCards/productCards';
import { fetchRecommendedCourses } from 'store/DetailPage/actions';


const CoursesMayLike = (props) => {
    const {product_id, skill} = props;
    const dispatch = useDispatch()
    const { results } = useSelector(store => store.recommendedCourses)

    useEffect(() => {
        handleEffects();
    },[])

    const handleEffects = async () => {
        try {
            await new Promise((resolve, reject) => dispatch(fetchRecommendedCourses({ payload: {'skill': (skill && skill?.join(',')) || '', 'id': product_id, 'page': 6}, resolve, reject })));
        } 
        catch (error) {}
    };



    return(
        <section className="m-container mt-0 mb-0 pr-0" data-aos="fade-up">
            <h3 className="m-heading2 mb-10">Courses you may like</h3>
            <div className="m-courses m-recent-courses ml-10n">
                {
                    results?.length > 0 ? <ProductCards page_section={'courses_you_may_like'} productList = {results}/> : ''
                }
            </div>
        </section>
    )
}

export default CoursesMayLike;