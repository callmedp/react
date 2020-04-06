import React, {useState} from 'react';
import './callToAction.scss';
import GetExpertForm from '../../Forms/GetExpertForm/getExpertForm';

export default function CallToActionScore() {
    const [isVisible, setIsVisible] = useState(false);
    const toggle = () => setIsVisible(!isVisible)
    return (
        <div>
            <div className="call-to-action">
                <div className="d-flex justify-content-between">
                    <button className="d-flex align-items-center file-upload btn btn-yellow btn-round-30 fs-11 mr-10 px-20" onClick={toggle}>
                        <i className="sprite mr-5"></i>
                        Get expert help
                    </button>


                    <div className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20">
                        <i className="sprite upload mr-5"></i> Upload new resume                            
                        <input className="file-upload__input_left" type="file" name="file"></input>
                    </div>
                </div>
            </div>
            <GetExpertForm isVisible={isVisible} hide={toggle}/>
        </div>
    );
  };