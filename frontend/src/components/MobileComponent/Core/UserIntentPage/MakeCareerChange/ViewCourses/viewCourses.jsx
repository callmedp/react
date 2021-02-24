import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import 'slick-carousel/slick/slick.css';
import '../../../SkillPage/CoursesTray/courses.scss'
import '../../FindRightJob/JobsUpskills/jobsUpskills.scss';
import CourseLisiting from '../../IntentUtil/courseListing';
import { useDispatch, useSelector } from 'react-redux';
import queryString from "query-string";
import { startCareerChangeLoader, stopCareerChangeLoader } from 'store/Loader/actions/index';
import { fetchUpskillYourselfData } from 'store/UserIntentPage/actions';
import Loader from '../../../../Common/Loader/loader';
import { showSwal } from 'utils/swal';

const ViewCourses = (props) => {
    // const [key, setKey] = useState('categories1');
    const { history } = props;
    const dispatch = useDispatch();
    const params = queryString.parse(props.location.search);
    const [currentCoursePage, setCoursePage] = useState(1);
    let currentPage = 1;
    const data = {
        job : params?.job,
        experience : params?.experience,
        skills : params?.skills,
        intent : params?.intent ? params.intent : 1,
        page : params?.page ? params.page : 1
    };

    const [selectTab, tabSelected] = useState('tab1');
    const openSelectedTab = (id) => tabSelected(id);

    useEffect(() => {
        handleEffects();
    }, []);



    const handleUpskillData = async(tab) => {
        const dataUpskill = `?preferred_role=${data.job}&experience=${data.experience}&skills=${data.skills|| ''}&intent=${data.intent}&page=${currentPage}`;

        dispatch(startCareerChangeLoader());

        // api hit for upskill yourself
        try {
            await new Promise((resolve, reject) => dispatch(fetchUpskillYourselfData({ dataUpskill, resolve, reject })));
            openSelectedTab(tab);
        }
        catch(e) {
            showSwal('error', 'Something went wrong! Try Again');
            openSelectedTab('tab1');
        }
        dispatch(stopCareerChangeLoader());
    }

    const { course_data, page } = useSelector(store => store.upskillYourself)
    const { jobsUpSkillsLoader } = useSelector(store => store.loader);

    const loadMoreCourses = (curr_page) => {
        currentPage = curr_page+1;
        handleUpskillData('tab2');
    }

    const handleEffects = async () => {
        try {   
                await new Promise((resolve, reject) => dispatch(fetchUpskillYourselfData({ data, resolve, reject })));               
        } catch (error) {

            if (error?.status == 404) {
                history.push('/404');
            }
        }
    };

    return (
        <>
        { jobsUpSkillsLoader ? <Loader /> : '' }
            <section className="m-container mt-0 mb-0 pl-0 pr-0">
                <div className="m-ui-main col">
                    <div className="d-flex align-items-center">
                        <div className="m-ui-steps">
                            <Link className="m-completed" to={"#"}>1</Link>
                            <Link className="m-completed" to={"#"}>2</Link>
                            <Link className="m-current" to={"#"}>3</Link>
                        </div>
                        <Link className="btn-blue-outline m-back-goal-btn" to={"/user-intent/"}>Back to goal</Link>
                    </div>
                    <h2 className="m-heading3 mt-20">Here’s how you can make a new career</h2>
                    <div className="m-jobs-upskills mt-20">
                        <div className="m-courses mt-20">
                            <CourseLisiting courseList={course_data} />
                            {/* <div className="m-card">
                                <div className="m-card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="m-heading3">
                                        <Link to={"#"}>Digital Marketing Training Course Programme</Link>
                                    </h3>
                                </div>
                                <div className="m-card__box">
                                    <div className="m-card__rating">
                                    <span className="mr-10">By ERB</span>
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="m-card__duration-mode">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong> <span className="d-block"><strong>2819</strong> Jobs available</span>
                                    </div>
                                    <div className="m-card__price">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="m-view-more">View more</Link>
                                    </div>
                                </div>
                            </div>
                            <div className="m-card">
                                <div className="m-card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="m-heading3">
                                        <Link to={"#"}>Email Marketing Master Training Course</Link>
                                    </h3>
                                </div>
                                <div className="m-card__box">
                                    <div className="m-card__rating">
                                    <span className="mr-10">By ERB</span>
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="m-card__duration-mode">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong> <span className="d-block"><strong>2819</strong> Jobs available</span>
                                    </div>
                                    <div className="m-card__price">
                                        <strong>12999/-</strong> 
                                    </div>
                                </div>
                                <div className="m-card__popover">
                                    <p className="m-type">Type: <strong>Certification</strong>  |   <strong>Course level:</strong> Intermediate 
                                        <strong> 2819</strong> Jobs available
                                    </p>
                                    <p>
                                        <strong>About</strong>
                                        This Course is intended for professionals and graduates wanting to excel in their chosen areas.
                                    </p>
                                    <p>
                                        <strong>Skills you gain</strong>
                                        Content Marketing  |  Email Marketing  |  Adwords Social Media  |  SEO  |  Copywriting  |  Digital Marketing 
                                    </p>
                                    <p>
                                        <strong>Highlights</strong>
                                        <ul>
                                            <li>Anytime and anywhere access</li>
                                            <li>Become a part of Job centre</li>
                                            <li>Lifetime course access</li>
                                            <li>Access to online e-learning</li>
                                        </ul>
                                    </p>
                                    <p className="d-flex align-items-center">
                                        <button type="submit" className="btn-yellow" role="button">Enroll now</button>
                                        <Link to={"#"} className="micon-pdf ml-auto"></Link>
                                    </p>
                                    <Link to={"#"} className="m-view-less d-block text-right">View less</Link>
                                </div>
                            </div>
                            <div className="m-card">
                                <div className="m-card__heading">
                                    <figure>
                                        <img src="https://static1.shine.com/l/m/product_image/3425/1542800087_8980.png" alt="Digital Marketing Training Course" />
                                    </figure>
                                    <h3 className="m-heading3">
                                        <Link to={"#"}>Digital Marketing Training Course Programme</Link>
                                    </h3>
                                </div>
                                <div className="m-card__box">
                                    <div className="m-card__rating">
                                    <span className="mr-10">By ERB</span>
                                    <span className="m-rating">
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-fullstar"></em>
                                        <em className="micon-blankstar"></em>
                                        <span>4/5</span>
                                    </span>
                                    </div>
                                    <div className="m-card__duration-mode">
                                        Duration: <strong>90 days</strong>  |   Mode: <strong>Online</strong> <span className="d-block"><strong>2819</strong> Jobs available</span>
                                    </div>
                                    <div className="m-card__price">
                                        <strong>12999/-</strong> 
                                        <Link to={"#"} className="m-view-more">View more</Link>
                                    </div>
                                </div>
                            </div> */}
                        </div>
                        {page?.has_next && <span className="load-more btn-col" onClick={() => loadMoreCourses(page?.current_page)}>View More Courses</span>}
                    </div>
                    <div className="m-courses-feedback">
                        <strong>Are these courses recommendation relevant to your profile?</strong>
                        <span className="mt-15">
                            <Link className="btn-blue-outline">Yes</Link>
                            <Link className="btn-blue-outline">No</Link>
                        </span>
                    </div>
                </div>
            </section>
        </>
    )
}

export default ViewCourses;