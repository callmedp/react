import React, {useState} from 'react';
import '../../CataloguePage/RecentCourses/recentCourses.scss';
import { Link } from 'react-router-dom';
   
const OtherProviders = (props) => {
    return(
        <section className="container-fluid" data-aos="fade-up">
        <div className="row">
            <div className="container"> 
                <div className="recent-courses mt-20 mb-30">
                    <h2 className="heading2">Courses by other providers</h2>
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
                        </ul>
                </div>
            </div>
        </div>
    </section>
    )
}
   
export default OtherProviders;