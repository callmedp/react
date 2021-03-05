import React, {useState} from 'react'
import { Link } from 'react-router-dom';
import { siteDomain } from 'utils/domains';
 
const CourseLisiting = (props) => {

    const { courseList } = props;
    const [setOpen, setCourseOpen] = useState(false);
    const openCourseDetails = (event, id) => { event.preventDefault(); setCourseOpen(setOpen === id ? false : 'upSkill'+id) };
    const regex = /<[^>]*>/g;
    const noOfWords = 100;

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="icon-fullstar" key={index}></em> : star === '+'
            ? <em className="icon-halfstar" key={index}></em> : <em className="icon-blankstar" key={index}></em>
        )
    }

    const getDurationMode = (duration, mode, d_type) => {
        return (
            <div className="m-card__duration-mode">
            {
                duration && mode ? <> Duration: <strong>{duration} {d_type}</strong> | Mode: <strong>{mode.split(" ")[0]}</strong> </> :
                duration ? <> Duration: <strong>{duration} {d_type}</strong> </> :
                mode ? <> Mode: <strong>{mode.split(" ")[0]}</strong> </> : <>&nbsp;</>
            }
            </div>
        )   
    }

    const goToUrl = (event, url) => {
        event.preventDefault();
        return window.location.href = `${siteDomain}${url}`;
    }

    return (
        <ul className="courses-listing ml-10n mt-30">
            {
                courseList?.map((course, index) => {
                    return (
                        <div className="m-card" key={index} onClick={(e) => goToUrl(e, course.url)}>
                            <div className="m-card__heading">
                                {course?.tags === 1 && <span className="m-flag-yellow">BESTSELLER</span>}
                                {course?.tags === 2 && <span className="m-flag-blue">NEW</span>}
                                <figure>
                                    <img src={course?.imgUrl} alt={course?.imgAlt} />
                                </figure>
                                
                                <h3 className="m-heading3">
                                    <a>{course?.name}</a>
                                </h3>
                            </div>
                            <div className="m-card__box">
                                <div className="m-card__rating">
                                    <span className="mr-10">By {course?.providerName}</span>
                                    <span className="m-rating">
                                        {course?.stars?.map((star, indx) => starRatings(star, indx))}
                                        <span>{course?.rating}/5</span>
                                    </span>
                                </div>
                                    {course?.test_duration ? getDurationMode(course?.test_duration, course?.mode, 'minutes') : getDurationMode(course?.duration, course?.mode, 'days')}
                                <div className="m-card__price">
                                    <strong>{course?.price}/-</strong> 
                                    {setOpen !== ('upSkill' + course?.id) && <span id={'upSk' + course?.id} className="m-view-more text-right" onClick={(e) => openCourseDetails(e, course?.id)}>View more</span>}
                                </div>
                            </div>

                            {setOpen === ('upSkill' + course?.id) && 
                                <div className="m-card__popover" htmlFor={'upSk' + course?.id}>
                                    <p className="m-type">
                                        {
                                            (course?.type && course?.level) ? 
                                                <> Type: <strong>{course?.type?.length > 12 ? course?.type?.slice(0,12)+'...' : course?.type}</strong>  |  Course level: <strong>{course?.level}</strong> </>
                                                :
                                                course?.type ? 
                                                <> Type: <strong>{course?.type?.length > 12 ? course?.type?.slice(0,12)+'...' : course?.type}</strong> </> 
                                                : 
                                                course?.level ? 
                                                <> Course level: <strong>{course?.level}</strong> </> : ''
                                        }
                                        <br />
                                        <strong> {course?.jobsAvailable}</strong> Jobs available
                                    </p>
                                    <p>
                                        <strong>About</strong>
                                        {
                                            course?.u_desc ? 
                                            <div dangerouslySetInnerHTML={{__html: (course?.u_desc?.replace(regex, '').slice(noOfWords)?.length ? (course?.u_desc?.replace(regex, '').slice(0,noOfWords)+'...') : course?.u_desc?.replace(regex, '').slice(0,noOfWords))}}></div> :
                                            <div dangerouslySetInnerHTML={{__html: (course?.about?.replace(regex, '').slice(noOfWords)?.length ? (course?.about?.replace(regex, '').slice(0,noOfWords)+'...') : course?.about?.replace(regex, '').slice(0,noOfWords))}}></div> 
                                        }
                                    </p>
                                    {course?.skillList ?
                                        <p>
                                            { 
                                                course?.skillList && 
                                                <>
                                                    <strong>Skills you gain</strong> 
                                                    { 
                                                        course?.skillList?.slice(0, 5)?.map((skill, index) =>{
                                                            return ( 
                                                                <React.Fragment key={index}>
                                                                    {skill}
                                                                    {index === course?.skillList?.slice(0, 5).length-1 ? ' ' : '  |  '}
                                                                    {(course?.skillList?.slice(0, 5)?.pop() == skill && course?.skillList?.slice(5)?.length) ? '& Many More..' : ''}
                                                                </React.Fragment>
                                                            )
                                                        })
                                                    }
                                                </>
                                            }
                                        </p>
                                        : ''
                                    }
                                    <p>
                                        {
                                            course?.highlights?.length ? 
                                            <>
                                                <strong>Highlights</strong>
                                                <ul>
                                                    {
                                                        course?.highlights?.slice(0, 2)?.map((value, index) =>{
                                                            return (
                                                                <li key={index} dangerouslySetInnerHTML={{__html: value}}></li>
                                                            )
                                                        })
                                                    }
                                                </ul>
                                            </> : ''
                                        }
                                    </p>
                                    <p className="d-flex align-items-center">
                                        <a className="btn-yellow" role="button" href={`${siteDomain}${course?.url}`}>Enroll now</a>
                                        {course?.brochure && <Link to={"#"} className="micon-pdf ml-auto"></Link>}
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
