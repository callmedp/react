import React, {Component} from 'react';
import './bottom-ctc.scss';

export default class BottomCTC extends Component { 

    constructor(props){
        super(props);
        this.preview = this.preview.bind(this);
    }

    async preview(){
        const {history,updateInfoBeforeLoss,context} = this.props
        await updateInfoBeforeLoss()
        context.setState({submit:true})
        history.push(`/resume-builder/preview`);
    }

    render (){
        const {disabled,length,pos,order_data,updateAlertModalStatus} = this.props
        const newUser = localStorage.getItem('newUser')
        return (
            <div>
                <div className="bottom-ctc">
                    <button className="btn link-color bg-white" 
                        onClick={ newUser ? ()=>{updateAlertModalStatus(true)}:this.preview}
                        type={'button'}>Preview
                    </button>
                    
                    <button className="btn btn__primary" disabled={disabled} type={'submit'}>
                        {(length === pos) ? order_data ? "Save Changes":"Buy" :"Save & Continue"}
                    </button>
                </div>
            </div>
        )
    }
}