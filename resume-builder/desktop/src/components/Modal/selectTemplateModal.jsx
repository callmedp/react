import React, {Component} from 'react';
import Modal from 'react-modal';
import ResumeSlider from '../Core/Home/ResumeSlider/resumeSlider';
import './selectTemplateModal.scss'

if (typeof document !== 'undefined') {

    Modal.setAppElement(document.getElementById('react-app'));

}
export default class SelectTemplateModal extends Component {

    render() {
        const {page} = this.props
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