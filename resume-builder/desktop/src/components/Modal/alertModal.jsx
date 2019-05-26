import React from 'react';
import Modal from 'react-modal';
import './alertModal.scss'

Modal.setAppElement(document.getElementById('react-app'));


// Make sure to bind modal to your appElement (http://reactcommunity.org/react-modal/accessibility/)

export default class AlertModal extends React.Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
        this.closeModal = this.closeModal.bind(this);
    }

    closeModal() {
        this.props.hideAlertModal()
    }

    render() {
        const {ui: {alertModal}} = this.props;
        return (
            <div className="pr alert-modal">

                <Modal
                    style={{
                        content: {
                            left: '0',
                            right: '0',
                            top: '10%',
                            bottom: '0',
                            width: '450px',
                            margin: 'auto',
                            height: '280px',
                        }
                    }}
                    isOpen={alertModal}
                    onRequestClose={this.closeModal}
                    contentLabel="Example Modal"
                >
                    <div className="pr">
                        <i onClick={this.closeModal} className='icon-close icon-close--position'></i>

                        <div className="alert-modal">
                            <span className="icon-alert"></span>
                            <strong>Are you sure?</strong>
                            <p>Some information may be lost as required fields are not filled.</p>
                            <div class="flex-container">
                                <button className="orange-button mr-10">Yes, changes it!</button>
                                <button className="blue-button">Cancel</button>
                            </div>
                        </div>
                    </div>
                </Modal>
            </div>
            /*<div className="pr alert-modal">

                <Modal
                    style={{
                        content: {
                            left: '0',
                            right: '0',
                            top: '10%',
                            bottom: '0',
                            width: '450px',
                            margin: 'auto',
                            height: '280px',
                        }
                    }}
                    isOpen={alertModal}
                    onRequestClose={this.closeModal}
                    contentLabel="Example Modal"
                >
                    <div className="pr">
                        <i onClick={this.closeModal} className='icon-close icon-close--position'></i>

                        <div className="alert-modal">
                            <span className="icon-alert"></span>
                            <p>Do you really want to <strong>remove this section?</strong></p>
                            <div class="flex-container">
                                <button className="orange-button mr-10">Confirm</button>
                                <button className="blue-button">Cancel</button>
                            </div>
                        </div>
                    </div>
                </Modal>
            </div>*/
        );
    }
}