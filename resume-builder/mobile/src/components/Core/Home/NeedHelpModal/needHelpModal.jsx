import React,{Component} from 'react';
import Modal from 'react-modal';


Modal.setAppElement(document.getElementById('react-app'));

export default class NeedHelpModal extends Component{

    render(){
        const {modal_status} = this.props;
        return(
            <Modal 
                isOpen={false} 
                contentLabel="onRequestClose Preview"
                onRequestClose={this.handleCloseModal}
                className="alertModal"
                overlayClassName="Overlay">
                dfjfhsdjhjshj
            </Modal>
        )
    }
}