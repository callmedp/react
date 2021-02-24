import React, {useState} from 'react'
import { Link } from 'react-router-dom';
 
const CourseLisiting = (props) => {

    const { courseList } = props;
    const [setOpen, setCourseOpen] = useState(false);
    const openCourseDetails = (id) => setCourseOpen(setOpen === id ? false : 'upSkill'+id);

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
                        <div className="m-card" key={index}>
                            <div className="m-card__heading">
                                {course?.tags === 1 && <span className="m-flag-yellow">BESTSELLER</span>}
                                {course?.tags === 2 && <span className="m-flag-blue">NEW</span>}
                                <figure>
                                    <img src={course?.imgUrl} alt={course?.imgAlt} />
                                </figure>
                                
                                <h3 className="m-heading3">
                                    <Link to={course?.url}>{course?.name}</Link>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating">
                                    <span className="mr-10">By {course?.providerName}</span>
                                    <span className="m-rating">
                                        {course?.stars?.map((star, indx) => starRatings(star, indx))}
                                        <span>{course?.rating}</span>
                                    </span>
                                </div>
                                <div className="m-card__duration-mode">
                                    { course?.duration > 0 ? <span>Duration:<strong>{course?.duration}  |  </strong></span> : '' } 
                                    { course?.mode ? <span>Mode: <strong>{course?.mode}</strong></span> : ''}
                                    { course?.jobsAvailable > 0 ? <span className="d-block"><strong>{course?.jobsAvailable}</strong> Jobs available</span> : ''}
                                </div>
                                <div className="m-card__price">
                                    <strong>{course?.price}/-</strong> 
                                    {setOpen !== ('upSkill' + course?.id) && <span id={'upSk' + course?.id} className="m-view-more text-right" onClick={() => openCourseDetails(course?.id)}>View more</span>}
                                </div>
                            </div>

                            {setOpen === ('upSkill' + course?.id) && 
                                <div className="m-card__popover" htmlFor={'upSk' + course?.id}>
                                    <p className="m-type">
                                        {course?.type ? <span>Type: <strong>{course?.type}</strong>  |  </span> : ''}
                                        {course?.level ? <span><strong>Course level:</strong>{course?.level}</span> : ''}
                                        {course?.jobsAvailable > 0 ? <span><strong>{course?.jobsAvailable}</strong> Jobs available</span> : ''}
                                    </p>
                                    {course?.about ? 
                                        <p>
                                            <strong>About</strong>
                                            {course?.about}
                                        </p>
                                        :''
                                    }
                                    {course?.skillList ?
                                        <p>
                                            <strong>Skills you gain</strong>
                                            {course?.skillList.join(' | ')}
                                        </p>
                                        : ''
                                    }
                                    {course?.highlights &&
                                        <p>
                                            <strong>Highlights</strong>
                                            <ul>
                                                {
                                                    course?.highlights?.slice(0, 2)?.map((value, ind) => {
                                                        return (
                                                            <li key={ind} dangerouslySetInnerHTML={{__html: value}}></li>
                                                        )
                                                    })
                                                }
                                            </ul>
                                        </p>
                                    }
                                    <p className="d-flex align-items-center">
                                        <button type="submit" className="btn-yellow" role="button">Enroll now</button>
                                        {/* <Link to={"#"} className="micon-pdf ml-auto"></Link> */}
                                    </p>
                                    <span to={"#"} className="m-view-less d-block text-right" onClick={() => openCourseDetails(false)}>View less</span>
                                </div>
                            }
                        </div>
                    )
                })
            }
        </ul>
    )
}

export default CourseLisiting
