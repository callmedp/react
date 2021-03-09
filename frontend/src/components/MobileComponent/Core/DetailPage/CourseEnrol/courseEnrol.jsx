import React from 'react';
import './courseEnrol.scss';
import {Link} from 'react-router-dom';


const CourseEnrol = (props) => {
    return (
        <section className="m-container mt-80n mb-0 pb-0">
            <div className="m-course-enrol">
                <div className="m-course-enrol__mode">
                    <form>
                        <strong>Mode</strong> <label><input type="radio" value="" checked /> Online</label> 
                        <label><input type="radio" value="" /> Class room</label>
                    </form>
                </div>
                <div className="m-course-enrol__price">
                    <strong className="mt-20 mb-10">3,499/- <del>5,499/-</del></strong>
                    <Link to={"#"} className="btn btn-secondary mt-10 ml-auto">Enroll now</Link>
                </div>
                <div className="m-course-enrol__offer lightblue-bg2">
                    <strong className="mt-10 mb-5">Offers</strong>
                    <ul className="pb-0">
                        <li><figure className="micon-offer-pay"></figure> Buy now & <strong>pay within 14 days using ePayLater</strong> </li>
                        <li><figure className="micon-offer-test"></figure> Take <strong>free practice test</strong> to enhance your skill</li>
                        <li><figure className="micon-offer-badge"></figure> <strong>Get badging</strong> on your Shine profile</li>
                        <li><figure className="micon-offer-global"></figure> <strong>Global</strong> Education providers</li>
                    </ul>
                    <Link to={"#"}>+2 more</Link>
                </div>
            </div>
        </section>
    )
}

export default CourseEnrol;