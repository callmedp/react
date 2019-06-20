import React from 'react';
import Modal from 'react-modal';
import './suggestionModal.scss'

Modal.setAppElement(document.getElementById('react-app'));

export default class SuggestionModal extends React.Component {
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
        const {label,modal_status,closeModal,suggestions,maxLength} = this.props
        const {suggestion_selected,error} = this.state

        return (
            <div className="pr">
                <Modal
                    isOpen={modal_status} 
                    onRequestClose={closeModal}
                    contentLabel="Suggestion Modal"
                    className="suggestion-modal"
                >
                    <div className="pr suggested-summary">
                        {suggestions.length ? 
                            <React.Fragment>
                                <i onClick={()=>{this.handleSuggestion({})}} className='icon-close icon-close--position'></i>
                                <h2>Add from suggested {label}</h2>
                                <ul>
                                    {(suggestions || []).map((el, index) => {
                                        return (
                                        <li key={index} onClick={(event)=>{suggestion_selected[index] 
                                            ? this.removeSuggestion(index,event): this.addSuggestion(el,index,event) }} htmlFor={`add${index}`}>
                                        <span className={suggestion_selected[index]  ? 'selected' : ''}  
                                         >
                                            <input className="styled-checkbox" type="checkbox" readOnly checked={suggestion_selected[index] ? true : false} id={`add${index}`} /> <label htmlFor="styled-checkbox-1">Add</label>
                                        </span>
                                            <p>{el}</p>
                                        </li>)
                                    })}
                                </ul>
                                {error ?<p className="suggestion-error">Sorry this Suggestion cannot be added.It exceeds the maximum {maxLength} characters length of summary</p>:''}
                                <button className="orange-button"
                                        type={'submit'} onClick={()=>{this.handleSuggestion(suggestion_selected)}}>Save and Continue
                                </button>
                            </React.Fragment>:
                            <React.Fragment>
                                    
                                <h2>Sorry suggestions not available for this job title</h2>
                                <button className="orange-button"
                                    type={'submit'} onClick={()=>{this.handleSuggestion({})}}>Close
                            </button>
                            </React.Fragment>
                        }
                    </div>
                </Modal>
            </div>
        );
    }
}