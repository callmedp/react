import React,{Component} from 'react';
import Modal from 'react-modal';
import './NeedHelpModal.scss'


Modal.setAppElement(document.getElementById('react-app'));

export default class NeedHelpModal extends Component{

    constructor(props){
        super(props);
        this.feedbackSubmit = this.feedbackSubmit.bind(this)
        this.state = {
            'message':''
        }
    }

    feedbackSubmit(){
        const {feedback,personalInfo,hideHelpModal,eventClicked} = this.props;
        const {message} = this.state
        const values = {
            'name':personalInfo.first_name,
            'mobile':personalInfo.number,
            'email':personalInfo.email,
            'msg':message,
            'lsource':"8"
        }
        feedback(values)
        eventClicked({
            'action':'LeadSubmit',
            'label':'Header'
        })
        hideHelpModal()

    }

    handleChange(e){
        this.setState({message:e.target.value})
    }

    render(){
        const {modalStatus,hideHelpModal} = this.props
        return(
            <Modal 
                isOpen={modalStatus} 
                contentLabel="onRequestClose Preview"
                onRequestClose={hideHelpModal}
                className="alertModal"
                overlayClassName="Overlay">
                <div className="modal-reachus">
                    <h2>Reach out to us</h2>
                    <p>Let us know your feedback and suggestions, so we can help you build a powerful resume.</p>
                    <div className="form__group mt-20">
                        <textarea rows="6" className="form__input" onChange={(e) => {this.handleChange(e)}}></textarea>
                    </div>
                    <div class="text-center">
                        <button className="btn btn__round btn__primary mt-20" onClick={this.feedbackSubmit}>
                            Submit
                        </button>
                    </div>
                    <span className="close-wrap" onClick={()=>{hideHelpModal()}}>
                        <i className="sprite icon--close"></i>
                    </span>
                </div>
                

            </Modal>
        )
    }
}