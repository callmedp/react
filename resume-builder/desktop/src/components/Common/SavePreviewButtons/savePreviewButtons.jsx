import React, {Component} from 'react';
import { getTrackingInfo, isTrackingInfoAvailable } from '../../../Utils/common';
import { connect } from 'react-redux';
import { trackUser } from '../../../store/tracking/actions/index'; 
class SavePreviewButtons extends Component { 

    constructor(props){
        super(props);
        this.preview = this.preview.bind(this);
        this.eventActionClick = this.eventActionClick.bind(this);
        this.sendTrackingInfo = this.sendTrackingInfo.bind(this);
        this.handleSaveClick = this.handleSaveClick.bind(this);

    }

    async preview(){
        const {history,updateInfoBeforeLoss,context,eventClicked} = this.props
        this.sendTrackingInfo('right_section_review_button',1);
        await updateInfoBeforeLoss()
        context.setState({submit:true})
        history.push(`/resume-builder/preview`);
        eventClicked({
            'action':'Preview',
            'label':'Bottom'
        })
    }


    sendTrackingInfo(action, position) {
        if (isTrackingInfoAvailable()) {
            const { trackingId, productTrackingMappingId, productId } = getTrackingInfo();
            const {userTrack} = this.props;
            userTrack({ trackingId, productTrackingMappingId, productId, action, position });
        }
    }

    eventActionClick(option){
        const {eventClicked,form_name} = this.props;
        eventClicked({
            'action':option ===1 ? 'Save Changes' : option===2 ?'Download': 'Save&Continue',
            'label':option===3 ? form_name : 'Click'
        })
    }

    handleSaveClick(order_data, nextEntity){
        const { sendTrackingInfo } = this.props;
        nextEntity ? sendTrackingInfo('right_section_save_and_continue',1) : !order_data ? sendTrackingInfo('right_section_download',1) : sendTrackingInfo('right_section_save_changes',1); 
        order_data && order_data.id && !nextEntity ? this.eventActionClick(1) : !nextEntity ? this.eventActionClick(2) : this.eventActionClick(3)
    }

    render (){
        const {showAlertModal,nextEntity,order_data} = this.props
        const newUser = localStorage.getItem('newUser')
        return (
            <div className="flex-container items-right mr-20 mb-30">
                <button className="blue-button mr-10" type={"button"} onClick={newUser ? showAlertModal: this.preview}>Preview</button>
                <button className="orange-button" type="submit" onClick={()=> this.handleSaveClick(order_data, nextEntity)}>
                    { order_data && order_data.id && !nextEntity ? 'Save Changes' : !nextEntity ? "Download" :'Save and Continue'}
                </button>
            </div>
        )
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
    "userTrack": (data) =>  {
        return  dispatch(trackUser(data))
      },
    }
}

export default connect(null,mapDispatchToProps)(SavePreviewButtons);