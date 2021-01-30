import React, {useState} from 'react';
import './recruitersLooking.scss';
import { Link } from 'react-router-dom';
import Carousel from 'react-bootstrap/Carousel';

   
const RecruitersLooking = (props) => {
    return(
        <section className="container-fluid mt-0 mb-0" data-aos="fade-up">
            <div className="row">
                <div className="container"> 
                    <div className="all-category mt-40 mb-30 pos-rel">
                        <h2 className="heading2 mb-5 text-center">What recruiters are looking at</h2>
                        <p className="text-center">Browse the skills with high demands to enhance your career</p>
                        <Carousel>
                            <Carousel.Item interval={10000000000}>
                                <ul className="all-category__list">
                                    <li className="col-sm-3">
                                        <div className="card">
                                            <figure>
                                                <img src="./media/images/categories1.jpg" className="img-fluid" alt="Personal Development" />
                                            </figure>
                                            <h3>Personal Development</h3>
                                            <strong>30 courses</strong>
                                            <Link to={"#"}>Know more</Link>
                                        </div>
                                    </li>
                                    <li className="col-sm-3">
                                        <div className="card">
                                            <figure>
                                                <img src="./media/images/categories2.jpg" className="img-fluid" alt="Information Technology" />
                                            </figure>
                                            <h3>Information Technology</h3>
                                            <strong>30 courses</strong>
                                            <Link to={"#"}>Know more</Link>
                                        </div>
                                    </li>
                                    <li className="col-sm-3">
                                        <div className="card">
                                            <figure>
                                                <img src="./media/images/categories3.jpg" className="img-fluid" alt="Sales and Marketing" />
                                            </figure>
                                            <h3>Sales and Marketing</h3>
                                            <strong>30 courses</strong>
                                            <Link to={"#"}>Know more</Link>
                                        </div>
                                    </li>
                                    <li className="col-sm-3">
                                        <div className="card">
                                            <figure>
                                                <img src="./media/images/categories4.jpg" className="img-fluid" alt="Human Resources (HR)" />
                                            </figure>
                                            <h3>Human Resources (HR)</h3>
                                            <strong>30 courses</strong>
                                            <Link to={"#"}>Know more</Link>
                                        </div>
                                    </li>
                                </ul>
                            </Carousel.Item>
                            <Carousel.Item>
                                <ul className="all-category__list">
                                    <li className="col-sm-3">
                                        <div className="card">
                                            <figure>
                                                <img src="./media/images/categories5.jpg" className="img-fluid" alt="Management" />
                                            </figure>
                                            <h3>Management</h3>
                                            <strong>30 courses</strong>
                                            <Link to={"#"}>Know more</Link>
                                        </div>
                                    </li>
                                    <li className="col-sm-3">
                                        <div className="card">
                                            <figure>
                                                <img src="./media/images/categories6.jpg" className="img-fluid" alt="Law" />
                                            </figure>
                                            <h3>Law</h3>
                                            <strong>30 courses</strong>
                                            <Link to={"#"}>Know more</Link>
                                        </div>
                                    </li>
                                    <li className="col-sm-3">
                                        <div className="card">
                                            <figure>
                                                <img src="./media/images/categories7.jpg" className="img-fluid" alt="Operation Management" />
                                            </figure>
                                            <h3>Operation Management</h3>
                                            <strong>30 courses</strong>
                                            <Link to={"#"}>Know more</Link>
                                        </div>
                                    </li>
                                    <li className="col-sm-3">
                                        <div className="card">
                                            <figure>
                                                <img src="./media/images/categories8.jpg" className="img-fluid" alt="Mass Communication" />
                                            </figure>
                                            <h3>Mass Communication</h3>
                                            <strong>30 courses</strong>
                                            <Link to={"#"}>Know more</Link>
                                        </div>
                                    </li>
                                </ul>
                            </Carousel.Item>
                        </Carousel>
                        <span className="pink-circle2" data-aos="fade-right"></span>
                        <span className="pink-circle3" data-aos="fade-left"></span>
                    </div>
                </div>
            </div>
        </section>
    )
}
   
export default RecruitersLooking;