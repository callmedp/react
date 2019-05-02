import React from 'react';
import Modal from 'react-modal';

Modal.setAppElement(document.getElementById('react-app'));


// Make sure to bind modal to your appElement (http://reactcommunity.org/react-modal/accessibility/)

export default class TemplateModal extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            modalIsOpen: false
        };
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
        this.openModal = this.openModal.bind(this);
        this.closeModal = this.closeModal.bind(this);
    }

    static getDerivedStateFromProps(nextProps, prevState) {
        const {ui: {modal}} = nextProps;
        if (prevState.modalIsOpen !== modal) {
            return ({
                modalIsOpen: modal
            })
        }
    }


    openModal() {
        this.setState({modalIsOpen: true});
    }

    closeModal() {
        this.props.hideModal()
    }

    render() {
        return (
            <div>
                <Modal
                    style={{
                        content: {
                            left: '10%',
                            right: '10%',
                            bottom: 'auto',
                        }
                    }}
                    isOpen={this.state.modalIsOpen}
                    onRequestClose={this.closeModal}
                    contentLabel="Example Modal"
                >
                    <div>
                        <i onClick={this.closeModal} className='icon-close'></i>
                        <img src={`${this.staticUrl}react/assets/images/resume1_Preview.jpg`}/>
                    </div>
                </Modal>
            </div>
        );
    }
}