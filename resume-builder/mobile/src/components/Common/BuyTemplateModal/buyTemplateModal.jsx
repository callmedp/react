import React,{Component} from 'react';
import Modal from 'react-modal';
import './buyTemplateModal.scss'


Modal.setAppElement(document.getElementById('react-app'));

export default class BuyTemplateModal extends Component{

    constructor(props){
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';

    }
    render(){
        const {modal_status,templateImage} = this.props;
        return(
            <Modal 
                isOpen={modal_status} 
                contentLabel="onRequestClose Preview"
                onRequestClose={this.handleCloseModal}
                className="Modal"
                overlayClassName="Overlay">
                <div className="modal-image">
                    <img className="modal-image-customize" src={`data:image/png;base64, ${templateImage}`} alt="Custom resume" />
                    {/* <img src={`${this.staticUrl}react/assets/images/mobile/resume-1.jpg`} alt=""/> */}
                </div>
                <span className="close-wrap" onClick={()=>{this.props.closeModalStatus()}}>
                    <i className="sprite icon--close"></i>
                </span>
            </Modal>
        )
    }
}