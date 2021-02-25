import React, {useState, useEffect, useRef} from 'react';
import { Link } from 'react-router-dom';
// import Slider from "react-slick";
import 'slick-carousel/slick/slick.css';
import '../../../CataloguePage/ServicesForYou/servicesForYou.scss';
import { shineDomain, resumeShineSiteDomain } from '../../../../../../utils/domains.js';
import './shineServices.scss';
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

import { getCandidateId } from '../../../../../../utils/storage.js';
import { uploadFileUrl } from 'store/UserIntentPage/actions';
import { startGetResumeScoreLoader, stopGetResumeScoreLoader } from 'store/Loader/actions/index';
import { fetchServiceRecommendation } from 'store/UserIntentPage/actions.js';
import { useDispatch, useSelector } from 'react-redux';
import Loader from '../../../../Common/Loader/loader';
import RecommendServices from './recommendServices.jsx';
import { showSwal } from 'utils/swal';

const ShineServices = (props) => {
    const settings = {
        dots: false,
        arrows: false,
        infinite: false,
        speed: 500,
        slidesToShow: 1,
        slidesToScroll: 1,
        swipeToSlide: true,
        variableWidth: true,
    };

    const { history } = props;
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const dispatch = useDispatch();
    const fileInput = useRef(null);

    const handleClick = () => {
        fileInput.current.click()
    }


    const [alert, setAlert] = useState(false);
    const handleAlert = () => setAlert(true);
    const [filename, setFilename] = useState(undefined);
    const resetFileName = () => setFilename(undefined);
    const [file, setFile] = useState(undefined);
    const resetFile = () => setFile(undefined);
    const [totalScore, setTotalScore] = useState(undefined);
    const resetTotalScore = () => setTotalScore(undefined);
    const resetFileDetails = () => {resetFileName(); resetFile(); resetTotalScore();}
    const { resumeScoreLoader } = useSelector(store => store.loader);
    const { services , page } = useSelector(store => store.serviceRecommend);

    useEffect(() => {
        handleEffects();
    }, []);

    const fileUpload = async event => {
        let file1 = await event.target.files[0];
        if(file1 === undefined){return;}
        let fileName = event.target.files[0].name;
        if (file1.size / (1024 * 1024) > 5) {return showSwal('error', 'File size should not exceed 5MB')}
        else if (file1.name.slice(-4).toLowerCase() === '.pdf' || file1.name.slice(-4).toLowerCase() === '.doc' || file1.name.slice(-5).toLowerCase() === '.docx' || file1.name.slice(-4).toLowerCase() === '.txt') {
            setFilename(fileName);
            setFile(file1);

            try {
                dispatch(startGetResumeScoreLoader());
                const response = await new Promise((resolve, reject) => {dispatch(uploadFileUrl({ file1, resolve, reject }));})
                if(response.status == 'SUCCESS'){
                    const total_score = response.total_score;
                    setTotalScore(total_score);
                    handleClose();

                }else{
                    return showSwal('error', 'Something went wrong! Try again.')
                }
                dispatch(stopGetResumeScoreLoader());
            } catch (err) {
                if (!err['error_message']) {
                    return showSwal('error', 'Something went wrong! Try again.')
                }
                dispatch(stopGetResumeScoreLoader());
            }
        }
        else {return showSwal('error', 'File size should be in .doc, PDF, .docx format only')}
    }

    const handleEffects = async () => {
        try {

                dispatch(startGetResumeScoreLoader());
                const candidate_id = getCandidateId();
                await new Promise((resolve, reject) => dispatch(fetchServiceRecommendation({ candidate_id: candidate_id, resolve, reject })));
                dispatch(stopGetResumeScoreLoader());

        } catch (error) {
            dispatch(stopGetResumeScoreLoader());
            if (error?.status == 404) {
                history.push('/404');
            }
        }
    };


    return (
        <>
            { resumeScoreLoader ? <Loader /> : ''}
            <section className="m-container mt-0 mb-0 pl-0 pr-0">
                <div className="m-ui-main col">
                    <div className="d-flex align-items-center">
                        <div className="m-ui-steps">
                            <Link className="m-completed" to={"#"}>1</Link>
                            <Link className="m-completed" to={"#"}>2</Link>
                        </div>
                        <Link className="btn-blue-outline m-back-goal-btn" to={"/user-intent/"}>Back to goal</Link>
                    </div>
                    <h2 className="m-heading3 mt-20">Get an edge over others with shine services</h2>
                    { totalScore ?
                    <div className="m-shine-services flex-column mt-20">
                        <span className="d-flex w-100">
                            <CircularProgressbar value={totalScore/100} maxValue={1} text={`${totalScore}`} />
                            <span>
                                <strong className="heading3 d-block">Your resume Scored <br />{totalScore} out of 100 </strong> 
                                <Link className="file-close mt-10" to={"#"}>{filename} <i className="icon-close-sm ml-10" onClick={() => resetFileDetails()}></i></Link>
                            </span>
                        </span>
                        <span className="fs-13 d-block mt-20">
                            <span className="">
                                Check out the detailed reviews to improve the score. <strong className="fs-13">Score more to get perfect job match your profile</strong>
                                <a href={`${resumeShineSiteDomain}/resume-score-checker`} className="mt-10">View details</a>
                            </span>
                        </span>
                    </div> :
                    <div className="m-shine-services mt-20">
                        <figure className="micon-upload-resume"></figure>
                        <p>Updated resume increases the chances of getting more opportunities. 
                            <a className="mt-10" onClick={() => handleClick()}>
                            <input ref={fileInput}  type="file" name="myfile" style={{ display: "none" }} onChange={fileUpload} />Upload latest resume</a>
                        </p>

                    </div> }
                    {/* <div className="m-shine-services mt-20">
                        <figure className="micon-upload-resume"></figure>
                        <p>Updated resume increases the chances of getting more opportunities. 
                            <Link to={"#"} className="mt-10">Upload latest resume</Link>
                        </p>
                        
                    </div> */}
                    <div className="m-shine-services mt-20">
                        <figure className="micon-update-profile"></figure>
                        <p>Update your profile to get customised career recommendation 
                            <a href={shineDomain + "/myshine/myprofile/"} className="mt-10">Update your profile</a>
                        </p>
                    </div>
                    { services ? <RecommendServices services={services} settings={settings}/> : null }
                    {/* <div className="m-services-foryou ml-10n mt-40">
                        <h2 className="m-heading2 ml-10">Recommended services</h2>
                        <Slider {...settings}>
                            <div className="m-services-foryou__list">
                                <h3 className="m-heading3">Resume Writing</h3>
                                <p>Resume written by experts to increase your profile visibility</p>
                                <span className="d-flex">
                                    <Link to={"#"}>Know more</Link>
                                    <figure className="micon-service1"></figure>
                                </span>
                            </div>
                            <div className="m-services-foryou__list">
                                <h3 className="m-heading3">Featured Profile</h3>
                                <p>Appear on top when Recruiters search for best candidates</p>
                                <span className="d-flex">
                                    <Link to={"#"}>Know more</Link>
                                    <figure className="micon-service2"></figure>
                                </span>
                            </div>
                            <div className="m-services-foryou__list">
                                <h3 className="m-heading3">Jobs on the Move</h3>
                                <p>Get personalized job recommendations from all the job portals on your Whatsapp</p>
                                <span className="d-flex">
                                    <Link to={"#"}>Know more</Link>
                                    <figure className="micon-service3"></figure>
                                </span>
                            </div>
                            <div className="m-services-foryou__list">
                                <h3 className="m-heading3">Application Highlighter</h3>
                                <p>Get your Job Application noticed among others</p>
                                <span className="d-flex">
                                    <Link to={"#"}>Know more</Link>
                                    <figure className="micon-service4"></figure>
                                </span>
                            </div>
                        </Slider>
                    </div> */}
                </div>
            </section>
        </>
    )
}

export default ShineServices;