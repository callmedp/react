import React, { Component } from "react";
import { Link } from 'react-router-dom';
import '../CoursesTray/courses.scss';

const PopularCourses = (props) => {
    return (
    <section className="m-container m-courses mt-0 mb-0 pb-0">
        <div className="d-flex">
            <h2 className="m-heading2 mb-10">Popular Courses</h2>
            <Link className="ml-auto m-view-course" to={"#"}>View all courses</Link>
        </div>
        <div className="d-flex m-popular-courses">
            <div className="m-col">
                <div className="m-card">
                    <div className="m-card__heading">
                        <figure>
                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                        </figure>
                        <h3 className="m-heading3">
                            <Link to={"#"}>Digital Marketing Training Course</Link>
                        </h3>
                    </div>
                    <div className="m-card__box">
                        <div className="m-card__rating">
                        <span className="mr-10">By Simplilearn</span>
                        <span className="m-rating">
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-blankstar"></em>
                            <span>4/5</span>
                        </span>
                        </div>
                    </div>
                </div>
            </div>
            <div className="m-col">
                <div className="m-card">
                    <div className="m-card__heading">
                        <figure>
                            <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                        </figure>
                        <h3 className="m-heading3">
                            <Link to={"#"}>Email Marketing Master Training</Link>
                        </h3>
                    </div>
                    <div className="m-card__box">
                        <div className="m-card__rating">
                        <span className="mr-10">By Simplilearn</span>
                        <span className="m-rating">
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-fullstar"></em>
                            <em className="micon-blankstar"></em>
                            <span>4/5</span>
                        </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        

    </section>
    );
  }

export default PopularCourses;