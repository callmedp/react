import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import './callToAction.scss';
import Swal from 'sweetalert2';
import * as Actions from '../../../../stores/homePage/actions/index';
import Loader from '../../../Common/Loader/loader';
import { Redirect } from 'react-router';


export default function CallToAction() {

    const [flag, setFlag] = useState(true);
    const [visible, setVisible] = useState(false);
    const [filename, setFileName] = useState('Upload Resume');

    const dispatch = useDispatch();
    const fileUpload = async event => {
        setVisible(!visible)
        const file = event.target.files[0];
        if((file.name.slice(-4)=='.pdf' || file.name.slice(-4)=='.txt' || file.name.slice(-4)=='.doc' || file.name.slice(-5)=='.docx') && (file.size/(1024*1024)<=5)){
            setFileName('Uploading File...')
            let response = await new Promise((resolve, reject) => {
                dispatch(Actions.uploadFile({file, resolve, reject}));
            })
            if (response == undefined){
                Swal.fire({
                    icon : 'error',
                    title : 'Something went wrong. Please re-upload your Resume'
                })
                setFileName("Upload Resume")
                setVisible(false)
            }
            else {setFlag(!flag)}
        }
        else{
            Swal.fire({
                icon: 'error',
                title: 'Please Upload PDF, DOC, DOCX, TXT file only'
              })
        }
    }

    // const scoreValue = useSelector(state => state.score)

    return(
        <div className="call-to-action">
        <div className="d-flex justify-content-between">
            {
                flag &&
                <React.Fragment>
                    <div className="d-flex align-items-center file-upload btn btn-yellow btn-round-30 fs-11 mr-10 px-20">
                        <i className="sprite upload mr-5"></i> { filename }                               
                        <input className="file-upload__input_right" type="file" name="file" onChange={fileUpload}></input>
                    </div>
                    {
                        visible &&
                        <Loader />
                    }
                </React.Fragment>
                ||
                <Redirect to="/score-checker" />
            }
            
            <a href="#" className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20">
                <i className="sprite export mr-5"></i>
                Import from shine.com
            </a>
        </div>
    </div>
    );
}
