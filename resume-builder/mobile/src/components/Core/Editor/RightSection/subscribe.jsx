import React, {Component} from 'react';
import {connect} from "react-redux";
import {hideSubscribeButton} from '../../../../store/personalInfo/actions/index';
import './rightSection.scss'
import moment from 'moment';


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
        if (!showSubscribeButton) return null;
        return (
            <div>
                <div className="buildResume__subscribe">
                    <p className="buildResume__subscribe--text">Subscribe now create later</p>
                    <a onClick={this.redirectToBuyPage} className="btn btn__sm btn__round btn--outline">Subscribe</a>
                    <a className="close" href="javascript:void(0)" onClick={this.hideSubscribeButton}>+</a>
                </div>
            </div>
        )
    }
}


const mapStateToProps = (state) => {
    return {
        ui: state.ui
    }
}
const mapDispatchToProps = (dispatch) => {
    return {
        'hideSubscribeButton': () => {
            return dispatch(hideSubscribeButton())
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(Subscribe)


