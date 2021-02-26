import React, {useState, useEffect} from 'react';
import { Link } from 'react-router-dom';
import { shineDomain, resumeShineSiteDomain } from '../../../../../../utils/domains.js';
import { getCandidateId } from '../../../../../../utils/storage.js';
import Modal from 'react-bootstrap/Modal';
import '../../../CataloguePage/ServicesForYou/servicesForYou.scss';
import {uploadFileUrl} from 'store/UserIntentPage/actions';
import { startGetResumeScoreLoader, stopGetResumeScoreLoader } from 'store/Loader/actions/index';
import { fetchServiceRecommendation } from 'store/UserIntentPage/actions.js';
import { CircularProgressbar } from 'react-circular-progressbar';
import './shineServices.scss';
import { useDispatch, useSelector } from 'react-redux';
import Loader from '../../../../Common/Loader/loader';
import RecommendServices from './serviceRecommend.jsx';
import { showSwal } from 'utils/swal';

const ShineServices = (props) => {
    const { history } = props;
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const dispatch = useDispatch();
    const [alert, setAlert] = useState(false);
    const handleAlert = () => setAlert(true);
    const [filename, setFilename] = useState("Choose file");
    const resetFileName = () => setFilename("Choose file");
    const [file1, setFile] = useState(undefined);
    const resetFile = () => setFile(undefined);
    const [totalScore, setTotalScore] = useState(undefined);
    const resetTotalScore = () => setTotalScore(undefined);
    const resetFileDetails = () => {resetFileName(); resetFile(); resetTotalScore();}
    const { resumeScoreLoader } = useSelector(store => store.loader);
    const { services , page } = useSelector(store => store.serviceRecommend);

    useEffect(() => {
        handleEffects();
    }, []);

    const fileUploadName = async event => {
        let file2 = await event.target.files[0];
        if(file2 === undefined){return;}
        let fileName = event.target.files[0].name;
        //event.target.value = null
        if (file2.size / (1024 * 1024) > 5) {handleAlert()}
        else if (file2.name.slice(-4).toLowerCase() === '.pdf' || file2.name.slice(-4).toLowerCase() === '.doc' || file2.name.slice(-5).toLowerCase() === '.docx' || file2.name.slice(-4).toLowerCase() === '.txt') {
            setFilename(fileName);
            setFile(file2);
        }
        else {handleAlert()}
    }

    const fileUpload = async (event) => {
        if(!file1) {
            handleAlert(); return;
        }
        else {
            try {
                dispatch(startGetResumeScoreLoader());
                const response = await new Promise((resolve, reject) => {dispatch(uploadFileUrl({ file1, resolve, reject }));})
                if(response.status == 'SUCCESS') {
                    const total_score = response.total_score;
                    setTotalScore(total_score);
                }
                else {
                    showSwal('error', 'Something went wrong! Try Again')
                }
                dispatch(stopGetResumeScoreLoader());
            }
            catch (err) {
                if (!err['error_message']) showSwal('error', 'Something went wrong! Try Again')
                dispatch(stopGetResumeScoreLoader());
            }

            handleClose();
        }
    }

    const handleEffects = async () => {
        try {
            dispatch(startGetResumeScoreLoader());
            // const candidate_id = getCandidateId();
            await new Promise((resolve, reject) => dispatch(fetchServiceRecommendation({ resolve, reject })));
            dispatch(stopGetResumeScoreLoader());
        }
        catch (error) {
            dispatch(stopGetResumeScoreLoader());
            if (error?.status == 404) history.push('/404');
        }
    };

    return (
        <>
            { resumeScoreLoader ? <Loader /> : ''}
            <section className="container-fluid mt-30n mb-0">
                <div className="row">
                    <div className="container">
                        <div className="ui-main col">
                            <div className="ui-steps">
                                <Link className="completed" to={"#"}>1</Link>
                                <Link className="completed" to={"#"}>2</Link>
                                {/* <Link to={"#"}>3</Link> */}
                            </div>
                            <h2 className="heading3 mt-20">Get an edge over others with shine services</h2>
                            { totalScore ? 
                            <div className="shine-services w-70">
                                <CircularProgressbar value={totalScore/100} maxValue={1} text={`${totalScore}`} />
                                <span className="fs-13">
                                    <strong className="heading3 d-block">Your resume Scored {totalScore} out of 100 </strong> 
                                    Check out the detailed reviews to improve the score. <strong className="fs-13">Score more to get perfect job match your profile</strong>
                                    <span className="d-flex mt-20">
                                        <a href={`${resumeShineSiteDomain}/resume-score-checker`}>View details</a>
                                        <Link className="file-close">{filename} <i className="icon-close-sm ml-10" onClick={() => resetFileDetails()} ></i></Link>
                                    </span>
                                </span>
                            </div> :
                            <div className="shine-services w-70">
                                <figure className="icon-upload-resume"></figure>
                                <p>Updated resume increases the chances of getting more opportunities. </p>
                                <Link to={"#"} onClick={handleShow} className="ml-auto">Upload latest resume</Link>
                            </div>
                        }
                            {/* <div className="shine-services w-70">
                                <figure className="icon-upload-resume"></figure>
                                <p>Updated resume increases the chances of getting more opportunities. </p>
                                <Link to={"#"} onClick={handleShow} className="ml-auto">Upload latest resume</Link>
                            </div> */}
                            <div className="shine-services w-70">
                                <figure className="icon-update-profile"></figure>
                                <p>Update your profile to get customised career recommendation </p>
                                {/* <Link to={"#"} className="ml-auto">Update your profile</Link> */}
                            {/* </div> */}

                            {/* <h2 className="heading3 mt-50">Recommended services</h2>
                            <div className="w-70">
                                <div className="row recommend-services">
                                    <div className="col">
                                        <div className="services-foryou">
                                            <h3 className="heading3">Resume Writing</h3>
                                            <p>Resume written by experts to increase your profile visibility</p>
                                            <span className="d-flex">
                                                <Link to={"#"}>Know more</Link>
                                                <figure className="icon-service1"></figure>
                                            </span>
                                        </div>
                                    </div>
                                    <div className="col">
                                        <div className="services-foryou">
                                            <h3 className="heading3">Featured Profile</h3>
                                            <p>Appear on top when Recruiters search for best candidates</p>
                                            <span className="d-flex">
                                                <Link to={"#"}>Know more</Link>
                                                <figure className="icon-service2"></figure>
                                            </span>
                                        </div>
                                    </div>
                                    <div className="col">
                                        <div className="services-foryou">
                                            <h3 className="heading3">Jobs on the Move</h3>
                                            <p>Get personalized job recommend -ations from all the job portals on your Whatsapp</p>
                                            <span className="d-flex">
                                                <Link to={"#"}>Know more</Link>
                                                <figure className="icon-service3"></figure>
                                            </span>
                                        </div>
                                    </div>
                                </div> */}
                                <a href={shineDomain + "/myshine/myprofile/"} className="ml-auto">Update your profile</a>
                            </div>
                            { services ? <RecommendServices services={services} /> : null } 
                        </div>
                    </div>
                </div>
                <Modal show={show} 
                    onHide={handleClose}
                    {...props}
                    // size="md"
                    dialogClassName="resume-upload-box"
                    className="db-page"
                    aria-labelledby="contained-modal-title-vcenter"
                    centered
                >
                    <Modal.Header closeButton>
                    </Modal.Header>
                    <Modal.Body>
                        <h2 className="mb-20">Upload Resume</h2>
                            <p>increases the chances of getting more opportunities, with latest resume</p>
                            <div class="upload-btn-wrapper mt-5">
                                <button class="btn-upload"><input class="btn-upload" type="file" name="myfile" onChange={fileUploadName} />{filename}</button>  
                            </div>
                            <span className={alert ?"d-block mt-10 alert":"d-block mt-10"}>File size should not exceed 5MB. in .doc, PDF, .docx format only</span>
                            <button className="btn btn-primary submit-btn mx-auto mt-30" onClick={fileUpload}>Save</button>
                    </Modal.Body>
                    
                    {/* <Modal.Header closeButton>
                    </Modal.Header>
                    <Modal.Body>
                        <h2 className="mb-20">Upload Resume</h2>
                        <form className="mt-10">
                            <p>increases the chances of getting more opportunities, with latest resume</p>
                            <div class="upload-btn-wrapper mt-5">
                                <button class="btn-upload">Choose file<input type="file" name="myfile" /></button>
                                
                            </div>
                            <span className="d-block mt-10">File size should not exceed 3MB. in .doc, PDF, Jpeg format only</span>
                            <button type="submit" className="btn btn-primary submit-btn mx-auto mt-30" role="button">Save</button>
                        </form>
                    </Modal.Body> */}
                </Modal>
            </section>
            </>
    )
}

export default ShineServices;