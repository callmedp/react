import React, {Component} from 'react';
import Modal from 'react-modal';
import './NeedHelpModal.scss'
import {getTitleCase} from "../../../../services/getTitleCase";
if(typeof document !== 'undefined') {
    Modal.setAppElement(document.getElementById('react-app'));
}

export default class NeedHelpModal extends Component {

    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
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
            'errorMessage': '',
            'isError': false
        });
        this.props.hideHelpModal();
    }


    handleFeedback(event) {
        event.preventDefault();
        const {feedback,personalInfo,hideHelpModal,eventClicked} = this.props;


        const feedbackObj = {
            name: personalInfo.first_name,
            email: personalInfo.email,
            msg: this.state.feedbackText,
            number: personalInfo.number,
            lsource: "8"
        };

         if (!this.state.feedbackText) {
            this.setState({
                errorMessage: 'Please provide us some information.',
                isError: true
            });
            return;
        }

        feedback(feedbackObj)

        eventClicked({
            'action':'LeadSubmit',
            'label':'Header'
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
        const {modalStatus} = this.props;
        const {errorMessage, isError} = this.state;
        return (
            <Modal
                isOpen={modalStatus}
                contentLabel="onRequestClose Preview"
                onRequestClose={this.closeModal}
                className="alertModal"
                overlayClassName="Overlay">
                <div className="modal-reachus">
                    <h2>Reach out to us</h2>
                    <p>Let us know your feedback and suggestions, so we can help you build a powerful resume.</p>
                    <div className="form__group mt-20">
                        <textarea rows="6" maxlength="100" className="form__input" onChange={this.onTextChange}></textarea>
                    </div>
                    {
                        !!(isError) &&
                        <span className="help-message-error">{errorMessage}</span>
                    }
                    <div class="text-center">
                        <button className="btn btn__round btn__primary mt-20" onClick={this.handleFeedback}>
                            Submit
                        </button>
                    </div>
                    <span className="close-wrap" onClick={this.closeModal}>
                        <i className="sprite icon--close"></i>
                    </span>
                </div>


            </Modal>
        )
    }
}