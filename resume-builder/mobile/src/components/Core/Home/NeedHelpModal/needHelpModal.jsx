import React, {Component} from 'react';
import Modal from 'react-modal';
import './NeedHelpModal.scss'
import {getTitleCase} from "../../../../services/getTitleCase";


Modal.setAppElement(document.getElementById('react-app'));

export default class NeedHelpModal extends Component {

    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
        this.handleFeedback = this.handleFeedback.bind(this);
        this.onTextChange = this.onTextChange.bind(this);
        this.closeModal = this.closeModal.bind(this);
        this.state = {
            feedbackText: ''
        }
    }

    closeModal() {
        this.setState({
            feedbackText: ''
        });
        this.props.hideHelpModal();
    }


    handleFeedback(event) {
        event.preventDefault();
        const {firstName, lastName, number: phoneNumber, email: emailId} = this.props;

        const feedbackObj = {
            name: getTitleCase(firstName, lastName),
            email: emailId,
            msg: this.state.feedbackText,
            number: phoneNumber,
            lsource: 8
        };

        this.props.submitFeedback(feedbackObj)

        this.setState({
            feedbackText: ''
        })

        this.props.hideHelpModal();
    }

    onTextChange(event) {
        this.setState({
            feedbackText: event.target.value
        })
    }

    render() {
        const {modalStatus} = this.props;
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
                        <textarea rows="6" maxlength="100" class="form__input" onChange={this.onTextChange}></textarea>
                    </div>
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