import React, {Component} from 'react';

export default class SavePreviewButtons extends Component { 

    constructor(props){
        super(props);
        this.preview = this.preview.bind(this);
        this.eventActionClick = this.eventActionClick.bind(this);
    }

    async preview(){
        const {history,updateInfoBeforeLoss,context,eventClicked} = this.props
        await updateInfoBeforeLoss()
        context.setState({submit:true})
        history.push(`/resume-builder/preview`);
        eventClicked({
            'action':'Preview',
            'label':'Bottom'
        })
    }

    eventActionClick(option){
        const {eventClicked,form_name} = this.props;
        eventClicked({
            'action':option ===1 ? 'Save Changes' : option===2 ?'Download': 'Save&Continue',
            'label':option===3 ? form_name : 'Click'
        })
    }

    render (){
        const {showAlertModal,nextEntity,order_data} = this.props;
        const newUser = localStorage.getItem('newUser')
        return (
            <div className="flex-container items-right mr-20 mb-30">
                <button className="blue-button mr-10" type={"button"} onClick={newUser ? showAlertModal: this.preview}>Preview</button>
                <button className="orange-button" type="submit" onClick={()=>{
                    order_data && order_data.id && !nextEntity ? this.eventActionClick(1) : !nextEntity ? this.eventActionClick(2) : this.eventActionClick(3)
                }}>
                    { order_data && order_data.id && !nextEntity ? 'Save Changes' : !nextEntity ? "Download" :'Save and Continue'}
                </button>
            </div>
        )
    }
}