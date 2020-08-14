import React, {Component} from 'react';
import {connect} from "react-redux";
import {hideSubscribeButton} from '../../../../store/personalInfo/actions/index';
import {updateAlertModalStatus} from '../../../../store/ui/actions/index';
import './rightSection.scss'
import moment from 'moment';
import propTypes from 'prop-types';

class Subscribe extends Component {
    constructor(props) {
        super(props);
        this.redirectToBuyPage = this.redirectToBuyPage.bind(this);
        this.hideSubscribeButton = this.hideSubscribeButton.bind(this);
        this.state = {
            showSubscribeButton: true
        }
    }

    hideSubscribeButton() {
        localStorage.setItem('buttonHideDuration', moment().valueOf().toString())
        this.setState({
            showSubscribeButton: false
        })
    }

    componentDidMount() {
        let startTime = localStorage.getItem('buttonHideDuration'), validDate = false, duration;

        if (startTime) validDate = (new Date(Number(startTime))).getTime() > 0;

        if (startTime && validDate) {
            duration = moment().diff(moment(Number(startTime)), 'hours');
            if (duration < 72) {
                this.setState({
                    showSubscribeButton: false
                })
            } else {
                localStorage.removeItem('buttonHideDuration')
            }
        }
    }

    redirectToBuyPage() {
        const {history, eventClicked} = this.props;
        eventClicked({
            'action': 'SubscribeNow',
            'label': 'Click'
        })
        history.push('/resume-builder/buy');
    }

    render() {
        const {showSubscribeButton} = this.state;
        const {updateAlertModalStatus, userInfo: {order_data}} = this.props;
        if (!showSubscribeButton || (((order_data && order_data.id)) && (localStorage.getItem('subscriptionActive') && localStorage.getItem('subscriptionActive') === 'true' ? true : false)))  return null;
        const newUser = localStorage.getItem('newUser');


        return (
            <div>
                <div className="buildResume__subscribe">
                    <p className="buildResume__subscribe--text">Subscribe now, create later</p>
                    <a onClick={() => newUser ? updateAlertModalStatus(true) : this.redirectToBuyPage()}
                       className="btn btn__sm btn__round btn--outline">Subscribe</a>
                    <a className="close" href="javascript:void(0)" onClick={this.hideSubscribeButton}>+</a>
                </div>
            </div>
        )
    }
}

Subscribe.propTypes = {
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
    eventClicked: propTypes.func, 
    updateAlertModalStatus: propTypes.func,
    userInfo: propTypes.shape({
        active_subscription: propTypes.bool,
        candidate_id: propTypes.string,
        date_of_birth: propTypes.string,
        email: propTypes.string,
        entity_preference_data: propTypes.array,
        extra_info: propTypes.string,
        extracurricular: propTypes.array,
        first_name: propTypes.string,
        free_resume_downloads: propTypes.number,
        gender: propTypes.string,
        id: propTypes.number,
        image: propTypes.string,
        interest_list: propTypes.array,
        last_name: propTypes.string,
        location: propTypes.string,
        number: propTypes.string,
        selected_template: propTypes.string,
    }),
}


const mapStateToProps = (state) => {
    return {
        ui: state.ui,
        userInfo: state.personalInfo
    }
}
const mapDispatchToProps = (dispatch) => {
    return {
        'hideSubscribeButton': () => {
            return dispatch(hideSubscribeButton())
        },
        'updateAlertModalStatus': (data) => {
            return dispatch(updateAlertModalStatus(data))
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Subscribe)


