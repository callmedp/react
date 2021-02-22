import React from 'react'
import { Link } from 'react-router-dom';

const CourseLisiting = (props) => {

    const { courseList } = props;

    return (
        <ul className="courses-listing ml-10n mt-30">
            {
                courseList?.map((course, index) => {
                    return (
                        <li className="col" key={index}>
                            <div className="course">
                                <div className="d-flex align-items-center">
                                    <figure className="course__icon">
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <div className="course__content">
                                        <span className="flag-red">BESTSELLER</span>
                                        <h3 className="heading3">
                                            <Link to={"#"}>Digital Marketing Training Course</Link>
                                        </h3>
                                        <span className="mr-10">By ERB</span>
                                        <span className="rating">
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-fullstar"></em>
                                            <em className="icon-blankstar"></em>
                                            <span className="ml-10">4/5</span>
                                        </span>
                                        <p className="course__duration-mode mt-20">
                                            Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong>  |   <strong>2819</strong> Jobs available
                                                            </p>
                                    </div>
                                    <div className="course__price-enrol mr-20 mt-20">
                                        <strong>12999/-</strong>
                                        <Link to={"#"} class="btn btn-secondary mt-10">Enroll now</Link>
                                    </div>
                                </div>
                                <div className="course__bottom">
                                    <div className="d-flex">
                                        <strong>Key Highlights</strong>
                                        <ul>
                                            <li>Earn a certificate after completion</li>
                                            <li>Get Access on mobile </li>
                                        </ul>
                                        <Link to={"#"} className="more-popover ml-30">More <figure className="icon-arrow-down-sm"></figure></Link>
                                        <Link to={"#"} className="icon-pdf ml-auto"></Link>
                                    </div>
                                </div>
                            </div>
                        </li>
                    )
                })
            }
        </ul>
    )
}

export default CourseLisiting
