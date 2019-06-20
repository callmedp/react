import React, {Component} from 'react';

export default class SavePreviewButtons extends Component { 

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
        const {showAlertModal,nextEntity,order_data} = this.props
        const newUser = localStorage.getItem('newUser')
        return (
            <div className="flex-container items-right mr-20 mb-30">
                <button className="blue-button mr-10" type={"button"} onClick={newUser ? showAlertModal: this.preview}>Preview</button>
                <button className="orange-button" type="submit">{ order_data && order_data.id ? 'Save Changes' : !nextEntity ? "Download" :'Save and Continue'}
                </button>
            </div>
        )
    }
}