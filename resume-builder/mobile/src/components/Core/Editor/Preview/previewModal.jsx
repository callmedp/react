import React,{Component} from 'react';
import Modal from 'react-modal';

export default class PreviewModal extends Component{
    constructor(props){
        super(props)
    }

    render(){
        return(
            <Modal isOpen={this.props.template.modal_status} contentLabel="Preview">
            <iframe srcdoc={this.props.template.html} style={{width:"90vh",height:"90vh"}}
            ></iframe>
                
            </Modal>
        )
    }
}