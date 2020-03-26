import React from 'react';
import './callToAction.scss';
import { Link } from 'react-router-dom';

export default function CallToActionScore() {
    return(
        <div className="call-to-action">
            <div className="d-flex justify-content-between">
                <Link to="/get-expert-form" className="d-flex align-items-center file-upload btn btn-yellow btn-round-30 fs-11 mr-10 px-20">
                    <i className="sprite mr-5"></i>
                    Get expert help
                </Link>


                <div className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20">
                    <i className="sprite upload mr-5"></i> Upload new resume                            
                    <input className="file-upload__input_left" type="file" name="file"></input>
                </div>

                
            </div>
        </div>
    );
}