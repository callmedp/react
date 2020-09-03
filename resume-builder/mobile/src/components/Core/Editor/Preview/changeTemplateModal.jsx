import React,{Component} from 'react';
import Modal from 'react-modal';
import './preview.scss'
import ResumeSlider from '../../Home/ResumeSlider/resumeSlider';
import propTypes from 'prop-types';

if(typeof document !== 'undefined') {
    Modal.setAppElement(document.getElementById('react-app'));
}

export default class ChangeTemplateModal extends Component{

    render(){
        return(
            <Modal 
                isOpen={this.props.template.modal_status} 
                contentLabel="onRequestClose Preview"
                onRequestClose={this.handleCloseModal}
                className="Modal overflow-visible"
                overlayClassName="Overlay">
                <div className="">
                    <ResumeSlider 
                        sendTrackingInfo={this.props.sendTrackingInfo}
                        showtext={false} {...this.props}/>
                </div>
                <span className="close-wrap preview-close" onClick={()=>{this.props.updateModalStatus({modal_status:false})}}>
                    <i className="sprite icon--close"></i>
                </span>
            </Modal>
        )
    }
}

ChangeTemplateModal.propTypes = {
    template: propTypes.shape({
        color: propTypes.number,
        entity_position: propTypes.array,
        heading_font_size: propTypes.number,
        html: propTypes.string,
        modal_status: propTypes.bool,
        reorderFailToast: propTypes.bool,
        templateImage: propTypes.string,
        text_font_size: propTypes.number,
        thumbnailImages: propTypes.array,
        zoomInHtml: propTypes.string,
    }),
    updateModalStatus: propTypes.func
}