import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import 'slick-carousel/slick/slick.css';
import '../../CataloguePage/RecentCourses/recentCourses.scss';
import ProductCardsSlider from '../../../Common/ProductCardsSlider/productCardsSlider';
import { fetchOtherProviderCourses } from 'store/DetailPage/actions';

const OtherProviders = (props) => {

    const { otherProvidersCourses } = useSelector(store => store.otherCourses);
    const dispatch = useDispatch()

    const handleEffects = async () => {
        try {
            await new Promise((resolve, reject) => dispatch(fetchOtherProviderCourses({ resolve, reject })));
        }
        catch (error) {
            if (error?.status == 404) {
                // history.push('/404');
            }
        }
    };

    useEffect(() => {
        handleEffects();
    }, [])

    return(
        <section className="m-container mt-0 mb-0 pr-0" data-aos="fade-up">
            <h2 className="m-heading2 mb-10 mt-10">Courses by other providers</h2>
            <div className="m-courses m-recent-courses ml-10n">
                {
                    otherProvidersCourses?.length > 0 ? <ProductCardsSlider productList = {otherProvidersCourses}/> : ''
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

export default OtherProviders;