import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Redirect } from 'react-router-dom'
import * as Actions from '../../../../store/LandingPage/actions/index';
import { eventClicked } from '../../../../store/googleAnalytics/actions/index'
import './banner.scss'
import Loader from '../../../Loader/loader';
import Swal from 'sweetalert2'
import { siteDomain } from '../../../../utils/domains'
import { useHistory } from "react-router-dom";
const queryString = require('query-string');


const Banner = props => {
    const [flag, setFlag] = useState(false);
    const [redirect, setRedirect] = useState(false);
    const dispatch = useDispatch()
    const staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
    const history = useHistory()

    const parsed = queryString.parse(history.location.search);

    useEffect(() => {
        const importResumeFromShine = async () => {
            await resumeImport();
        }
        if (parsed && parsed.candidate === 'true') {
            setFlag(true);
            setTimeout(() =>{
                importResumeFromShine;
            }, 2000)
        }
        else if (parsed && parsed.import === 'true') {
            importResumeFromShine
        }
    }, [])


    const resumeImport = async event => {

        dispatch(eventClicked({
            'action': 'Import from shine',
            'label': 'FirstFold'
        }))
        if (!localStorage.getItem('userId')) {
            setFlag(true);
            const isSessionAvailable = await new Promise((resolve, reject) => dispatch(Actions.checkSessionAvailability({ resolve, reject })));

            if (isSessionAvailable['result']) {
                // await dispatch(Actions.getCandidateId())
                try {
                    const candidateInfo = await new Promise((resolve, reject) => dispatch(Actions.getCandidateInfo({ resolve, reject })))
                    // const response = await new Promise((resolve,reject)=>dispatch(Actions.getCandidateResume({resolve,reject})))
                    //fileUpload({terget: {files : [response]}})
                    let resumeId = parsed.resume_id ? parsed.resume_id : null;
                    setFlag(true);
                    await new Promise((resolve, reject) => dispatch(Actions.getCandidateScore({ candidateId: candidateInfo['candidate_id'], resumeId: resumeId, resolve, reject })))
                    setFlag(false)
                    setRedirect(true)
                }
                catch (e) {
                    setFlag(false);
                    Swal.fire({
                        icon: 'error',
                        html: '<h3>Something went wrong! Try again.<h3>'
                    })
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
                // const response = await new Promise((resolve, reject) => dispatch(Actions.getCandidateResume({ resolve, reject })))
                // fileUpload({ terget: { files: [response] } })
                let resumeId = parsed.resume_id ? parsed.resume_id : null;
                setFlag(true);
                await new Promise((resolve, reject) => dispatch(Actions.getCandidateScore({ candidateId: localStorage.getItem('userId'), resumeId: resumeId, resolve, reject })))
                setFlag(false)
                setRedirect(true)
            }
            catch (e) {
                setFlag(false)
                if (!e['error_message']) {
                    Swal.fire({
                        icon: 'error',
                        html: '<h3>Something went wrong! Try again.<h3>'
                    })
                }
            }
        }

    }

    const fileUpload = async event => {

        dispatch(eventClicked({
            'label': "Upload Resume",
            'action': "Firstfold"
        }))
        event.persist();
        let file1 = event.target.files[0];
        event.target.value = null
        if (file1.size / (1024 * 1024) > 5) {
            Swal.fire({
                icon: 'warning',
                html: '<h3>File size should be less than 5 MB<h3>',
            })
        }
        else if (file1.name.slice(-4).toLowerCase() === '.pdf' || file1.name.slice(-4).toLowerCase() === '.doc' || file1.name.slice(-5).toLowerCase() === '.docx' || file1.name.slice(-4).toLowerCase() === '.txt') {
            try {
                setFlag(true)
                await new Promise((resolve, reject) => {
                    dispatch(Actions.uploadFileUrl({ file1, resolve, reject }));
                })
                localStorage.setItem('file_name', file1.name);
                setFlag(false)
                setRedirect(true)
            } catch (err) {
                setFlag(false)
                if (!err['error_message']) {
                    Swal.fire({
                        icon: 'error',
                        html: '<h3>Something went wrong! Try again.<h3>'
                    })
                }
            }
        }
        else {
            Swal.fire({
                icon: 'warning',
                html: '<h3>Please select the file in the format PDF,DOC,DOCX,TXT only<h3>',
            })
        }
    }

    return (
        <section className="banner" id="banner">
            <div className="container h-100">
                <div className="row h-100">
                    <div className="col-md-6 h-100 d-flex align-items-self-start justify-content-center flex-column">
                        <h1>
                            <span>Smart Resume Score Checker</span>
                        </h1>
                        <p className="">Get the <strong>free review</strong> of your resume in <strong>just 30 sec</strong></p>

                        <div className="d-flex mt-5">

                            <div className="file-upload btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                                <i className="sprite upload mr-3"></i>
                                {
                                    !!(JSON.parse(localStorage.getItem('resume_score'))) ? "Upload New Resume" : "Upload Resume"
                                }
                                <input className="file-upload__input" type="file" onChange={fileUpload} name="resume" />
                            </div>

                            {flag && <Loader></Loader>}
                            {redirect &&
                                <Redirect push to="/resume-score-checker/score-checker" className="file-upload btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                                </Redirect>
                            }

                            <button onClick={resumeImport} className="d-flex align-items-center btn btn-outline-light btn-round-40 font-weight-bold px-4">
                                <i className="sprite export down mr-3"></i>
                                Import from shine.com
                    </button>
                        </div>
                        <p className="banner__text">PDF, DOC, DOCX, TXT only  |  Max file size: 5MB</p>
                    </div>
                    <div className="col-md-6">
                        <div className="banner__image">
                            <img aria-label="header image" className="banner__image" alt="banner" src={`${staticUrl}score-checker/images/banner-img.png`} />
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default Banner;