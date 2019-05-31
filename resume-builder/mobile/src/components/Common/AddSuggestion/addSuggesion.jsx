import React,{Component} from 'react';
import Modal from 'react-modal';
import './addSuggestion.scss';
import { renderAsyncCreatableSelect } from '../../FormHandler/formFieldRenderer';

Modal.setAppElement(document.getElementById('react-app'));

export default class AddSuggesion extends Component{
    constructor(props){
        super(props);
        this.state={
            suggestion_selected:{}
        }
        this.addSuggesion = this.addSuggesion.bind(this);
        this.removeSuggesion =this.removeSuggesion.bind(this)
    }

    addSuggesion(el,index,event){
        event.preventDefault()
        let {suggestion_selected} = this.state
        suggestion_selected[`${index}`] = el
        this.setState({suggestion_selected})

    }

    removeSuggesion(index,event){
        event.preventDefault()
        let {suggestion_selected} = this.state
        delete suggestion_selected[`${index}`]
        this.setState({suggestion_selected})
    }

    render(){
        const {label,modal_status,closeModal,suggestions} = this.props
        const {suggestion_selected} = this.state
        return(
            <Modal 
                isOpen={modal_status} 
                contentLabel="AddSuggested Summary"
                className="Modal"
                onRequestClose={closeModal}
                overlayClassName="Overlay">
                
                <div className="Modal--summary">
                    { suggestions.length ?
                        <React.Fragment>
                            <p className="add text-center">Add from suggested {label}</p>
                            <div className="Modal--summary--white-box">
                                {suggestions.map((el,index)=>{
                                        return(
                                            <div className="Modal--summary--add" key={index}>
                                                <p>{el}</p>
                                                <div className="btn btn__blue" onClick={(event)=>{suggestion_selected[index] 
                                                    ? this.removeSuggesion(index,event): this.addSuggesion(el,index,event) }}>
                                                    <input type="checkbox" readOnly checked={suggestion_selected[index] ? true : false} id={`add${index}`} />
                                                    <label htmlFor={`add${index}`}>ADD</label>
                                                </div>
                                            </div>
                                        )
                                    }
                                    )
                                }
                                <div className="text-center mb-15">
                                    <a className="btn btn__round btn__primary" onClick={()=>{closeModal(suggestion_selected); this.setState({suggestion_selected:{}})}}>Save & Continue</a>
                                </div>
                            </div>
                        </React.Fragment> :
                        <div className="Modal--summary--white-box">
                            <p className=" text-center no-suggestion">Sorry Suggestion not Available for this Job Title</p>
                            <div className="text-center mb-15">
                                <a className="btn btn__round btn__primary" onClick={()=>{closeModal(suggestion_selected); this.setState({suggestion_selected:{}})}}>Save & Continue</a>
                            </div>
                        </div>

                    }
                    
                </div>
            </Modal>
        )
    }
}