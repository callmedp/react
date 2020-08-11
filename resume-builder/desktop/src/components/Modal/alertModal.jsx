import React, {Component, PureComponent} from 'react';
import Modal from 'react-modal';
import './alertModal.scss'
import { withRouter } from 'react-router-dom';
import propTypes from 'prop-types';

if(typeof document !== 'undefined') {
    Modal.setAppElement(document.getElementById('react-app'));
}

// Make sure to bind modal to your appElement (http://reactcommunity.org/react-modal/accessibility/)

class AlertModal extends PureComponent {
    static propTypes = {
        hideAlertModal: propTypes.func,
        alertModal: propTypes.bool,
        history: propTypes.shape({
            action: propTypes.string,
            block: propTypes.func,
            createHref: propTypes.func,
            go: propTypes.func,
            goBack: propTypes.func,
            goForward: propTypes.func,
            length: propTypes.number,
            listen: propTypes.func,
            location: propTypes.shape({
                hash: propTypes.string,
                pathname: propTypes.string,
                search: propTypes.string,
                state: undefined
            }),
            push: propTypes.func,
            replace: propTypes.func, 
        }),
        nextLink: propTypes.string,
        newUser: propTypes.func ,
        isPreview: propTypes.bool
    }

    constructor(props) {
        super(props);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
        this.closeModal = this.closeModal.bind(this);
    }


    closeModal() {
        this.props.hideAlertModal()
    }

    render() {
        const {alertModal, generateResumeModal, nextLink, newUser, isPreview} = this.props;
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
                        isOpen={alertModal || generateResumeModal}
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
                            generateResumeModal ?
                            <div className="pr">
                                <div className="alert-modal margin-top-alert">
                                    <strong>Generating Resume</strong>
                                    <p>Your resume is being generated. Please wait..</p>
                                    <div className="logo-center">
                                        <img src={`${this.staticUrl}react/assets/images/blue-loader.png`}/>
                                    </div> 
                                </div>
                            </div>:
                            isPreview  ?
                                <div className="pr">
                                    <div className="alert-modal">
                                        <span className="icon-alert"></span>
                                        <strong>Sorry, this section cannot be moved.</strong>
                                        <p>This is to ensure the best look for your resume.</p>
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
                                                    }>Yes, change it.
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

export default withRouter(AlertModal) 