import React, {Component} from 'react';
import './bottom-ctc.scss';

export default class BottomCTC extends Component { 
    render (){
        const {savePreview,disabled,length,pos,subscription_status} = this.props
        return (
            <div>
                <div className="bottom-ctc">
                    <button className="btn link-color bg-white" 
                        onClick={savePreview}
                        type={'button'}>Preview
                    </button>
                    
                    <button className="btn btn__primary" disabled={disabled} type={'submit'}>
                        {(length === pos) ? subscription_status ?"Download Resume":"Buy" :"Save & Continue"}
                    </button>
                </div>
            </div>
        )
    }
}