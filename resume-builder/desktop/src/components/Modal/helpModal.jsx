import React from 'react';
import Modal from 'react-modal';
import './helpModal.scss'
import {getTitleCase} from "../../services/getTitleCase";

Modal.setAppElement(document.getElementById('react-app'));


export default class HelpModal extends React.Component {
    constructor(props) {
        super(props);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/';
        this.handleFeedback = this.handleFeedback.bind(this);
        this.onTextChange = this.onTextChange.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.state = {
            feedbackText: '',
            showWarning: false
        }
    }

    closeModal() {
        this.setState({
            feedbackText: '',
            'showWarning': false
        });
        this.props.hideHelpModal();
    }


    handleFeedback(event) {
        event.preventDefault();
        const {firstName, lastName, number: phoneNumber, email: emailId} = this.props;

        if (!this.state.feedbackText) {
            this.setState({
                'showWarning': true
            });
            return;
        }
        const feedbackObj = {
            name: getTitleCase(firstName, lastName),
            email: emailId,
            msg: this.state.feedbackText,
            number: phoneNumber,
            lsource: 8
        };

        this.props.submitFeedback(feedbackObj)

        this.setState({
            feedbackText: '',
            showWarning: false

        })

        this.props.hideHelpModal();
    }

    onTextChange(event) {
        this.setState({
            feedbackText: event.target.value,
            showWarning: false
        })
    }

    render() {
        const {modalStatus, hideHelpModal} = this.props
        const {showWarning} = this.state
        return (
            <div className="pr">
                <Modal
                    isOpen={modalStatus}
                    onRequestClose={this.closeModal}
                    contentLabel="Help Modal"
                    className="help-modal1"
                >
                    <form>
                        <div className="pr help-modal">
                            <React.Fragment>
                                <i onClick={this.closeModal}
                                   className='icon-close icon-close--position1'/>
                                <h2>Reach out to us</h2>
                                <p>Let us know your feedback and suggestions, so we can help you build a powerful
                                    resume. </p>
                                <textarea rows="10" className="mb-20" placeholder="Message"
                                          onChange={this.onTextChange}/>
                                 {
                            showWarning && <span className={"warn-msg-help"}>Please provide some feedback message.</span>
                        }
                                <button className="orange-button"
                                        type={'submit'} onClick={this.handleFeedback}>Submit
                                </button>
                            </React.Fragment>
                        </div>
                    </form>
                </Modal>
            </div>
        );
    }
}
