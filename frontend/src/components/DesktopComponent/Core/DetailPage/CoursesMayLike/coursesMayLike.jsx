import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import '../../CataloguePage/RecentCourses/recentCourses.scss';
import './coursesMayLike.scss'
import Carousel from 'react-bootstrap/Carousel';
import { Link } from 'react-router-dom';
import { fetchRecommendedCourses } from 'store/DetailPage/actions';

const CoursesMayLike = (props) => {
    const {product_id, skill} = props;
    const dispatch = useDispatch();
    const { results } = useSelector(store => {console.log(store); return store.recommendedCourses});
    console.log(results);

    useEffect(() => {
        handleEffects();
    },[])

    const handleEffects = async () => {
        try {
            await new Promise((resolve, reject) => dispatch(fetchRecommendedCourses({ payload: {'skill': (skill && skill?.join(',')) || '', 'id': product_id, 'page': 6}, resolve, reject })));
        } 
        catch (error) {
            if (error?.status == 404) {
                // history.push('/404');
                console.log(error)
            }
        }
    };

    return(
        <section className="container" data-aos="fade-up">
            <div className="row">
                <div className="recent-courses mt-20 mb-30">
                    <h2 className="heading2 text-center">Courses you may like</h2>
                    <Carousel className="courses-like">
                        <Carousel.Item interval={10000000000}>
                            <ul className="recent-courses__list mt-30">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
                                            <span className="mr-10">By ERB</span>
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
                                            <span className="mr-10">By ERB</span>
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
                                            <span className="mr-10">By ERB</span>
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Carousel.Item>
                        <Carousel.Item interval={10000000000}>
                            <ul className="recent-courses__list mt-30">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
                                            <span className="mr-10">By ERB</span>
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
                                            <span className="mr-10">By ERB</span>
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
                                            <span className="mr-10">By ERB</span>
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Carousel.Item>
                        <Carousel.Item interval={10000000000}>
                            <ul className="recent-courses__list mt-30">
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing & Email Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
                                            <span className="mr-10">By ERB</span>
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Email Marketing Master Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
                                            <span className="mr-10">By ERB</span>
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                                <li className="col">
                                    <div className="card">
                                        <div className="card__heading">
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="card__box">
                                            <div className="card__rating">
                                            <span className="mr-10">By ERB</span>
                                            <span className="rating">
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-fullstar"></em>
                                                <em className="icon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            </div>
                                            <div className="card__price mt-10">
                                                <strong>12999/-</strong> 
                                            </div>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </Carousel.Item>
                    </Carousel>
                </div>
        </div>
    </section>
    )
}
   
export default CoursesMayLike;