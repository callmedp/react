import React, { useState } from 'react';
import './innerBanner.scss';
import { Link as LinkScroll } from 'react-scroll';
import { Link } from 'react-router-dom'
import { useDispatch } from 'react-redux';
import * as Actions from '../../../../store/LandingPage/actions/index';
import Loader from '../../../Loader/loader';
import { Toast } from '../../../../services/Toast';
import { useHistory } from "react-router-dom";

const InnerBanner = props => {

    const [flag, setFlag] = useState(false);
    const localScore = JSON.parse(localStorage.getItem('resume_score'))?.total_score
    const total_local_score = JSON.parse(localStorage.getItem('resume_score'))?.section_score
    const reduced = (accumulator, currentValue) => accumulator + currentValue.section_total_score;
     const file_name = localStorage.getItem('file_name')
    const dispatch = useDispatch()
    useState(() => {

    }, [])
    const history = useHistory()
    const fileUpload = async event => {
        event.persist();
        let file1 = await event.target.files[0];
        event.target.value = null

        if ((file1.name.slice(-4) === '.pdf' || file1.name.slice(-4) === '.doc' || file1.name.slice(-5) === '.docx' || file1.name.slice(-4) === '.txt')  && file1.size/(1024*1024)<=5){
            try {

                setFlag(true)
                await new Promise((resolve, reject) => {
                    dispatch(Actions.uploadFileUrl({ file1, resolve, reject }));
                })
                localStorage.setItem('file_name',file1.name);
                setFlag(false)
                history.push('/resume-score-checker/score-checker')
               
               
            } catch (err) {
                setFlag(false)
                if (!err['error_message']) {

                    Toast.fire({
                        icon: 'error',
                        html: '<h3>Something went wrong! Try again.<h3>'
                    })
                }
            }

        }
        else {

            Toast.fire({
                icon: 'warning',
                html: '<h3>Please select the file in the format PDF,DOC,DOCX,TXT and less than 5MB only<h3>',
            })
        }
    }

    const scoreBasedText = (score) => {
        if (score > 80) {
            return <p className="text-white-50">Great Job! Your resume scores well as per the industry standards. Check out the detailed reviews</p>
        }
        else if (score > 65 && score <= 80) {
            return <p className="text-white-50">Good Job! You are just few steps away for perfecting your resume. Check out the detailed reviews to improve the score. Score more to get perfect job match your profile</p>
        }
        else if (score > 50 && score <= 65) {
            return <p className="text-white-50">Your resume score is average and can be improved a lot with quick fixes we have highlighted in the detailed review. You can also get expert assistance to perfect the s core</p>
        }
        else {
            return <p className="text-white-50">Your resume score is low. It has room for lot of improvements. Check out the detailed reviews to improve the score or reach out to our experts to improve your resume</p>
        }
    }


    return (
        <div>
            <section className="banner">
                <div className="container h-100">
                    <div className="row h-100">
                        <div className="col-md-6">
                            <div className="banner-score">
                                <nav aria-label="breadcrumb">
                                    <ol className="breadcrumb">
                                        <li className="breadcrumb-item"><Link to='/resume-score-checker/'>Home</Link></li>
                                        <li className="breadcrumb-item active" aria-current="page">Resume Review</li>
                                    </ol>
                                </nav>
                                <div className="banner-score__resume-scoreWrap">
                                    <div className="banner-score__progressBar">

                                        <div className="ko-progress-circle" data-progress={Math.round(localScore * 100 / total_local_score?.reduce(reduced, 0))}>
                                            <div className="ko-progress-circle__text">
                                                <strong>{localScore}</strong>
                                                <p className="fs-12">Resume score</p>

                                            </div>
                                            <div className="ko-circle">
                                                <div className="full ko-progress-circle__slice">
                                                    <div className="ko-progress-circle__fill"></div>
                                                </div>
                                                <div className="ko-progress-circle__slice">
                                                    <div className="ko-progress-circle__fill"></div>
                                                    <div className="ko-progress-circle__fill ko-progress-circle__bar"></div>
                                                </div>
                                            </div>
                                            <div className="ko-progress-circle__overlay"></div>
                                        </div>
                                    </div>
                                    <div className="banner-score__myresume">
                                        <a href="/#">
                                            <i className="sprite clip"></i>
                                        {file_name}
                                        </a>

                                        <a href="/#" className="btn btn-outline-primary btn-round-40 fs-12 py-1">Download</a>
                                    </div>
                                </div>

                            </div>
                        </div>
                        <div className="col-md-6 h-100 d-flex align-items-self-start justify-content-center flex-column">
                            <h1 className="fs-30">
                                <span>Hello {localStorage.getItem('userName') || 'User'},<br />Your resume Scored {localScore} out of {total_local_score?.reduce(reduced, 0)}</span>
                            </h1>
                            {scoreBasedText(localScore * 100 / total_local_score?.reduce(reduced, 0))}
                            <div className="d-flex mt-5">
                                <LinkScroll
                                    to='getexpert'
                                    className="btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                                    Get expert help
                    </LinkScroll>
                                <div className="file-upload btn btn-outline-light btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                                    <i className="sprite export mr-3"></i>
                            Upload New Resume
                        <input className="file-upload__input" type="file" onChange={fileUpload} name="resume" />
                                </div>
                                {flag && <Loader></Loader>}


                            </div>

                        </div>

                    </div>
                </div>
            </section>
            <section className="howItWork" style={{ height: '60px' }}></section>
        </div>
    );
}

export default InnerBanner;