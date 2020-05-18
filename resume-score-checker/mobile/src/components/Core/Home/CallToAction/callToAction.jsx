import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Redirect, useLocation } from 'react-router-dom';
import './callToAction.scss';
import * as Actions from '../../../../stores/scorePage/actions/index';
import { eventClicked } from '../../../../stores/googleAnalytics/actions/index';
import Loader from '../../../Common/Loader/loader';
import { Toast } from '../../../../services/Toast';
import { siteDomain } from '../../../../Utils/domains';


export default function CallToAction() {

    const [flag, setFlag] = useState(true);
    const [visible, setVisible] = useState(false);
    const [filename, setFileName] = useState('Upload Resume');
    // let location_value = useLocation();
    // let import_value = new URLSearchParams(location_value.search).get("import");

    useEffect(() => localStorage.getItem("resume_score") === null ? setFileName('Upload Resume') : setFileName('Upload New Resume'), [])

    const dispatch = useDispatch();
    const fileUpload = async event => {
        dispatch(eventClicked({
            'action': 'M_UploadResume',
            'label': 'Footer'
        }))

        setVisible(!visible)
        const file = event.target.files[0];
        event.target.value = null;
        if (file.name.slice(-4).toLowerCase() === '.pdf' || file.name.slice(-4).toLowerCase() === '.txt' || file.name.slice(-4).toLowerCase() === '.doc' || file.name.slice(-5).toLowerCase() === '.docx') {
            if (!(file.size / (1024 * 1024) <= 5)) {
                Toast('error', 'File size should be less than 5MB')
                setVisible(false)
            }
            else {
                setFileName('Fetching Score...')
                try {
                    let result = await new Promise((resolve, reject) => {
                        dispatch(Actions.uploadFile({ file, resolve, reject }));
                    })
                    if (result['error_message']) {
                        Toast('error', result['error_message'])
                        setFileName("Upload Resume")
                        setVisible(false)
                    }
                    else {
                        localStorage.setItem('resume_file', file.name)
                        setFlag(!flag)
                    }
                }
                catch (e) {
                    Toast('error', 'Something went wrong! Try again')
                    setFileName("Upload Resume")
                    setVisible(false)
                }
            }
        }
        else {
            Toast('error', 'Please Upload Pdf, Doc, Docx or txt format file only')
            setVisible(false)
        }
    }

    const importResume = async () => {

        dispatch(eventClicked({
            'action': 'M_ImportShine',
            'label': 'Footer'
        }))
        setVisible(!visible)
        if (!localStorage.getItem('userId')) {
            const isSessionAvailable = await new Promise((resolve, reject) => dispatch(Actions.checkSessionAvailability({ resolve, reject })));

            if (isSessionAvailable['result']) {
                try {
                    // await new Promise((resolve, reject) => dispatch(Actions.getCandidateId({resolve, reject})))
                    // let resume = await new Promise((resolve, reject) => {
                    //     dispatch(Actions.getCandidateResume({ resolve, reject }));
                    // })
                    setFlag(true);
                    const candidateInfo = await new Promise((resolve, reject) => dispatch(Actions.getCandidateInfo({ resolve, reject })))
                    let result = await new Promise((resolve, reject) => dispatch(Actions.getCandidateScore({ candidateId: candidateInfo['candidate_id'], resolve, reject })))
                    if (result['error_message']) {
                        Toast('warning', result['error_message'])
                        setVisible(false)
                    }
                    else { setFlag(false) }

                    // fileUpload({target : {files : [resume]}})
                }
                catch (error) {
                    //setFlag(false);
                    Toast('error', 'Something went wrong! Try again')
                    setVisible(false)
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
                // let resume = await new Promise((resolve, reject) => {
                //     dispatch(Actions.getCandidateResume({ resolve, reject }));
                // })
                // fileUpload({target : { files : [resume] }})
                setFlag(true);
                let result = await new Promise((resolve, reject) => dispatch(Actions.getCandidateScore({ candidateId: localStorage.getItem('userId'), resolve, reject })))
                if (result['error_message']) {
                    Toast('warning', result['error_message'])
                    setVisible(false)
                }
                else { setFlag(false) }
            }
            catch (e) {
                //setFlag(false)
                Toast('error', 'Something went wrong! Try again')
                setVisible(false)
            }
        }
    }

    // if(import_value){
    //     importResume()
    // }


    return (
        <div className="call-to-action">
            <div className="d-flex justify-content-between">
                <div className="d-flex align-items-center file-upload btn btn-yellow btn-round-30 fs-11 mr-10 px-20">
                    <i className="sprite upload mr-5"></i> {filename}
                    <input className="file-upload__input_right" type="file" name="file" onChange={fileUpload}></input>
                </div>

                <div className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20" onClick={importResume}>
                    <i className="sprite export down mr-5"></i>
                    Import from shine.com
            </div>
                {
                    (flag &&
                        <React.Fragment>
                            {
                                visible &&
                                <Loader />
                            }
                        </React.Fragment>)
                    ||
                    <Redirect push to="/resume-score-checker/score-checker" />
                }
            </div>
        </div>
    );
}
