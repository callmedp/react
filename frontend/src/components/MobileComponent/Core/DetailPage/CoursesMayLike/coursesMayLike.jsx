import React, { useEffect }  from 'react';
import { useSelector, useDispatch } from 'react-redux';
// import 'slick-carousel/slick/slick.css';
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
                    results?.length > 0 ? <ProductCards productList = {results}/> : ''
                }
                {/* <Slider {...settings}>
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
                </Slider> */}
            </div>
        </section>
    )
}

export default CoursesMayLike;