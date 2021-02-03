import React from 'react'

const popularCourse = (props) => {

    return (
        <li className="col">
        <div className="card">
            <div className="card__heading">
                <figure>
                    <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                </figure>
                <h3 className="heading3">
                    <a to={"#"}>Digital Marketing & Email Marketing Training Course</a>
                </h3>
            </div>
            <div className="card__box">
                <div className="card__rating">
                <span className="rating">
                    <em className="icon-fullstar"></em>
                    <em className="icon-fullstar"></em>
                    <em className="icon-fullstar"></em>
                    <em className="icon-fullstar"></em>
                    <em className="icon-blankstar"></em>
                    <span>4/5</span>
                </span>
                <span className="mode">Online</span>
                </div>
                <div className="card__price mt-10">
                    <strong>12999/-</strong> 
                </div>
            </div>
        </div>
    </li>
    )
}

export default popularCourse;
