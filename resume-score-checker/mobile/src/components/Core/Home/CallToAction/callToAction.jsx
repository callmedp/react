import React, {Component} from 'react';
import './callToAction.scss'

class CallToAction extends Component {
    render() {
        return(
            <div className="call-to-action">
                <div className="d-flex justify-content-between">
                    <div className="d-flex align-items-center file-upload btn btn-yellow btn-round-30 fs-11 mr-10 px-20">
                        <i className="sprite upload mr-5"></i> Upload resume                                
                        <input className="file-upload__input_right" type="file" name="file"></input>
                    </div>
        
                    <a href="#" className="d-flex align-items-center btn btn-outline-white btn-round-30 fs-11 px-20">
                    <i className="sprite export mr-5"></i>
                    Export from shine.com
                    </a>
                </div>
            </div>
        );
    }
}

export default CallToAction;