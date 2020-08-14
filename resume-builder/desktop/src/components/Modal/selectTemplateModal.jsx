import React, {Component} from 'react';
import Modal from 'react-modal';
import ResumeSlider from '../Core/Home/ResumeSlider/resumeSlider';
import './selectTemplateModal.scss';
import propTypes from 'prop-types';

if (typeof document !== 'undefined') {

    Modal.setAppElement(document.getElementById('react-app'));

}
export default class SelectTemplateModal extends Component {
    render() {
        const {page} = this.props;
        return (
            <Modal
                isOpen={this.props.ui.select_template_modal}
                contentLabel="onRequestClose"
                onRequestClose={this.handleCloseModal}
                className="Modal"
                overlayClassName="Overlay">
                <ResumeSlider   {...this.props} page={page}/>
                <button className="Modal--close" onClick={() => {
                    this.props.hideSelectTemplateModal()
                }}>+
                </button>
            </Modal>
        )
    }
}

SelectTemplateModal.propTypes = {
    hideSelectTemplateModal: propTypes.func,
    ui: propTypes.shape({
        alertModal: propTypes.bool,
        alertType: propTypes.string,
        formName: propTypes.string,
        generateResumeModal: propTypes.bool,
        helpModal: propTypes.bool,
        loader: propTypes.bool,
        loginModal: propTypes.bool,
        modal: propTypes.bool,
        previewClicked: propTypes.bool,
        select_template_modal: propTypes.bool,
        showMoreSection: propTypes.bool,
        successLogin: propTypes.bool,
        suggestionModal: propTypes.bool,
        suggestionType: propTypes.string,
        suggestions: propTypes.array,
    }),
    page: propTypes.string
}