import React, { Component } from 'react';
import './bottom-ctc.scss';
import { isTrackingInfoAvailable, getTrackingInfo} from '../../../Utils/common';
import { connect } from 'react-redux';
import { trackUser } from '../../../store/tracking/actions/index';
import propTypes from 'prop-types';
class BottomCTC extends Component {

    constructor(props) {
        super(props);
        this.preview = this.preview.bind(this);
        this.eventActionClick = this.eventActionClick.bind(this);
        this.sendTrackingInfo = this.sendTrackingInfo.bind(this);
    }

    sendTrackingInfo(action, pos) {
        if (isTrackingInfoAvailable()) {
            const { trackingId, productTrackingMappingId, productId,
                triggerPoint, uId, utmCampaign } = getTrackingInfo();
            const {userTrack} = this.props;
            let { position } = getTrackingInfo() 
            if(position === ""){
                position = pos;
            }
            userTrack({ trackingId, productTrackingMappingId, productId, action, position,
                triggerPoint, uId, utmCampaign });
        }
    }
    
    async preview() {
        const { history, updateInfoBeforeLoss, context, eventClicked } = this.props

        this.sendTrackingInfo('bottom_preview',1)

        eventClicked({
            'action': 'Preview',
            'label': 'Bottom'
        })
        await updateInfoBeforeLoss()
        context.setState({ submit: true })
        history.push(`/resume-builder/preview`);
    }
    
    eventActionClick(option) {
        const { eventClicked, form_name } = this.props;
        option === 1 ? this.sendTrackingInfo('bottom_save_changes',1) : option === 2 ? this.sendTrackingInfo('bottom_dowload',1) : this.sendTrackingInfo('bottom_save_and_continue',1)

        eventClicked({
            'action': option === 1 ? 'Save Changes' : option === 2 ? 'Download' : 'Save&Continue',
            'label': option === 3 ? form_name : 'Click'
        })
    }
    
    render() {
        const { disabled, length, pos, order_data, updateAlertModalStatus } = this.props
        const newUser = localStorage.getItem('newUser')
        return (
            <div>
            <div className="bottom-ctc">
            <button className="btn link-color bg-white"
            onClick={newUser ? () => { updateAlertModalStatus(true) } : this.preview}
            type={'button'}>Preview
            </button>
            
            <button className="btn btn__primary" disabled={disabled} type={'submit'}
            onClick={() => {
                (length === pos) ? order_data && order_data.id && (localStorage.getItem('subscriptionActive') && localStorage.getItem('subscriptionActive') === 'true' ? true : false) ? this.eventActionClick(1) : this.eventActionClick(2) : this.eventActionClick(3)
            }}>
            {(length === pos) ? order_data && order_data.id && (localStorage.getItem('subscriptionActive') && localStorage.getItem('subscriptionActive') === 'true' ? true : false) ? "Save Changes" : "Download" : "Save & Continue"}
            </button>
            </div>
            </div >
            )
        }
}

const mapDispatchToProps = (dispatch) => {
    return{
        "userTrack" : (data) => dispatch(trackUser(data))
    }
}


    
    BottomCTC.propTypes = {
        context:  propTypes.object,
        disabled:  propTypes.bool,
        eventClicked: propTypes.func,
        form_name: propTypes.string,
        history: propTypes.shape({
            action: propTypes.string,
            block: propTypes.func,
            createHref: propTypes.func,
            go: propTypes.func,
            goBack: propTypes.func,
            goForward: propTypes.func,
            length: propTypes.number,
            listen: propTypes.func,
            location: propTypes.shape({
                hash: propTypes.string,
                pathname: propTypes.string,
                search: propTypes.string,
                state: undefined
            }),
            push: propTypes.func,
            replace: propTypes.func, 
        }),
        length: propTypes.number,
        order_data: propTypes.object,
        pos: propTypes.number,
        updateAlertModalStatus: propTypes.func,
        updateInfoBeforeLoss: propTypes.func
    }


    export default connect(null, mapDispatchToProps)(BottomCTC);