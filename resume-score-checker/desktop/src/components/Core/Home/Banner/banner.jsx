import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Redirect } from 'react-router-dom'
import * as Actions from '../../../../store/LandingPage/actions/index';
import './banner.scss'
import Loader from '../../../Loader/loader';
import { Toast } from '../../../../services/Toast';
import { siteDomain } from '../../../../utils/domains'

const Banner = props => {

    const [flag, setFlag] = useState(false);
    const [redirect, setRedirect] = useState(false);
    const dispatch = useDispatch()
    const staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
    const resumeImport = async event => {
        if (!localStorage.getItem('userId')) {
            const isSessionAvailable = await new Promise((resolve, reject) => dispatch(Actions.checkSessionAvailability({ resolve, reject })));

            if (isSessionAvailable['result']) {
                // await dispatch(Actions.getCandidateId())
                try {
                    const candidateInfo = await new Promise((resolve, reject) => dispatch(Actions.getCandidateInfo({ resolve, reject })))

                    // const response = await new Promise((resolve,reject)=>dispatch(Actions.getCandidateResume({resolve,reject})))
                    //fileUpload({terget: {files : [response]}})
                    setFlag(true);
                    await new Promise((resolve, reject) => dispatch(Actions.getCandidateScore({ candidateId: candidateInfo['candidate_id'], resolve, reject })))
                    setFlag(false)
                    setRedirect(true)
                }
                catch (e) {
                    setFlag(false);
                    Toast.fire({
                        icon: 'error',
                        html: '<h3>Something went wrong! Try again.<h3>'
                    })
                }
            }
            else {
                window.location.href = `${siteDomain}login/?next=/resume-score-checker/`
            }
        }
        else {
            try {
                // const response = await new Promise((resolve, reject) => dispatch(Actions.getCandidateResume({ resolve, reject })))
                // fileUpload({ terget: { files: [response] } })
                setFlag(true);
                await new Promise((resolve, reject) => dispatch(Actions.getCandidateScore({ candidateId: localStorage.getItem('userId'), resolve, reject })))
                setFlag(false)
                setRedirect(true)
            }
            catch (e) {
                setFlag(false)
                Toast.fire({
                    icon: 'error',
                    html: '<h3>Something went wrong! Try again.<h3>'
                })
            }
        }
    }

    const fileUpload = async event => {

        let file1 = event.target.files[0];
        event.target.value = null
        if ((file1.name.slice(-4) === '.pdf' || file1.name.slice(-4) === '.doc' || file1.name.slice(-5) === '.docx' || file1.name.slice(-4) === '.txt')) {
            try {
                setFlag(true)
                await new Promise((resolve, reject) => {
                    dispatch(Actions.uploadFileUrl({ file1, resolve, reject }));
                })
                setFlag(false)
                setRedirect(true)
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
                html: '<h3>Please select the file in the format PDF,DOC,DOCX only<h3>',
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
                                Upload New Resume
                    <input className="file-upload__input" type="file" onChange={fileUpload} name="resume" />
                            </div>

                            {flag && <Loader></Loader>}
                            {redirect &&
                                <Redirect push to="/resume-score-checker/score-checker" className="file-upload btn btn-secondary btn-round-40 font-weight-bold d-flex px-5 py-4 mr-4">
                                </Redirect>
                            }

                            <button onClick={resumeImport} className="d-flex align-items-center btn btn-outline-light btn-round-40 font-weight-bold px-4">
                                <i className="sprite export mr-3"></i>
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