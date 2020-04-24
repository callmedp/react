import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Redirect } from 'react-router-dom';
import * as Actions from '../../../../stores/scorePage/actions/index';
import { eventClicked } from '../../../../stores/googleAnalytics/actions/index';
import './callToAction.scss';

import GetExpertForm from '../../Forms/GetExpertForm/getExpertForm';
import Loader from '../../../Common/Loader/loader';
import { Toast } from '../../../../services/Toast';

export default function CallToActionScore() {
    const [isFormVisible, setIsFormVisible] = useState(false);
    const toggle = () => {
        dispatch(eventClicked({
            'action': 'M_ExpertHelp',
            'label': 'Footer'
        }))
        setIsFormVisible(!isFormVisible)
    }

    const [flag, setFlag] = useState(true);
    const [visible, setVisible] = useState(false);
    const [filename, setFileName] = useState('Upload New Resume');

    const dispatch = useDispatch();
    const fileUpload = async event => {
        dispatch(eventClicked({
            'action': 'M_UploadNew',
            'label': 'Footer'
        }))
        setVisible(!visible)
        const file = event.target.files[0];
        event.target.value = null
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
                        setFileName("Upload New Resume")
                        setVisible(false)
                    }
                    else {
                        localStorage.setItem('resume_file', file.name)
                        setFileName("Upload New Resume")
                        setFlag(!flag)
                    }
                }
                catch (e) {
                    Toast('error', 'Something went wrong! Try again')
                    setFileName("Upload New Resume")
                    setVisible(false)
                }
            }
        }
        else {
            Toast('error', 'Please Upload only Pdf, Doc, Docx or txt format file only')
            setVisible(false)
        }
    }

    return (
        <div className="call-to-action">
            <div className="d-flex justify-content-between">
                <button className="d-flex align-items-center file-upload btn btn-yellow btn-round-30 fs-11 mr-10 px-30" onClick={toggle}>
                    <i className="sprite mr-5"></i>
                    Get expert help
                </button>

                <div className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20">
                    <i className="sprite export mr-5"></i> {filename}
                    <input className="file-upload__input_left" type="file" name="file" onChange={fileUpload}></input>
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
                    <Redirect to="/resume-score-checker/score-checker" />
                }
                <GetExpertForm isFormVisible={isFormVisible} hide={toggle} />
            </div>
        </div>
    );
};