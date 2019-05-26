import React from 'react';
import Modal from 'react-modal';
import './templateModal.scss'

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
            <div className="pr">

                <Modal
                    style={{
                        content: {
                            left: '10%',
                            right: '10%',
                            top: '15%',
                            bottom: '0',
                        }
                    }}
                    isOpen={alertModal}
                    onRequestClose={this.closeModal}
                    contentLabel="Example Modal"
                >
                    <div className="pr">
                        <i onClick={this.closeModal} className='icon-close icon-close--position'></i>

                        <div>
                            Alert Message here
                        </div>
                    </div>
                </Modal>
            </div>
        );
    }
}