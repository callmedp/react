import React, { useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { Redirect } from 'react-router';
import './callToAction.scss';
import * as Actions from '../../../../stores/scorePage/actions/index';
import Loader from '../../../Common/Loader/loader';
import { Toast } from '../../../../services/Toast';


export default function CallToAction() {

    const [flag, setFlag] = useState(true);
    const [visible, setVisible] = useState(false);
    const [filename, setFileName] = useState('Upload Resume');

    useEffect(() => localStorage.getItem("resume_score") === null ? setFileName('Upload Resume') :  setFileName('Upload New Resume'),[])

    const dispatch = useDispatch();
    const fileUpload = async event => {
        setVisible(!visible)
        const file = event.target.files[0];
        if((file.name.slice(-4)==='.pdf' || file.name.slice(-4)==='.txt' || file.name.slice(-4)==='.doc' || file.name.slice(-5)==='.docx') && (file.size/(1024*1024)<=5)){
            setFileName('Uploading File...')
            try{
                let result = await new Promise((resolve, reject) => {
                    dispatch(Actions.uploadFile({file, resolve, reject}));
                })
                if(result['status'] === 0){
                    Toast('error', 'Unable to parse your resume. Please upload a new Resume')
                    setFileName("Upload Resume")
                    setVisible(false)
                }
                else {setFlag(!flag)}
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
        if (!localStorage.getItem('candidateId') || !localStorage.getItem('token')) {
            const isSessionAvailable = await new Promise((resolve, reject) => dispatch(Actions.checkSessionAvailability({resolve, reject})));
            if (isSessionAvailable) {
                try{
                    await new Promise((resolve, reject) => dispatch(Actions.getCandidateId({resolve, reject})))
                    let resume = await new Promise((resolve, reject) => {
                        dispatch(Actions.getCandidateResume({ resolve, reject }));
                    })
                    fileUpload({target : {files : [resume]}})
                }
                catch(error){
                    Toast('error', 'Something went wrong! Try again')
                    setVisible(false)
                }
            }
            else{
                window.location.href = 'https://learning.shine.com/login/?next=score-checker'
            }
        }
        else{
            try{
                let resume = await new Promise((resolve, reject) => {
                    dispatch(Actions.getCandidateResume({ resolve, reject }));
                })
                fileUpload({target : { files : [resume] }})
            }
            catch(e){
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

            <a href="#/" className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20" onClick = {importResume}>
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
                <Redirect to="/score-checker" />
            }
        </div>
    </div>
    );
}
