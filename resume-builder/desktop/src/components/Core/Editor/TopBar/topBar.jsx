import React, { Component, PureComponent } from 'react'
import './topBar.scss'
import { withRouter } from 'react-router-dom';
import propTypes from 'prop-types';

class TopBar extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
        this.changeTemplate = this.changeTemplate.bind(this);
        this.redirectToBuyPage = this.redirectToBuyPage.bind(this);
    }
    
    redirectToBuyPage() {
        const { history, eventClicked } = this.props;
        eventClicked({
            'action': 'SubscribeNow',
            'label': 'Click'
        })
        history.push('/resume-builder/buy');
    }
    
    changeTemplate() {
        const { showSelectTemplateModal, eventClicked } = this.props;
        showSelectTemplateModal();
        let eventData = {
            'action': 'ChangeTemplate',
            'label': 'ResumeCreation'
        }
        eventClicked(eventData);
    }
    
    shouldComponentUpdate(nextProps, nextState) {
        // stop  unnecessary rendering 
        const { page: oldPage, userInfo: { selected_template: oldSelectedTemplate, order_data: oldOrderData, resume_generated: oldResumeGenerated }, showAlertModal: oldAlertModal } = this.props;
        const { page: newPage, userInfo: { selected_template: newSelectedTemplate, order_data: newOrderData, resume_generated: newResumeGenerated }, showAlertModal: newAlertModal } = nextProps;
        if (oldSelectedTemplate !== newSelectedTemplate) return true;
        if (oldResumeGenerated !== newResumeGenerated) return true;
        if (oldPage !== newPage) return true;
        if (oldAlertModal !== newAlertModal) return true;
        if (JSON.stringify(oldOrderData) !== JSON.stringify(newOrderData)) return true;
        return false;
    }
    render() {
        let { page, userInfo: { selected_template, order_data, resume_generated }, showAlertModal } = this.props;
        if (!selected_template && !localStorage.getItem('selected_template')) {
            selected_template = 1;
        }
        const newUser = localStorage.getItem('newUser');
        return (
            <section className="flex-container">
            <div className="top-banner">
            {
                page === 'buy' ?
                <div className="top-banner--banner-txt pr">
                <h1>Your customised resume is ready!</h1>
                <p>Buy more templates and save more </p>
                <span className="launch-offer"></span>
                </div> :
                page === 'download' ?
                <div className="top-banner--banner-txt">
                <h1>Congratulations!</h1>
                <p>Your order is confirmed, download your resume</p>
                </div> :
                <div className="top-banner--banner-txt">
                <h1>You are closer to your perfect resume.</h1>
                <p>Fill the details to create your
                resume {!!(!(order_data && order_data.id)) ?
                    <span>( You can also subscribe <br />now and create resume later)</span> : ""}</p>
                    </div>
                }
                {
                    page === 'download' ?
                    <div className="top-banner--banner-right">
                    
                    <span className="top-banner--banner-right--payment-done ml-0">
                    
                    </span>
                    </div> :
                    page === 'buy' ?
                    '' :
                    !!(!(order_data && order_data.id) || !(resume_generated) || (localStorage.getItem('subscriptionActive') && localStorage.getItem('subscriptionActive') === 'false' ? true : false)) ?
                    <div className="top-banner--banner-right">
                    <div>
                    {
                        < button className="orange-button mr-10"
                        onClick={() => newUser ? showAlertModal() : this.redirectToBuyPage()}>Subscribe
                        now
                        </button>
                        
                    }
                    <button className="white-button mr-20" onClick={() => {
                        newUser ? showAlertModal() : this.changeTemplate()
                    }}>Change template
                    </button>
                    </div>
                    <span className="top-banner--banner-right--banner-thumb">
                    <img
                    src={`${this.staticUrl}react/assets/images/resume-thumb-${selected_template}.jpg`}
                    alt="" />
                    </span>
                    </div> :
                    (order_data && order_data.id && order_data.combo) ?
                    <div className="top-banner--banner-right">
                    <div>
                    <button className="white-button mr-20" onClick={() => {
                        newUser ? showAlertModal() : this.changeTemplate()
                    }}>Change template
                    </button>
                    </div>
                    <span className="top-banner--banner-right--banner-thumb">
                    <img
                    src={`${this.staticUrl}react/assets/images/resume-thumb-${selected_template}.jpg`}
                    alt="" />
                    </span>
                    </div> : (order_data && order_data.id && order_data.expiry && (localStorage.getItem('subscriptionActive') && localStorage.getItem('subscriptionActive') === 'true' ? true : false)) ?
                    <div className="top-banner--banner-right">
                    <div>
                    <button className="white-button mr-20" onClick={() => {
                        newUser ? showAlertModal() : this.changeTemplate()
                    }}>Change template
                    </button>
                    </div>
                    <span className="top-banner--banner-right--banner-thumb">
                    <img
                    src={`${this.staticUrl}react/assets/images/resume-thumb-${selected_template}.jpg`}
                    alt="" />
                    </span>
                    </div> : ''
                }
                </div>
                </section>
                )
            }
        }

        TopBar.propTypes = {
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
            showSelectTemplateModal: propTypes.func,
            userInfo: propTypes.shape({
                order_data: undefined,
                resume_generated: undefined,
                selected_template: propTypes.string,
            }),
            showAlertModal: propTypes.func,
            page: propTypes.string
        }
        
        export default withRouter(TopBar)