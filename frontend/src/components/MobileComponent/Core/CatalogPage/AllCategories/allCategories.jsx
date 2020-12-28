import React, {useState} from 'react';
import './allCategories.scss';
import { Link } from 'react-router-dom';

   
const AllCategories = (props) => {
    return(
        <section id="m-all-categories" className="m-container m-lightblue-bg mt-0 mb-0" data-aos="fade-up">
            <div className="m-all-category">
                <h2 className="m-heading2 text-center">All categories</h2>
                <ul className="m-all-category__list">
                    <li>
                        <div className="m-card">
                            <figure>
                                <img src="./media/images/mobile/categories1.jpg" className="img-fluid" alt="Personal Development" />
                            </figure>
                            <h3>Personal Development</h3>
                            <Link to={"#"}>View courses</Link>
                        </div>
                    </li>
                    <li>
                        <div className="m-card">
                            <figure>
                                <img src="./media/images/mobile/categories2.jpg" className="img-fluid" alt="Information Technology" />
                            </figure>
                            <h3>Information Technology</h3>
                            <Link to={"#"}>View courses</Link>
                        </div>
                    </li>
                    <li>
                        <div className="m-card">
                            <figure>
                                <img src="./media/images/mobile/categories3.jpg" className="img-fluid" alt="Sales and Marketing" />
                            </figure>
                            <h3>Sales and Marketing</h3>
                            <Link to={"#"}>View courses</Link>
                        </div>
                    </li>
                    <li>
                        <div className="m-card">
                            <figure>
                                <img src="./media/images/mobile/categories4.jpg" className="img-fluid" alt="Human Resources (HR)" />
                            </figure>
                            <h3>Human Resources (HR)</h3>
                            <Link to={"#"}>View courses</Link>
                        </div>
                    </li>
                    <li>
                        <div className="m-card">
                            <figure>
                                <img src="./media/images/mobile/categories5.jpg" className="img-fluid" alt="Management" />
                            </figure>
                            <h3>Management</h3>
                            <Link to={"#"}>View courses</Link>
                        </div>
                    </li>
                    <li>
                        <div className="m-card">
                            <figure>
                                <img src="./media/images/mobile/categories6.jpg" className="img-fluid" alt="Law" />
                            </figure>
                            <h3>Law</h3>
                            <Link to={"#"}>View courses</Link>
                        </div>
                    </li>
                    <li>
                        <div className="m-card">
                            <figure>
                                <img src="./media/images/mobile/categories7.jpg" className="img-fluid" alt="Operation Management" />
                            </figure>
                            <h3>Operation Management</h3>
                            <Link to={"#"}>View courses</Link>
                        </div>
                    </li>
                    <li>
                        <div className="m-card">
                            <figure>
                                <img src="./media/images/mobile/categories8.jpg" className="img-fluid" alt="Mass Communication" />
                            </figure>
                            <h3>Mass Communication</h3>
                            <Link to={"#"}>View courses</Link>
                        </div>
                    </li>
                </ul>
            </div>
        </section>
    )
}
   
export default AllCategories;