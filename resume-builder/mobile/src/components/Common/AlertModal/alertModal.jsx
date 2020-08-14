import React,{Component} from 'react';
import Modal from 'react-modal';
import './alert.scss'
import propTypes from 'prop-types';

if(typeof document !== 'undefined') {
    Modal.setAppElement(document.getElementById('react-app'));
}

export default class AlertModal extends Component{
    
    constructor(props){
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/';
        this.goToNewLink = this.goToNewLink.bind(this);
    }
    
    goToNewLink(){
        const {history,link,closeModal} = this.props;
        history.push(`/resume-builder/edit/?type=${link}`)
        closeModal()
        
    }
    render(){
        const {modal_status,closeModal,newUser,generateResumeModal} = this.props;
        return(
            <Modal 
            isOpen={modal_status} 
            contentLabel="onRequestClose Preview"
            onRequestClose={this.handleCloseModal}
            className="alertModal"
            overlayClassName="Overlay">
            {newUser ?
                <div className="alertModal__wrap">
                <i className="alertModal__wrap--alert m-auto"></i>
                <div className="alertModal__wrap--title text-center mb-15">Please save your profile info to continue</div>
                {/* <div className="alertModal__wrap--content text-center mb-15">
                <p>Some information may be lost as required fields are not filled.</p>
            </div> */}
            <div className="alertModal__wrap__btn-wrap">
            {/* <span className="btn btn-sm btn__primary btn__round w-150" onClick={this.goToNewLink}>Yes, change it!</span> */}
            <span className="btn btn-sm btn--outline btn__round w-150" onClick={closeModal}>Ok</span>
            </div>
            </div>:
            generateResumeModal ?
            <div className="alertModal__wrap">
            <div className="alertModal__wrap--title text-center mb-15">Generating Resume</div>
            <div className="alertModal__wrap--content text-center mb-15">
            <p>Your resume is being generated. Please wait..</p>
            </div>
            <div className="logo-center">
            <img src={`${this.staticUrl}react/assets/images/mobile/blue-loader.png`}/>
            </div> 
            </div>:
            <div className="alertModal__wrap">
            <i className="alertModal__wrap--alert m-auto"></i>
            <div className="alertModal__wrap--title text-center mb-15">Are you sure?</div>
            <div className="alertModal__wrap--content text-center mb-15">
            <p>Some information may be lost as required fields are not filled.</p>
            </div>
            <div className="alertModal__wrap__btn-wrap">
            <span className="btn btn-sm btn__primary btn__round w-150" onClick={this.goToNewLink}>Yes, change it!</span>
            <span className="btn btn-sm btn--outline btn__round w-150" onClick={closeModal}>Cancel</span>
            </div>
            </div>
        }
        </Modal>
        )
    }
}

AlertModal.propTypes = {
    generateResumeModal: propTypes.bool,
    modal_status: propTypes.bool,
    closeModal: propTypes.func,
    link: propTypes.string,
    newUser: propTypes.func,
    history: propTypes.shape({
        action: propTypes.string,
        block: propTypes.func,
        createHref: propTypes.func,
        go: propTypes.func,
        goBack: propTypes.func,
        goForward: propTypes.func,
        length: propTypes.number,
        listen: propTypes.func,
        location: propTypes.shape({
            hash: propTypes.string,
            pathname: propTypes.string,
            search: propTypes.string,
            state: undefined
        }),
        push: propTypes.func,
        replace: propTypes.func, 
    }),
}