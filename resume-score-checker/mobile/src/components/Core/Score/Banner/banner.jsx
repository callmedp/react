import React, { useEffect, useState } from 'react';
import './score-banner.scss';
import * as Actions from '../../../../stores/scorePage/actions/index.js'
import { useDispatch } from 'react-redux';
import { useHistory } from 'react-router-dom';
import { siteDomain } from '../../../../Utils/domains';
import Loader  from '../../../Common/Loader/loader.jsx'
import {Toast} from '../../../../services/Toast';
const queryString = require('query-string');

export default function Banner() {
    const [flag, setFlag] = useState(false);
    const dispatch = useDispatch();
    const history = useHistory();
    const parsed = queryString.parse(history.location.search);

    useEffect(() => {
        window.scrollTo(0, 0);

        const importResume = async () => {
            if (!localStorage.getItem('userId')) {
                setFlag(true)
                const isSessionAvailable = await new Promise((resolve, reject) => dispatch(Actions.checkSessionAvailability({ resolve, reject })));

                if (isSessionAvailable['result']) {
                    try {
                        setFlag(true);
                        const candidateInfo = await new Promise((resolve, reject) => dispatch(Actions.getCandidateInfo({ resolve, reject })))
                        let result = await new Promise((resolve, reject) => dispatch(Actions.getCandidateScore({ candidateId: candidateInfo['candidate_id'], resolve, reject })))
                        setFlag(false)
                        if (result['error_message']) {
                            Toast('warning', result['error_message'])
                        }
                    }
                    catch (error) {
                        setFlag(false);
                        Toast('error', 'Something went wrong! Try again')
                    }
                }
                else {
                    setFlag(true);
                    setTimeout(() => {
                        window.location.replace(`${siteDomain}/login/?next=/resume-score-checker/?import=true`)
                    }, 100)
                }
            }
            else {
                try {
                    setFlag(true);
                    let result = await new Promise((resolve, reject) => dispatch(Actions.getCandidateScore({ candidateId: localStorage.getItem('userId'), resolve, reject })))
                    setFlag(false)
                    if (result['error_message']) {
                        Toast('warning', result['error_message'])
                    }
                }
                catch (e) {
                    setFlag(false)
                    Toast('error', 'Something went wrong! Try again')
                }
            }
        }
        if (parsed && parsed.candidate === 'true') importResume();
    }, [])
    const localValue = JSON.parse(localStorage.getItem('resume_score'))
    const storeValue = localValue ?.total_score;

    const score = localStorage.getItem('resume_score') === null ? storeValue : localValue['total_score'];

    const scoreBasedDescription = () => {
        switch (true) {
            case score > 80:
                return <p className="mt-15">Great Job! Your resume scores well as per the industry standards. Check out the detailed reviews</p>
            case score > 65 && score <= 80:
                return <p className="mt-15">Good Job! You are just few steps away from perfecting your resume. Check out the detailed reviews to improve the score. Score more to improve your chances of short listing</p>
            case score > 50 && score <= 65:
                return <p className="mt-15">Your resume score is average and can be improved a lot with quick fixes we have highlighted in the detailed review. You can also get expert assistance to perfect the score</p>
            default: {
                return <p className="mt-15">Your resume score is low. It has room for lot of improvements. Check out the detailed reviews to improve the score or reach out to our experts to improve your resume</p>
            }
        }
    }

    return (
        <div>
            {
                flag && <Loader />
            }
            <div className="score-banner">
                <div className="container-box">
                    <h1 className="mb-10"><span>Hello {localStorage.getItem('userName') || "User"} <br />Your resume scored {score} out of 100</span></h1>

                    <div className="score-banner__image">
                        <div className="score-banner__progressBar">
                            <div className="ko-progress-circle" data-progress={Math.round(score) ? Math.round(score) : 0}>
                                <div className="ko-progress-circle__text">
                                    <strong>{score}</strong>
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
                    </div>
                    <div className="circle"></div>
                    <div className="dots"></div>
                </div>
            </div>

            <div className="container-box">
                <div className="resume-detail mb-30 text-center">
                    <p>
                        {
                            localStorage.getItem('resume_file') ? localStorage.getItem('resume_file') : 'No Resume'
                        }
                    </p>
                    {/* <a href="#" className="btn btn-round-30 btn-outline-blue py-5">Download</a> */}
                    {/* Good Job! You are just few steps away for perfecting your resume. Check out the detailed reviews to improve the score. Score more to get perfect job match your profile */}
                    {scoreBasedDescription()}
                </div>

            </div>
        </div>

    );
} 