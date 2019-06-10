import React from 'react';
import Modal from 'react-modal';
import './suggestionModal.scss'

Modal.setAppElement(document.getElementById('react-app'));

export default class SuggestionModal extends React.Component {
    constructor(props) {
        super(props);
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
        this.addSuggesion = this.addSuggesion.bind(this);
        this.removeSuggesion =this.removeSuggesion.bind(this)
        this.state = {
            suggestion_selected: {}
        }
        this.handleSuggestion = this.handleSuggestion.bind(this)
    }

    addSuggesion(el,index,event){
        // event.preventDefault()
        let {suggestion_selected} = this.state
        suggestion_selected[`${index}`] = el
        this.setState({suggestion_selected})

    }

    removeSuggesion(index,event){
        // event.preventDefault()
        let {suggestion_selected} = this.state
        delete suggestion_selected[`${index}`]
        this.setState({suggestion_selected})
    }

    handleSuggestion(suggestion_selected){
        this.props.closeModal(suggestion_selected); 
        this.setState({suggestion_selected:{}})
    }

    render() {
        const {label,modal_status,closeModal,suggestions} = this.props
        const {suggestion_selected} = this.state

        return (
            <div className="pr">
                <Modal
                    style={{
                        content: {
                            left: '10%',
                            right: '10%',
                            top: '5%',
                            overflow: 'hidden'
                        }
                    }}
                    isOpen={modal_status} 
                    onRequestClose={closeModal}
                    contentLabel="Suggestion Modal"
                >
                    <div className="pr suggested-summary">
                        {suggestions.length ? 
                            <React.Fragment>
                                <i onClick={()=>{this.handleSuggestion({})}} className='icon-close icon-close--position'></i>
                                <h2>Add from suggested {label}</h2>
                                <ul>
                                    {(suggestions || []).map((el, index) => {
                                        return (
                                        <li key={index}>
                                        <span className={suggestion_selected[index]  ? 'selected' : ''}  
                                        onClick={(event)=>{suggestion_selected[index] 
                                            ? this.removeSuggesion(index,event): this.addSuggesion(el,index,event) }} htmlFor={`add${index}`} >
                                            <input class="styled-checkbox" type="checkbox" readOnly checked={suggestion_selected[index] ? true : false} id={`add${index}`} /> <label for="styled-checkbox-1">Add</label>
                                        </span>
                                            <p>{el}</p>
                                        </li>)
                                    })}
                                </ul>
                                <button className="orange-button"
                                        type={'submit'} onClick={()=>{this.handleSuggestion(suggestion_selected)}}>Save and Continue
                                </button>
                            </React.Fragment>:
                            <React.Fragment>
                                    
                                <h2>Sorry Suggestions not available for this Job Title</h2>
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