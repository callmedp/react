import React, {Component} from 'react'
import './topBar.scss'

export default class TopBar extends Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
        this.changeTemplate = this.changeTemplate.bind(this);
        this.redirectToBuyPage = this.redirectToBuyPage.bind(this);
    }

    redirectToBuyPage() {
        const {history, eventClicked} = this.props;
        eventClicked({
            'action': 'SubscribeNow',
            'label': 'Click'
        })
        history.push('/resume-builder/buy');
    }

    changeTemplate() {
        const {showSelectTemplateModal, eventClicked} = this.props;
        showSelectTemplateModal();
        let eventData = {
            'action': 'ChangeTemplate',
            'label': 'ResumeCreation'
        }
        eventClicked(eventData);
    }

    render() {
        let {page, userInfo: {selected_template, order_data}, showAlertModal} = this.props;
        if (localStorage.getItem('selected_template')) {
            selected_template = localStorage.getItem('selected_template')
        }
        const newUser = localStorage.getItem('newUser')
        return (
            <section className="flex-container">
                <div className="top-banner">
                    {
                        page === 'buy' ?
                            <div className="top-banner--banner-txt pr">
                                <h1>Your customised resume is ready!</h1>
                                <p>Buy more templates and save more </p>
                                <span class="launch-offer"></span>
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
                                            <span>( You can also subscribe <br/>now and create resume later)</span> : ""}</p>
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
                                !(order_data && order_data.id) ?
                                    <div className="top-banner--banner-right">
                                        <div>
                                            <button className="orange-button mr-10"
                                                    onClick={() => newUser ? showAlertModal() : this.redirectToBuyPage()}>Subscribe
                                                now
                                            </button>
                                            <button className="white-button mr-20" onClick={() => {
                                                newUser ? showAlertModal() : this.changeTemplate()
                                            }}>Change template
                                            </button>
                                        </div>
                                        <span className="top-banner--banner-right--banner-thumb">
                                    <img
                                        src={`${this.staticUrl}react/assets/images/resume-thumb-${selected_template}.jpg`}
                                        alt=""/>
                		            </span>
                                    </div> :
                                    (order_data && order_data.id && order_data.isCombo) ?
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
                                        alt=""/>
                		            </span>
                                        </div> : ""
                    }
                </div>
            </section>
        )
    }
}