import React from 'react';
import Modal from 'react-modal';
import './templateModal.scss'

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
        const {template: {templateId}} = this.props;
        return (
            <div className="pr">
                {this.state.modalIsOpen &&
                <i onClick={this.closeModal} className='icon-close icon-close--position'></i>
                }
                <Modal
                    style={{
                        content: {
                            left: '10%',
                            right: '10%',
                            top: '15%',
                        }
                    }}
                    isOpen={this.state.modalIsOpen}
                    onRequestClose={this.closeModal}
                    contentLabel="Example Modal"
                >
                    <div>
                        <img className="img-responsive"
                             src={`${this.staticUrl}react/assets/images/resume${templateId || '1'}_preview.jpg`}/>
                    </div>
                </Modal>
            </div>
        );
    }
}