import React from 'react';
import Modal from 'react-modal';
import './helpModal.scss'
import {getTitleCase} from "../../services/getTitleCase";

if (typeof document !== 'undefined') {

    Modal.setAppElement(document.getElementById('react-app'));

}
export default class HelpModal extends React.Component {

     constructor(props) {
        super(props);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/';
        this.handleFeedback = this.handleFeedback.bind(this);
        this.onTextChange = this.onTextChange.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.state = {
            feedbackText: '',
            'errorMessage': '',
            'isError': false
        }
    }

     closeModal() {
        this.setState({
            feedbackText: '',
            isError: false,
            errorMessage: ''
        });
        this.props.hideHelpModal();
    }
    handleFeedback(event) {
        event.preventDefault();
        const {feedback, userInfo, hideHelpModal, eventClicked} = this.props;

        const feedbackObj = {
            name: userInfo.first_name,
            email: userInfo.email,
            msg: this.state.feedbackText,
            number: userInfo.number,
            lsource: 8
        };

        if (!this.state.feedbackText) {
            this.setState({
                errorMessage: 'Please provide us some information.',
                isError: true
            });
            return;
        }

        feedback(feedbackObj);


        eventClicked({
            'action': 'LeadSubmit',
            'label': 'Header'
        })
        this.setState({
            feedbackText: '',
            isError: false,
            errorMessage: ''
        })

        hideHelpModal();
    }

     onTextChange(event) {
        this.setState({
            feedbackText: event.target.value,
            isError: false,
            errorMessage: ''
        })
    }

    render() {
        const {modalStatus, hideHelpModal} = this.props
        const {errorMessage, isError} = this.state;
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
                                    !!(isError) &&
                                    <span className="help-message-error">{errorMessage}</span>
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
