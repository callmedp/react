import Modal from 'react-modal';
import React from 'react';

export default class PreviewResumeModal extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            showModal: false
        };
    }

    render() {
        const {closeModal, showModal, html} = this.props;
        return (
            <div>
                <Modal
                    isOpen={showModal}
                    contentLabel="Minimal Modal Example"
                >
                    <div style="width:100%;" dangerouslySetInnerHTML={{__html: html}}>

                    </div>
                    <button onClick={closeModal}>CLOSE</button>
                </Modal>
            </div>
        );
    }
}