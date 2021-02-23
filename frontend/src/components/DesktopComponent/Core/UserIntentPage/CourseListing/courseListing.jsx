import React from 'react'
import { Link } from 'react-router-dom';
import { siteDomain } from 'utils/domains';
 
const CourseLisiting = (props) => {

    const { courseList } = props;

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+'
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    return (
        <ul className="courses-listing ml-10n mt-30">
            {
                courseList?.map((course, index) => {
                    return (
                        <li className="col" key={index}>
                            <div className="course">
                                <div className="d-flex align-items-center">
                                    <figure className="course__icon">
                                        <img src={course.imgUrl} alt={course.imgAlt} />
                                    </figure>
                                    <div className="course__content">
                                        <span className="flag-red">BESTSELLER</span>
                                        <h3 className="heading3">
                                            <a href={`${siteDomain}${course.url}`}>{course.name}</a>
                                        </h3>
                                        <span className="mr-10">By {course.providerName}</span>
                                        <span className="rating">
                                        {course.stars?.map((star, index) => starRatings(star, index))}
                                            <span className="ml-10">{course.rating}/5</span>
                                        </span>
                                        <p className="course__duration-mode mt-20">
                                            {course.duration ? <>Duration: <strong>{ +course.duration > 1 ? course.duration+" days":
                                             course.duration+" day"}</strong></>: ''}  { course.duration && course.mode ? '|': ''}  { course.mode ? <>Mode: <strong>{course.mode}</strong></>:
                                             ''}  { course.mode && course.jobsAvailable ? '|' : ''}  { course.jobsAvailable ? <strong>{ +course.jobsAvailable > 1 ? course.jobsAvailable+' Jobs available':
                                              course.jobsAvailable+' Job available'}</strong>: '' }
                                                            </p>
                                    </div>
                                    <div className="course__price-enrol mr-20 mt-20">
                                        <strong>{course.price}/-</strong>
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
                                        <Link onClick={(e) => e.preventDefault()} className="more-popover ml-30">More <figure className="icon-arrow-down-sm"></figure></Link>
                                        <Link onClick={(e) => e.preventDefault()}className="icon-pdf ml-auto"></Link>
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
