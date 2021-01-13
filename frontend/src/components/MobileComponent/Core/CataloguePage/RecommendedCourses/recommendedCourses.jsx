import React, { useState } from 'react';
import {Link} from 'react-router-dom';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import './recommendedCourses.scss';
import { useSelector } from 'react-redux';
import ProductCards from '../../../Common/ProductCardsSlider/productCardsSlider';

const RecommendedCourses = (props) => {
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

    const trendingCategories = ['Sales and Marketing', 'Information Technology', 'Banking & Finance']
    const { SnMCourseList, ITCourseList, BnFCourseList } = useSelector( store => store.popularCategories );
    const [selectedId, setSelectedId] = useState(0)
    const [category, setCategory] = useState('SnM')

    const setSelectedClass = (event, index) => {
        event.preventDefault();

        if( index !== selectedId ){
            setSelectedId(index)
            index === 0 ?   setCategory('SnM') :
            index === 1 ?   setCategory('IT') :
                            setCategory('BnF')  
        }
    }

    return(
        <section className="m-container mt-0 mb-0 pr-0">
            <div className="m-recomend-courses">
                <h2 className="m-heading2 text-center">Recommended Courses</h2>
                <Slider {...settings}>
                    {
                        trendingCategories?.map((category, index) =>{
                            return (
                                <div className="m-recomend-courses__tab" key={index}>
                                    <a className={selectedId === index ? 'selected':''} href="#" onClick={(event) => setSelectedClass(event, index)} >{category}</a>
                                </div>
                            )
                        })
                    }
                </Slider>
                <div className="m-courses m-recent-courses">
                {
                    category === 'SnM' && <ProductCards productList={SnMCourseList} />
                }

                {
                    category === 'IT' && <ProductCards productList={ITCourseList} />
                }

                {
                    category === 'BnF' && <ProductCards productList={BnFCourseList} />
                }
                </div>
                <Link to={"#"} className="m-load-more mt-5">View all courses</Link>
            </div>
        </section>
    )
}
   
export default RecommendedCourses;