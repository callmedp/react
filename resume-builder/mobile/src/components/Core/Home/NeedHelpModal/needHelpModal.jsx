import React,{Component} from 'react';
import Modal from 'react-modal';


Modal.setAppElement(document.getElementById('react-app'));

export default class NeedHelpModal extends Component{

    constructor(props){
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
    }
    render(){
        const {modal_status} = this.props;
        return(
            <Modal 
                isOpen={true} 
                contentLabel="onRequestClose Preview"
                onRequestClose={this.handleCloseModal}
                className="alertModal"
                overlayClassName="Overlay">
                <div className="modal-image">
                    <img src={`${this.staticUrl}react/assets/images/mobile/resume-1.jpg`} alt=""/>
                </div>
                <span className="close-wrap" onClick={()=>{this.props.closeModalStatus()}}>
                    <i className="sprite icon--close"></i>
                </span>
            </Modal>
        )
    }
}