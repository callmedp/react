import React from 'react';
import { Link } from 'react-router-dom';
import './popularCourses.scss'

const PopularCourses = (props) => {
    return (
        <div className="popular-courses mt-40">
            <h2 className="heading2">Popular Courses</h2>
            <ul className="popular-courses__list">
                <li>
                    <figure>
                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                    </figure>
                    <div className="links">
                        <Link to={"#"}>Email Marketing Master Training Course</Link>
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
                </li>
                <li>
                    <figure>
                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                    </figure>
                    <div className="links">
                        <Link to={"#"}>Email Marketing Master Training Course</Link>
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
                </li>
                <li>
                    <figure>
                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                    </figure>
                    <div className="links">
                        <Link to={"#"}>Email Marketing Master Training Course</Link>
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
                </li>
            </ul>
            <Link className="view-all" to={"#"}>View all courses</Link>
        </div>
    )
}

export default PopularCourses;