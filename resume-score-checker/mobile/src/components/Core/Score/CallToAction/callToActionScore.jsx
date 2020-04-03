import React, {useState} from 'react';
import { useDispatch } from 'react-redux';
import './callToAction.scss';
import { Link } from 'react-router-dom';
import * as Actions from '../../../../stores/homePage/actions/index';
import GetExpertForm from '../../Forms/GetExpertForm/getExpertForm';

export default function CallToActionScore() {
    const [isVisible, setIsVisible] = useState(false);
    const toggle = () => {
        setIsVisible(!isVisible)
        // setNewFlag(!newFlag)
    }

    const [flag, setFlag] = useState(true);
    const [filename, setFileName] = useState('Upload New Resume');
    const dispatch = useDispatch();
    const fileUpload = async event => {
        const file = event.target.files[0];
        if((file.name.slice(-4)=='.pdf' || file.name.slice(-4)=='.txt' || file.name.slice(-4)=='.doc' || file.name.slice(-5)=='.docx') && (file.size/(1024*1024)<=5)){
            setFileName('Uploading File...')
            let response = await new Promise((resolve, reject) => {
                dispatch(Actions.uploadFile({file, resolve, reject}));
            })
            setFlag(!flag)
        }
        else{
            alert("Please Upload Valid Format File Only")
        }
    }
    return (
    <div className="call-to-action">
            <div className="d-flex justify-content-between">
                <button className="d-flex align-items-center file-upload btn btn-yellow btn-round-30 fs-11 mr-10 px-20" onClick={toggle}>
                    <i className="sprite mr-5"></i>
                    Get expert help
                </button>
            
                {
                    flag &&
                    <div className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20">
                        <i className="sprite upload mr-5"></i> { filename }                            
                        <input className="file-upload__input_left" type="file" name="file" onChange = { fileUpload }></input>
                    </div>
                    ||
                    <Link to = "/score-checker" className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20">
                        &emsp;Check Score&emsp;
                    </Link>
                }
                <GetExpertForm isVisible={isVisible} hide={toggle}/>
            </div>
        </div>
    );
  };