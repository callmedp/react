import React from 'react';
import Modal from 'react-modal';
import './templateModal.scss'
import propTypes from 'prop-types';

if (typeof document !== 'undefined') {
    
    Modal.setAppElement(document.getElementById('react-app'));
}

// Make sure to bind modal to your appElement (http://reactcommunity.org/react-modal/accessibility/)

export default class TemplateModal extends React.Component {
    constructor(props) {
        super(props);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
        this.disableScroll = this.disableScroll.bind(this);
        this.closeModal = this.closeModal.bind(this);
    }
    
    closeModal() {
        this.props.hideModal()
    }
    
    disableScroll() {
        document.body.style.overflow = 'hidden'
    }
    
    
    render() {
        const { templateId, modalTemplateImage, modal, page } = this.props;
        return (
            <div className="pr">
            
            <Modal
            style={{
                content: {
                    left: '10%',
                    right: '10%',
                    top: '10%',
                    bottom: '0',
                }
            }}
            isOpen={modal}
            onRequestClose={this.closeModal}
            contentLabel="Example Modal"
            >
            <div className="pr">
            <i onClick={this.closeModal} className='icon-close icon-close--position'></i>
            {page === 'buy' ?
            < img alt="template" className="img-responsive"
            src={`data:image/png;base64,${modalTemplateImage}`} /> :
            < img alt="static template" className="img-responsive"
            src={`${this.staticUrl}react/assets/images/resume${templateId || '1'}_preview.jpg`} />
        }
        </div>
        </Modal>
        </div>
        );
    }
}

TemplateModal.propTypes = {
    hideModal: propTypes.func,
    modal: propTypes.bool,
    modalTemplateImage: propTypes.string,
    page: propTypes.string,
    templateId: propTypes.number
}