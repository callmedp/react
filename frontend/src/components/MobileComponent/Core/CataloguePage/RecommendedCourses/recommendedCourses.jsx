import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
// import 'slick-carousel/slick/slick.css';
import './recommendedCourses.scss';
import { useSelector } from 'react-redux';

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
    // const { trendingCategories } = useSelector( store => store.popularCategories );
    const trendingCategories = ['Sales and Marketing', 'Information Technology', 'Banking & Finance']
    const [selectedId, setSelectedId] = useState(0)
    const [showCategory1, setShowCategory1] = useState(true)
    const [showCategory2, setShowCategory2] = useState(false)
    const [showCategory3, setShowCategory3] = useState(false)

    const setSelectedClass = (event, index) => {
        event.preventDefault();
        if(index !== selectedId){
            setSelectedId(index)
            if(index===0){
                setShowCategory2(false)
                setShowCategory1(true)
                setShowCategory3(false)
            }
            if(index===1){
                setShowCategory2(true)
                setShowCategory1(false)
                setShowCategory3(false)
            }
            if(index===2){
                setShowCategory2(false)
                setShowCategory1(false)
                setShowCategory3(true)
            }
        }
    }

    return(
        <section className="m-container mt-0 mb-0">
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
                    showCategory1 && (
                        <Slider {...settings}>
                            <div className="m-card">
                                <div className="m-card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="m-heading3">
                                        <Link to={"#"}>Digital Marketing Training Course Programme 1</Link>
                                    </h3>
                                </div>
                                <div className="m-card__box">
                                    <div className="m-card__rating">
                                    <span className="mr-10">By ERB</span>
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="m-card__price">
                                        <strong>12999/-</strong> 
                                    </div>
                                </div>
                            </div>
                            <div className="m-card">
                                <div className="m-card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="m-heading3">
                                        <Link to={"#"}>Digital Marketing Training Course Programme</Link>
                                    </h3>
                                </div>
                                <div className="m-card__box">
                                    <div className="m-card__rating">
                                    <span className="mr-10">By ERB</span>
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="m-card__price">
                                        <strong>12999/-</strong> 
                                    </div>
                                </div>
                            </div>
                        </Slider>
                    )
                }

                {
                    showCategory2 && (
                        <Slider {...settings}>
                            <div className="m-card">
                                <div className="m-card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="m-heading3">
                                        <Link to={"#"}>Digital Marketing Training Course Programme 2</Link>
                                    </h3>
                                </div>
                                <div className="m-card__box">
                                    <div className="m-card__rating">
                                    <span className="mr-10">By ERB</span>
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="m-card__price">
                                        <strong>12999/-</strong> 
                                    </div>
                                </div>
                            </div>
                            <div className="m-card">
                                <div className="m-card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="m-heading3">
                                        <Link to={"#"}>Digital Marketing Training Course Programme</Link>
                                    </h3>
                                </div>
                                <div className="m-card__box">
                                    <div className="m-card__rating">
                                    <span className="mr-10">By ERB</span>
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="m-card__price">
                                        <strong>12999/-</strong> 
                                    </div>
                                </div>
                            </div>
                        </Slider>
                    )
                }

                {
                    showCategory3 && (
                        <Slider {...settings}>
                            <div className="m-card">
                                <div className="m-card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="m-heading3">
                                        <Link to={"#"}>Digital Marketing Training Course Programme 3</Link>
                                    </h3>
                                </div>
                                <div className="m-card__box">
                                    <div className="m-card__rating">
                                    <span className="mr-10">By ERB</span>
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="m-card__price">
                                        <strong>12999/-</strong> 
                                    </div>
                                </div>
                            </div>
                            <div className="m-card">
                                <div className="m-card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="m-heading3">
                                        <Link to={"#"}>Digital Marketing Training Course Programme</Link>
                                    </h3>
                                </div>
                                <div className="m-card__box">
                                    <div className="m-card__rating">
                                    <span className="mr-10">By ERB</span>
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="m-card__price">
                                        <strong>12999/-</strong> 
                                    </div>
                                </div>
                            </div>
                        </Slider>
                    )
                }
                </div>
            </div>
        </section>
    )
}
   
export default RecommendedCourses;