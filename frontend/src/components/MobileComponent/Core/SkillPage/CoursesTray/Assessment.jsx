import React, { useState, useEffect } from "react";
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import { Link } from 'react-router-dom';
import './courses.scss';
import { useDispatch, useSelector } from 'react-redux';
import Product from './Product/product';
import { MyGA } from 'utils/ga.tracking.js';

const Assessment = (props) => {
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

    const { assessmentList } = useSelector(store => store.coursesTray)
    const { r_assesments } = useSelector(store => store.recommendation)
    const [sliceFlag, setSliceFlag] = useState(true)

    const loadMore = () => {
        MyGA.SendEvent('SkillAssesmentLoadMore', 'ln_course_click', 'ln_know_more', 'ln_assessment','', false, true);
        setSliceFlag(state => !state);
    }

    useEffect(()=>{
        window.scrollTo(0, 0)
    },[])

    return (
    <section className="m-container mt-0 mb-0 pb-0 pr-0">
        {
            r_assesments?.length ?
            <>
                <h2 className="m-heading2 mb-10">Assessments for you</h2>
                <div className="m-courses m-courses-slider ml-10n">
                    <Slider {...settings}>
                        {
                            r_assesments?.map((assessment, idx)=> <Product product={assessment} key={idx} compType='For You'/>)
                        }
                    </Slider>
                </div>
            </> : null
        }

        <h2 className="m-heading2 mt-0 mb-20">More assessments</h2>
        <div className="m-courses mr-15">
            {
                (sliceFlag ? assessmentList.slice(0, 4) : assessmentList)?.map((assessment, idx)=> <Product product={assessment} key={idx + 100} compType='More Courses'/>)
            }
            { sliceFlag && (assessmentList?.length > 4) ? <Link to={"#"} onClick={loadMore} className="m-load-more mt-20 mb-20">Load More Assessments</Link> : '' }
        </div>
    </section>
    );
  }

export default Assessment;