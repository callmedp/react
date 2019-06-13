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
        const {ui: {alertModal}, nextLink, newUser,isPreview} = this.props;
        return (
            <React.Fragment>
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
                        shouldCloseOnOverlayClick={false}
                    >
                            {newUser ?
                                <div className="pr">
                                    <div className="alert-modal">
                                        <span className="icon-alert"></span>
                                        <p className="mb-3"><strong>Please save your profile info to continue</strong>
                                        </p>
                                        <div className="flex-container">
                                            <button className="blue-button" onClick={this.closeModal}>OK</button>
                                        </div>
                                    </div>
                                </div> :
                            isPreview ?
                                <div className="pr">
                                    <div className="alert-modal">
                                        <span className="icon-alert"></span>
                                        <strong>You Cannot Move this Section</strong>
                                        <p>Moving this section will render bad resume.</p>
                                        <div className="flex-container">
                                            <button className="orange-button mr-10"
                                                    onClick={() => {
                                                        this.closeModal();
                                                    }
                                                    }>Ok
                                            </button>
                                        </div>
                                    </div>
                                </div>
                                :
                                <div className="pr">
                                    <div className="alert-modal">
                                        <span className="icon-alert"></span>
                                        <strong>Are you sure?</strong>
                                        <p>Some information may be lost as required fields are not filled.</p>
                                        <div className="flex-container">
                                            <button className="orange-button mr-10"
                                                    onClick={() => {
                                                        this.props.history.push(nextLink);
                                                        this.closeModal();
                                                    }
                                                    }>Yes, changes it!
                                            </button>
                                            <button className="blue-button" onClick={this.closeModal}>Cancel</button>
                                        </div>
                                    </div>
                                </div>
                            }
                    </Modal>
                </div>


            </React.Fragment>
        )
            ;
    }
}