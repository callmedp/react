import React, { useState, useEffect } from "react";
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import { Link } from 'react-router-dom';
import './courses.scss';
import { useDispatch, useSelector } from 'react-redux';
import Product from './Product/product';
import { MyGA } from 'utils/ga.tracking.js';

const Courses = (props) => {
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
    useEffect(()=>{
        window.scrollTo(0, 0)
    },[])

    const { courseList } = useSelector(store => store.coursesTray)
    const { r_courses } = useSelector(store => store.recommendation)
    const [sliceFlag, setSliceFlag] = useState(true)
    const loadMore = () => {
        MyGA.SendEvent('SkillCourseLoadMore', 'ln_course_click', 'ln_know_more', 'ln_course','', false, true);
        setSliceFlag(state => !state);
    }

    return (
    <section className="m-container mt-0 mb-0 pb-0 pr-0">
        {
            r_courses?.length ?
            <>
                <h2 className="m-heading2 mb-10">Courses for you</h2>
                <div className="m-courses m-courses-slider ml-10n">
                    <Slider {...settings}>
                        {
                            r_courses?.map((course, idx)=> <Product product={course} key={idx} compType='For You' productType = 'Courses'/>)
                        }
                    </Slider>
                </div>
            </> : null
        }

        <h2 className="m-heading2 mt-0 mb-20">More courses</h2>
        <div className="m-courses mr-15">
            {
                (sliceFlag ? courseList.slice(0, 4) : courseList)?.map((course, idx)=> <Product product={course} key={idx + 100} compType='More Courses'/>)
            }
            { sliceFlag && (courseList?.length  > 4) ? <Link to={"#"} onClick={loadMore} className="m-load-more mt-20 mb-20">Load More Courses</Link> : '' }
        </div>
    </section>
    );
  }

export default Courses;