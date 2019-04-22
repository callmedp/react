import React,{Component} from 'react';
import Modal from 'react-modal';

export default class PreviewModal extends Component{
    constructor(props){
        super(props)
    }

    render(){
        return(
            <Modal isOpen={this.props.template.modal_status} contentLabel="Preview">
                <div dangerouslySetInnerHTML={{__html: this.props.template.html}}></div>
            </Modal>
        )
    }
}