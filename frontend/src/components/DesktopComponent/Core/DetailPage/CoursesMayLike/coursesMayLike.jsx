import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import '../../CataloguePage/RecentCourses/recentCourses.scss';
import './coursesMayLike.scss'
import Carousel from 'react-bootstrap/Carousel';
import { fetchRecommendedCourses } from 'store/DetailPage/actions';
import { getTrackingInfo, getTrackingUrl } from 'utils/storage.js';
import { trackUser } from 'store/Tracking/actions/index.js';
import { siteDomain } from 'utils/domains';
import useLearningTracking from 'services/learningTracking';
import {stringReplace} from 'utils/stringReplace.js';

const CoursesMayLike = (props) => {
    const {product_id, skill} = props;
    const dispatch = useDispatch();
    const { results } = useSelector(store => store.recommendedCourses);
    const sendLearningTracking = useLearningTracking();
    const [carIndex, setIndex] = useState(0);

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

    const handleSelect = (selectedIndex, e) => {
        if (e !== undefined) {
            setIndex(selectedIndex);

            sendLearningTracking({
                productId: '',
                event: `course_detail_reviews_${e.target.offsetParent.className}_${selectedIndex}_clicked`,
                pageTitle:`course_detail`,
                sectionPlacement:'reviews',
                eventCategory: `${e.target.offsetParent.className}`,
                eventLabel: '',
                eventAction: 'click',
                algo: '',
                rank: selectedIndex,
            })
        }
    }

    const handleTracking = (name, vendor, url, idx) => {
        let tracking_data = getTrackingInfo();
        let appendTracking = "";

        dispatch(trackUser({"query" : tracking_data, "action" :'exit_product_page'}));
        dispatch(trackUser({"query" : tracking_data, "action" :'recommended_products'}));
        
        sendLearningTracking({
            productId: '',
            event: `course_detail_courses_you_may_like_${stringReplace(name)}_vendor_${stringReplace(vendor)}_${idx}_clicked`,
            pageTitle:'course_detail',
            sectionPlacement: 'courses_you_may_like',
            eventCategory: '',
            eventLabel: '',
            eventAction: 'click',
            algo: '',
            rank: idx,
        })

        if(localStorage.getItem("trackingId")){
            appendTracking = getTrackingUrl();
            window.location.href=`${siteDomain}${url}${appendTracking}`;
        }
        else window.location.href=`${siteDomain}${url}`;
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
                                                <img src={coursesLike.pImg} alt={coursesLike.display_name} />
                                            </figure>
                                            <h3 className="heading3">
                                                <a onClick={() => handleTracking(coursesLike.display_name, coursesLike.vendor, coursesLike.pURL, inx)}>
                                                    {coursesLike.display_name}
                                                </a>
                                            </h3>
                                        </div>

                                        <div className="card__box">
                                            <div className="card__rating">
                                                <span className="mr-10">By {(coursesLike.vendor)?.split(' ')[0]?.length > 10 ? (coursesLike.vendor)?.split(' ')[0]?.slice(0,10) + '...' : (coursesLike.vendor)?.split(' ')[0] }</span>
                                            <span className="rating">
                                                {coursesLike.pStar?.map((star, index) => starRatings(star, index))}
                                            </span>
                                                {/* <em className="icon-blankstar"></em> */}
                                                <span>{parseFloat(coursesLike.avg_rating)?.toFixed(1)}/5</span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>{parseInt(coursesLike.price)}/-</strong> 
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
                    <Carousel className={`courses-like ${results.length === 1 ? `removeButtons` : ``}`} activeIndex={carIndex} onSelect={handleSelect}>
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