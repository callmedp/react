import React, {useState} from 'react';
import { useDispatch } from 'react-redux';
import { Redirect } from 'react-router';
import './callToAction.scss';
import * as Actions from '../../../../stores/scorePage/actions/index';
import GetExpertForm from '../../Forms/GetExpertForm/getExpertForm';
import Loader from '../../../Common/Loader/loader';
import { Toast } from '../../../../services/Toast';

export default function CallToActionScore() {
    const [isFormVisible, setIsFormVisible] = useState(false);
    const toggle = () => setIsFormVisible(!isFormVisible)

    const [flag, setFlag] = useState(true);
    const [visible, setVisible] = useState(false);
    const [filename, setFileName] = useState('Upload New Resume');

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
                    Toast('error', 'Unable to parse your resume. Please upload a new resume')
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
    
    return (
    <div className="call-to-action">
            <div className="d-flex justify-content-between">
                <button className="d-flex align-items-center file-upload btn btn-yellow btn-round-30 fs-11 mr-10 px-20" onClick={toggle}>
                    <i className="sprite mr-5"></i>
                    Get expert help
                </button>

                <div className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20">
                    <i className="sprite upload mr-5"></i> { filename }                            
                    <input className="file-upload__input_left" type="file" name="file" onChange = { fileUpload }></input>
                </div>
            
                {
                    flag &&
                    <React.Fragment>
                        {
                            visible &&
                            <Loader />
                        }
                    </React.Fragment>
                    ||
                    <Redirect to="/score-checker" />
                }
                <GetExpertForm isFormVisible={isFormVisible} hide={toggle}/>
            </div>
        </div>
    );
  };