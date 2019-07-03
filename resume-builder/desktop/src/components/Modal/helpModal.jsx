import React from 'react';
import Modal from 'react-modal';
import './helpModal.scss'
import  {getTitleCase} from "../../services/getTitleCase";

Modal.setAppElement(document.getElementById('react-app'));


export default class HelpModal extends React.Component {

    constructor(props){
        super(props)
        this.feedbackSubmit = this.feedbackSubmit.bind(this)
        this.state = {
            'message':''
        }
    }

    feedbackSubmit(){
        const {feedback,userInfo,hideHelpModal,eventClicked} = this.props;
        const {message} = this.state
        const values = {
            'name':userInfo.first_name,
            'mobile':userInfo.number,
            'email':userInfo.email,
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
    render() {
        const {modalStatus,hideHelpModal} = this.props
        return (
            <div className="pr">
                <Modal
                    isOpen={modalStatus} 
                    onRequestClose={hideHelpModal}
                    contentLabel="Help Modal"
                    className="help-modal1"
                >
                    <form>
                        <div className="pr help-modal">
                                <React.Fragment>
                                    <i onClick={()=>{hideHelpModal()}} className='icon-close icon-close--position1'></i>
                                    <h2>Reach out to us</h2>
                                    <p>Let us know your feedback and suggestions, so we can help you build a powerful resume. </p>
                                    <textarea rows="10" className="mb-20" placeholder="Message" onChange={(e) => {this.handleChange(e)}}></textarea>
                                    <button className="orange-button"
                                            type={'button'} onClick={this.feedbackSubmit}>Submit
                                    </button>
                                </React.Fragment>
                        </div>
                    </form>
                </Modal>
            </div>
        );
    }
}
