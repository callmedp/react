import React, {useEffect, useState} from 'react';
import { Link } from 'react-router-dom';
// import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
// import Button from 'react-bootstrap/Button';
import '../../../SkillPage/CoursesTray/courses.scss'
import './jobsUpskills.scss';
import { useSelector } from 'react-redux';
import Loader from '../../../../Common/Loader/loader';
import { fetchFindRightJobsData, fetchUpskillYourselfData } from 'store/UserIntentPage/actions';
import { useDispatch } from 'react-redux';
import { fetchPopularServices } from 'store/CataloguePage/actions';
import { startJobsUpskillsLoader, stopJobsUpskillsLoader } from 'store/Loader/actions';
import { siteDomain } from 'utils/domains';

const JobsUpskills = (props) => {
    // const [key, setKey] = useState('categories1');
    const dispatch = useDispatch();
    const { jobsUpskillsLoader } = useSelector(store => store?.loader);
    const findJobsData = useSelector(store => store.findRightJob?.jobsList);
    const {course_data, page, recommended_course_ids} = useSelector(store => store.upskillYourself.upskillList);
    const params = new URLSearchParams(props.location.search);

    const starRatings = (star, index) => {
        return (star === '*' ? <em className="micon-fullstar" key={index}></em> : star === '+'
            ? <em className="micon-halfstar" key={index}></em> : <em className="micon-blankstar" key={index}></em>
        )
    }

    const [setOpen, setCourseOpen] = useState(false);
    const openCourseDetails = (id) => setCourseOpen(setOpen === id ? false : 'upSkill'+id);

    const [selectTab, tabSelected] = useState('tab1');
    const openSelectedTab = (id) => tabSelected(id);

    useEffect(() => {
        resultApiFunc();
    }, []);

    const resultApiFunc = async() => {
        const data = {
            'job': params.get('job_title'),
            'location': params.get('loc'), //Is document work on SSR?
            'skills': params.get('skill'),
            'experience': params.get('minexp')
        };

        // api hit for jobs for you
        if (!findJobsData?.results){
        dispatch(startJobsUpskillsLoader());
            await new Promise((resolve) => dispatch(fetchFindRightJobsData({ data, resolve })));
        dispatch(stopJobsUpskillsLoader());
        }
        
        
    }

    function handleUpskillData(tab) {
        const dataUpskill = {
            'preferred_role': params.get('job_title'),
            'skills': params.get('skills'),
            'experience': params.get('experience')
        };
        // api hit for upskill yourself
        if(!course_data) {
        dispatch(startJobsUpskillsLoader());
        new Promise((resolve) => dispatch(fetchUpskillYourselfData({ dataUpskill, resolve })));
        dispatch(stopJobsUpskillsLoader());
        }
        openSelectedTab('tab2');
    }

    return (
        <section className="m-container mt-0 mb-0 pl-0 pr-0">
            { jobsUpskillsLoader ? <Loader /> : ''}
            <div className="m-ui-main col">
                <div className="d-flex align-items-center">
                    <div className="m-ui-steps">
                        <Link className="m-completed" to={"#"}>1</Link>
                        <Link className="m-completed" to={"#"}>2</Link>
                        <Link className="m-current" to={"#"}>3</Link>
                    </div>
                    <Link className="btn-blue-outline m-back-goal-btn" to={"/user-intent/"}>Back to goal</Link>
                </div>
                <div className="m-jobs-upskills mt-20">
                    <div className="m-tabset-intent">
                        <input checked={selectTab === 'tab1'} onClick={() => openSelectedTab('tab1')} type="radio" name="tabset" id="tab1" aria-controls="Jobs for you" />
                        <label htmlFor="tab1">Jobs for you</label>

                        <input checked={selectTab === 'tab2'} onClick={() => handleUpskillData('tab2')} type="radio" name="tabset" id="tab2" aria-controls="Upskill yourself" />
                        <label htmlFor="tab2">Upskill yourself</label>

                        <div className="tab-panels">
                            <div id="tab1" className="tab-panel">
                                <ul className="m-shine-courses-listing mt-20">
                                    {findJobsData?.results?.map((jData,indx) => {
                                        return(
                                            <li key={indx}>
                                                <div className="course">
                                                    <div className="d-flex p-15">
                                                        <div className="course__content">
                                                            {/* <span className="hot-badge">
                                                                <figure className="icon-hot"></figure> Hot
                                                            </span> */}
                                                            <h3 className="heading3">
                                                                <Link to={"#"}>{jData.jJT}</Link>
                                                            </h3>
                                                            <strong>{jData.jCName}</strong>
                                                            <div className="d-flex">
                                                                <ul>
                                                                    <li>{jData.jExp}</li>
                                                                    <li>{jData.jLoc.join(',')}</li>
                                                                    <li>{jData.jKwd}</li>
                                                                </ul>
                                                                <div className="m-price-date">
                                                                    <a href={`${siteDomain}/${jData.jSlug}`} className="btn-blue-outline mb-10">Apply</a>
                                                                    <span>{new Date(jData.jPDate).toLocaleDateString()}</span> 
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </li>
                                        )
                                    })}
                                </ul>
                            </div>
                            <div id="tab2" className="tab-panel">
                                <div className="m-courses mt-20">
                                    {course_data?.map((cour, indx) => {
                                        return (
                                            <div className="m-card" key={indx}>
                                                <div className="m-card__heading">
                                                    {cour.tags === 2 && <span className="m-flag-yellow">NEW</span>}
                                                    {cour.tags === 1 && <span className="m-flag-yellow">BESTSELLER</span>}
                                                    <figure>
                                                        <img src={cour.imgUrl} alt={cour.imgAlt} />
                                                    </figure>
                                                    
                                                    <h3 className="m-heading3">
                                                        <Link to={cour.url}>{cour.name}</Link>
                                                    </h3>
                                                </div>
                                                <div className="m-card__box">
                                                    <div className="m-card__rating">
                                                        <span className="mr-10">By {cour.providerName}</span>
                                                        <span className="m-rating">
                                                            {cour?.stars?.map((star, index) => starRatings(star, index))}
                                                            <span>{cour?.rating}</span>
                                                        </span>
                                                    </div>
                                                    <div className="m-card__duration-mode">
                                                        { cour?.duration > 0 ? <span>Duration:<strong>{cour?.duration}  |  </strong></span> : '' } 
                                                        { cour?.mode ? <span>Mode: <strong>{cour?.mode}</strong></span> : ''}
                                                        { cour?.jobsAvailable > 0 ? <span className="d-block"><strong>{cour?.jobsAvailable}</strong> Jobs available</span> : ''}
                                                    </div>
                                                    <div className="m-card__price">
                                                        <strong>{cour.price}/-</strong> 
                                                        {setOpen !== ('upSkill' + cour.id) && <span id={'upSk' + cour.id} className="m-view-more" onClick={() => openCourseDetails(cour.id)}>View more</span>}
                                                    </div>
                                                </div>

                                                {setOpen === ('upSkill' + cour.id) && 
                                                    <div className="m-card__popover" htmlFor={'upSk' + cour.id}>
                                                        <p className="m-type">
                                                            {cour?.type ? <span>Type: <strong>{cour?.type}</strong>  |  </span> : ''}
                                                            {cour?.level ? <span><strong>Course level:</strong>{cour?.level}</span> : ''}
                                                            {cour?.jobsAvailable > 0 ? <span><strong>{cour.jobsAvailable}</strong> Jobs available</span> : ''}
                                                        </p>
                                                        {cour.about ? 
                                                            <p>
                                                                <strong>About</strong>
                                                                {cour.about}
                                                            </p>
                                                            :''
                                                        }
                                                        {cour?.skillList ?
                                                            <p>
                                                                <strong>Skills you gain</strong>
                                                                {cour?.skillList.join(' | ')}
                                                            </p>
                                                            : ''
                                                        }
                                                        {cour?.highlights &&
                                                            <p>
                                                                <strong>Highlights</strong>
                                                                <ul>
                                                                    {
                                                                        cour?.highlights?.slice(0, 2)?.map((value, index) => {
                                                                            return (
                                                                                <li key={index} dangerouslySetInnerHTML={{__html: value}}></li>
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
                                    })}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="m-courses-feedback">
                    <strong>Are these courses recommendation relevant to your profile?</strong>
                    <span className="mt-15">
                        <Link className="btn-blue-outline" to={'#'}>Yes</Link>
                        <Link className="btn-blue-outline" to={'#'}>No</Link>
                    </span>
                </div>
            </div>
        </section>
    )
}

export default JobsUpskills;