import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import '../../CataloguePage/RecentCourses/recentCourses.scss';
import './coursesMayLike.scss'
import Carousel from 'react-bootstrap/Carousel';
import { fetchRecommendedCourses } from 'store/DetailPage/actions';
import { getTrackingInfo } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import { siteDomain } from 'utils/domains';

const CoursesMayLike = (props) => {
    const {product_id, skill} = props;
    const dispatch = useDispatch();
    const { results } = useSelector(store => store.recommendedCourses);
    const tracking_data = getTrackingInfo();

    useEffect(() => {
        handleEffects();
    },[])

    const handleEffects = async () => {
        try {
            await new Promise((resolve, reject) => dispatch(fetchRecommendedCourses({ payload: {'skill': (skill && skill?.join(',')) || '', 'id': product_id, 'page': 6, 'device': 'desktop'}, resolve, reject })));
        } 
        catch (error) {}
    };

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+'
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    const handleTracking = (url) => {
        dispatch(trackUser({"query" : tracking_data, "action" :'exit_product_page'}));
        dispatch(trackUser({"query" : tracking_data, "action" :'recommended_products'}));
        window.location.href=`${siteDomain}${url}`;
    }

    const getLikeCourses = (courseData, idx) => {
        return (
            <Carousel.Item interval={10000000000} key={idx}>
                <ul className="recent-courses__list mt-30">
                    {
                        courseData?.map((coursesLike, inx) => {
                            return (
                                <li className="col-4" key={inx}>
                                    <div className="card">
                                        <div className="card__heading cursorLink">
                                            <figure>
                                                <img src={coursesLike.pImg} alt={coursesLike.name} />
                                            </figure>
                                            <h3 className="heading3">
                                                <a onClick={() => handleTracking(coursesLike.pURL)}>
                                                    {coursesLike.name || coursesLike.pNm}
                                                </a>
                                            </h3>
                                        </div>

                                        <div className="card__box">
                                            <div className="card__rating">
                                                <span className="mr-10">By {(coursesLike.pPvn || coursesLike.pViA)?.split(' ')[0]?.length > 10 ? (coursesLike.pPvn || coursesLike.pViA)?.split(' ')[0]?.slice(0,10) + '...' : (coursesLike.pPvn || coursesLike.pViA)?.split(' ')[0] }</span>
                                            <span className="rating">
                                                {coursesLike.pStar?.map((star, index) => starRatings(star, index))}
                                            </span>
                                                <em className="icon-blankstar"></em>
                                                <span>{parseInt(coursesLike.pAR)?.toFixed(1)}/5</span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>{coursesLike.pPin}/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            )
                        })
                    }
                </ul>
            </Carousel.Item>
        )
    }

    return(
        <section className="container" data-aos="fade-up">
            <div className="row">
                <div className="recent-courses w-100 mt-20 mb-30">
                    <h3 className="heading2 text-center">Courses you may like</h3>
                    <Carousel className={`courses-like ${results.length === 1 ? `removeButtons` : ``}`}>
                        {
                            results?.map(getLikeCourses)
                        }
                    </Carousel>
                </div>
            </div>
        </section>
    )
}
   
export default CoursesMayLike;