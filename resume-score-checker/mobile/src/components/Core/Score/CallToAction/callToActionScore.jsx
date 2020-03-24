import React from 'react';

export default function CallToActionScore() {
    return(
        <div className="call-to-action">
            <div className="d-flex justify-content-between">
            <a href="#" className="d-flex align-items-center file-upload btn btn-yellow btn-round-30 fs-11 mr-10 px-20">
                <i className="sprite export mr-5"></i>
                Get expert help
            </a>


                <div className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20">
                    <i className="sprite upload mr-5"></i> Upload new resume    ssdssd                            
                    <input className="file-upload__input" type="file" name="file"></input>
                </div>

                
            </div>
        </div>
    );
}