import React, { useState } from 'react'
import { Link } from 'react-router-dom';
import { siteDomain } from 'utils/domains';

const CourseLisiting = (props) => {

    const { courseList } = props;
    const [toggleMore, setToggleMore] = useState(false)
    const regex = /<(.|\n)*?>/g
    const noOfWords = 330

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+'
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    const handleToggleMore = (event, idx) => {
        event.preventDefault();
        setToggleMore(state => state === idx ? false : idx);
    }

    // const goToUrl = (event, url) => {
    //     event.preventDefault();
    //     return window.location.href = `${siteDomain}${url}`;
    // }

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
                                        {course?.tags === 1 && <span className="flag-red">BESTSELLER</span>}
                                        {course?.tags === 2 && <span className="flag-blue">NEW</span>}
                                        <h3 className="heading3">
                                            <a>{course.name}</a>
                                        </h3>
                                        <span className="mr-10">By {course.providerName}</span>
                                        <span className="rating">
                                            {course.stars?.map((star, index) => starRatings(star, index))}
                                            <span className="ml-10">{course.rating}/5</span>
                                        </span>
                                        <p className="course__duration-mode mt-20">
                                            {course.duration ? <>Duration: <strong>{course.duration}</strong></> : ''}  {course.duration && course.mode ? '|' : ''}  {course.mode ? <>Mode: <strong>{course.mode}</strong></> :
                                                    ''}  {course.mode && course.jobsAvailable ? '|' : ''}  {course.jobsAvailable ? <strong>{+course.jobsAvailable > 1 ? course.jobsAvailable + ' Jobs available' :
                                                        course.jobsAvailable + ' Job available'}</strong> : ''}
                                        </p>
                                    </div>
                                    <div className="course__price-enrol mr-20 mt-20">
                                        <strong>{course.price}/-</strong>
                                        <a href={`${siteDomain}${course.url}`} class="btn btn-secondary mt-10">Enroll now</a>
                                    </div>
                                </div>
                                <div className="course__bottom">
                                    <div className="d-flex">
                                        <strong>Key Highlights</strong>
                                        <ul>
                                            <li>Earn a certificate after completion</li>
                                            <li>Get Access on mobile </li>
                                        </ul>
                                        <Link onClick={(e) => handleToggleMore(e, index)} className="more-popover ml-30">{ toggleMore === index ? ' Less ' : ' More '}<figure className="icon-arrow-down-sm"></figure></Link>
                                        { course.brochure ? <a onClick={(e) => e.preventDefault()} href={course.brochure} className="icon-pdf ml-auto"></a> : ''}
                                    </div>
                                    {
                                        toggleMore === index ? <div className="course-popover">
                                            <p className="type"> {!!course.type ? <>Type: <strong>{course.type}</strong></> : ''}{!!course.type && !!course.level ? ' | ' : ''}{!!course.level ? <>Course level: <strong>{course.level}</strong></> : ''} </p>
                                            <p>
                                                <strong>About</strong>
                                                {
                                                    course.u_desc ?
                                                        <div dangerouslySetInnerHTML={{ __html: (course.u_desc?.replace(regex, '').slice(noOfWords)?.length ? (course.u_desc?.replace(regex, '').slice(0, noOfWords) + '...') : course.u_desc?.replace(regex, '').slice(0, noOfWords)) }}></div> :
                                                        <div dangerouslySetInnerHTML={{ __html: (course.about?.replace(regex, '').slice(noOfWords)?.length ? (course.about?.replace(regex, '').slice(0, noOfWords) + '...') : course.about?.replace(regex, '').slice(0, noOfWords)) }}></div>

                                                }
                                            </p>
                                            {course.skillList?.length ?
                                                <p>
                                                    <strong>Skills you gain</strong>
                                                    {
                                                        course.skillList?.slice(0, 10)?.map((skill, index) => {
                                                            return (
                                                                <React.Fragment key={index}>
                                                                    {skill}
                                                                    {index === course.skillList?.slice(0, 10).length - 1 ? ' ' : '  |  '}
                                                                    {(course.skillList?.slice(0, 10)?.pop() == skill && course.skillList?.slice(10)?.length) ? '& Many More..' : ''}
                                                                </React.Fragment>
                                                            )
                                                        })
                                                    }
                                                </p> : ''
                                            }
                                            {
                                                course.highlights?.length ?
                                                    <>
                                                        <strong>Highlights</strong>
                                                        <ul>
                                                            {
                                                                course.highlights?.slice(0, 4)?.map((value, index) => {
                                                                    return (
                                                                        <li key={index} dangerouslySetInnerHTML={{ __html: value }}></li>
                                                                    )
                                                                })
                                                            }
                                                        </ul>
                                                    </> : ''
                                            }
                                        </div> : ''
                                    }
                                </div>
                            </div>
                        </li>
                    )
                })
            }
        </ul>
    )
}

export default CourseLisiting;
