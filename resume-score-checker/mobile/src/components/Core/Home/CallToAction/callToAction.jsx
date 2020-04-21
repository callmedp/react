import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Redirect } from 'react-router-dom';
import './callToAction.scss';
import * as Actions from '../../../../stores/scorePage/actions/index';
import Loader from '../../../Common/Loader/loader';
import { Toast } from '../../../../services/Toast';
import {siteDomain} from '../../../../Utils/domains';


export default function CallToAction() {

    const [flag, setFlag] = useState(true);
    const [visible, setVisible] = useState(false);
    const [filename, setFileName] = useState('Upload Resume');

    useEffect(() => localStorage.getItem("resume_score") === null ? setFileName('Upload Resume') :  setFileName('Upload New Resume'),[])

    const dispatch = useDispatch();
    const fileUpload = async event => {
        setVisible(!visible)
        const file = event.target.files[0];
        event.target.value = null
        if((file.name.slice(-4)==='.pdf' || file.name.slice(-4)==='.txt' || file.name.slice(-4)==='.doc' || file.name.slice(-5)==='.docx') && (file.size/(1024*1024)<=5)){
            setFileName('Uploading File...')
            try{
                let result = await new Promise((resolve, reject) => {
                    dispatch(Actions.uploadFile({file, resolve, reject}));
                })
                if(result['error_message']){
                    Toast('error', result['error_message'])
                    setFileName("Upload Resume")
                    setVisible(false)
                }
                else {
                    localStorage.setItem('resume_file', file.name)
                    setFlag(!flag)
                }
            }
            catch(e){
                Toast('error', 'Something went wrong! Try again')
                setFileName("Upload Resume")
                setVisible(false)
            }
        }
        else{
            Toast('error', 'Please Upload only Pdf, Doc, Docx or txt format file only')
            setVisible(false) 
        }
    }

    const importResume = async () => {
        setVisible(!visible)
        if (!localStorage.getItem('userId')) {
            const isSessionAvailable = await new Promise((resolve, reject) => dispatch(Actions.checkSessionAvailability({resolve, reject})));
           
            if (isSessionAvailable['result']) {
                try{
                    // await new Promise((resolve, reject) => dispatch(Actions.getCandidateId({resolve, reject})))
                    // let resume = await new Promise((resolve, reject) => {
                    //     dispatch(Actions.getCandidateResume({ resolve, reject }));
                    // })
                    setFlag(true);
                    const candidateInfo = await new Promise((resolve, reject) => dispatch(Actions.getCandidateInfo({ resolve, reject })))
                    await new Promise((resolve, reject) => dispatch(Actions.getCandidateScore({ candidateId: candidateInfo['candidate_id'], resolve, reject })))
                    setFlag(false)

                    // fileUpload({target : {files : [resume]}})
                }
                catch(error){
                    //setFlag(false);
                    Toast('error', 'Something went wrong! Try again')
                    setVisible(false)
                }
            }
            else{
                window.location.href = `${siteDomain}/login/?next=resume-score-checker/`
            }
        }
        else{
            try{
                // let resume = await new Promise((resolve, reject) => {
                //     dispatch(Actions.getCandidateResume({ resolve, reject }));
                // })
                // fileUpload({target : { files : [resume] }})
                setFlag(true);
                await new Promise((resolve, reject) => dispatch(Actions.getCandidateScore({ candidateId: localStorage.getItem('userId'), resolve, reject })))
                setFlag(false)
            }
            catch(e){
                //setFlag(false)
                Toast('error', 'Something went wrong! Try again')
                setVisible(false)
            }
        }
    }
    

    return(
        <div className="call-to-action">
        <div className="d-flex justify-content-between">
            <div className="d-flex align-items-center file-upload btn btn-yellow btn-round-30 fs-11 mr-10 px-20">
                <i className="sprite upload mr-5"></i> { filename }                               
                <input className="file-upload__input_right" type="file" name="file" onChange={fileUpload}></input>
            </div>

            <a href = "/" className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20" onClick = {importResume}>
                <i className="sprite export mr-5"></i>
                Import from shine.com
            </a>
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
