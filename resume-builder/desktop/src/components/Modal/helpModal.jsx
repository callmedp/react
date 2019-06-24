import React from 'react';
import Modal from 'react-modal';
import './helpModal.scss'

Modal.setAppElement(document.getElementById('react-app'));

export default class HelpModal extends React.Component {
    constructor(props) {
        super(props);
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
        this.addSuggestion = this.addSuggestion.bind(this);
        this.removeSuggestion =this.removeSuggestion.bind(this)
        this.state = {
            suggestion_selected: {},
            error:false,
            length:0
        }
        this.handleSuggestion = this.handleSuggestion.bind(this)
    }
    componentDidMount(){
        const {length} = this.props
        this.setState({length})
    }
    componentDidUpdate(prevProps){
        const {length} = this.props
        if(length!==prevProps.length){
            this.setState({length})
        }
    }

    addSuggestion(el,index,event){
        // event.preventDefault()
        let {suggestion_selected} = this.state
        const {maxLength} = this.props
        const {length} = this.state
        if(length + el.length >maxLength){
            this.setState({error:true})
            return
        }
        suggestion_selected[`${index}`] = el
        this.setState({suggestion_selected,error:false,length:length+el.length})

    }

    removeSuggestion(index,event){
        // event.preventDefault()
        let {suggestion_selected,length} = this.state
        this.setState({error:false,length:length-suggestion_selected[`${index}`].length})
        delete suggestion_selected[`${index}`]
        this.setState({suggestion_selected})
        
        
    }

    handleSuggestion(suggestion_selected){
        this.props.closeModal(suggestion_selected); 
        this.setState({suggestion_selected:{},error:false})
    }

    render() {
        const {label,modalStatus,closeModal,suggestions,maxLength,hideHelpModal} = this.props
        const {suggestion_selected,error} = this.state
        return (
            <div className="pr">
                <Modal
                    isOpen={modalStatus} 
                    onRequestClose={closeModal}
                    contentLabel="Help Modal"
                    className="help-modal1"
                >
                    <form>
                        <div className="pr help-modal">
                                <React.Fragment>
                                    <i onClick={()=>{hideHelpModal()}} className='icon-close icon-close--position1'></i>
                                    <h2>Reach out to us</h2>
                                    <p>Let us know your feedback and suggestions, so we can help you build a powerful resume. </p>
                                    <textarea rows="10" className="mb-20" placeholder="Message"></textarea>
                                    <button className="orange-button"
                                            type={'submit'} onClick={()=>{this.handleSuggestion(suggestion_selected)}}>Submit
                                    </button>
                                </React.Fragment>
                        </div>
                    </form>
                </Modal>
            </div>
        );
    }
}