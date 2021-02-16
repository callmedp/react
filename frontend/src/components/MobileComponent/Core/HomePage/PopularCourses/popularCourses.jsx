// React-Core Import
import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import Slider from "react-slick";
import { useSelector, useDispatch } from 'react-redux';

// Inter-App Import
// import 'slick-carousel/slick/slick.css';
import './popularCourses.scss';
import { populartabType } from 'utils/constants';
import { siteDomain } from 'utils/domains';
import PopularTab from './popularTab';

// API Import
import { fetchInDemandProducts } from 'store/HomePage/actions';
import { startHomePageLoader, stopHomePageLoader } from 'store/Loader/actions';

const PopularCourses = (props) => {

    const [key, setKey] = useState('master');
    const { courses, certifications } = useSelector(store => store.inDemand)
    const dispatch = useDispatch()

    const handleTabChange = async (tabType, id) => {
        try {
            if (tabType === 'certifications' && certifications.length === 0) {
                dispatch(startHomePageLoader())
                await new Promise((resolve, reject) => dispatch(fetchInDemandProducts({ pageId: 1, tabType, device: 'mobile', resolve, reject })));
                dispatch(stopHomePageLoader())
            }
            setKey(tabType)
        }
        catch (e) {
            dispatch(stopHomePageLoader());
        }
    };

    return (
        <section className="m-container mt-0 mb-0 pr-0 pt-20 pb-0">
            <div className="m-courses m-popular-course-demand">
                <h2 className="m-heading2-home text-center">Popular courses in demand</h2>

                <div className="m-tabset-pop">
                    {populartabType?.map((tab, index) => {
                        return (
                            <React.Fragment key={index}>
                                <input  type="radio" name="tabset" id={`tab${index}`} aria-controls={tab?.visible} defaultChecked={key === tab?.slug ? true : false} onClick={() => handleTabChange(tab?.slug, index)} />
                                <label htmlFor={`tab${index}`}>{tab?.visible}</label>
                            </React.Fragment>
                        )
                    })
                    }

                    {/* <input type="radio" name="tabset" id="tab2" aria-controls="Certifications" />
                    <label htmlFor="tab2">Certifications</label> */}
                    <div className="tab-panels">
                        {populartabType?.map((tab, index) => {
                            return (
                                <div id={`tab${index}`} className="tab-panel" key={index}>
                                    <div className="m-courses">

                                        {key === 'master' ?
                                            <PopularTab productList={courses} tabType={key}/>
                                            :
                                            <PopularTab productList={certifications} tabType={key}/>
                                        }

                                    </div>
                                </div>
                            )
                        })
                        }
                    </div>

                    {/* <div className="m-card">
                                        <div className="m-card__heading colbg2">
                                            <span className="m-flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="m-heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating mt-5">
                                            <span className="m-rating">
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="m-mode">Online</span>
                                            </div>
                                            <div className="m-card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="m-view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div> 
                                    <div className="m-card">
                                        <div className="m-card__heading colbg3">
                                            <span className="m-flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="m-heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating mt-5">
                                            <span className="m-rating">
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="m-mode">Online</span>
                                            </div>
                                            <div className="m-card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="m-view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div>
                                    <div className="m-card">
                                        <div className="m-card__heading colbg4">
                                            <span className="m-flag-yellow">BESTSELLER</span>
                                            <figure>
                                                <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                            </figure>
                                            <h3 className="m-heading3">
                                                <Link to={"#"}>Digital Marketing Training Course</Link>
                                            </h3>
                                        </div>
                                        <div className="m-card__box">
                                            <div className="m-card__rating mt-5">
                                            <span className="m-rating">
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-fullstar"></em>
                                                <em className="micon-blankstar"></em>
                                                <span>4/5</span>
                                            </span>
                                            <span className="m-mode">Online</span>
                                            </div>
                                            <div className="m-card__duration-mode mt-10">
                                                <strong>2819</strong> Jobs available | Duration: <strong>90 days</strong>
                                            </div>
                                            <Link className="m-view-program mt-10" to={"#"}>View program</Link>
                                        </div>
                                    </div> */}

                </div>

            </div>
        </section>
    )
}

export default PopularCourses;