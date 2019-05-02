import React, {Component} from 'react';
import {Field, reduxForm, FieldArray} from "redux-form";
import * as actions from "../../../../../../store/reference/actions";
import {connect} from "react-redux";
import renderReferences from "./renderReference"
import validate from "../../../../../FormHandler/validtaions/reference/validate"
import PreviewModal from "../../../Preview/previewModal";
import { animateScroll as scroll, scrollSpy, scroller } from 'react-scroll'

class References extends Component {
    constructor(props) {
        super(props)
        this.handleSubmit = this.handleSubmit.bind(this)
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteReference = this.deleteReference.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);
        this.state = {
            'editHeading': false,
            'heading' : ''
        }
        this.updateInputValue =this.updateInputValue.bind(this);
        this.editHeadingClick = this.editHeadingClick.bind(this);
    }

    async handleSubmit(values) {
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        await this.props.bulkUpdateUserReference(values.list);
        if(currentLinkPos === listOfLinks.length){
            currentLinkPos = 0
            this.props.history.push(`/resume-builder/buy`)  
        }
        else{
            this.props.updateCurrentLinkPos({currentLinkPos})
            this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)    
        }
        
    }

    componentDidMount() {
        this.props.fetchUserReference()
        console.log("Here")
        console.log("----",this.props.sidenav.currentLinkPos)
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[9].entity_text})
        }
    }

    updateInputValue(key,e) {
        if(e.keyCode === 13){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,9,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        if(key === 'blur'){
            if(e.target.value.length){
                this.props.headingChange(this.props.personalInfo,9,e.target.value)
                this.setState({editHeading:false,heading:e.target.value})
            }
            else{
                this.setState({editHeading:false})
            }
        }
        
    }

    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({heading : this.props.personalInfo.entity_preference_data[9].entity_text})
        }
    }

    editHeadingClick(){
        this.setState({editHeading:true})
    }

    handleAddition(fields, error) {
        
        fields.push({
            "candidate_id": '',
            "id": '',
            "reference_name": '',
            "reference_designation": '',
            "about_user": "",
            order: fields.length
        })
        scroller.scrollTo(`references${fields.length -1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 150
        })
    }

    deleteReference(index, fields, event) {
        event.stopPropagation();
        const reference = fields.get(index);
        fields.remove(index);
        if (reference && reference.id) {
            this.props.removeReference(reference.id)
        }


    }

    async changeOrderingUp(index,fields,event){
        event.stopPropagation();
        ////console.log("Clicked Up")
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index - 1)
        fields.insert(index - 1, prevItem)
        fields.swap(index, index - 1)
        await this.props.bulkUpdateUserReference(fields.getAll());
    }

    async changeOrderingDown(index,fields,event){
        event.stopPropagation();
        ////console.log("Clicked Down")
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index+1)
        fields.insert(index + 1, nextItem)
        fields.swap(index, index + 1);
        await this.props.bulkUpdateUserReference(fields.getAll());
    }

    render () {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const { handleSubmit,reference,submitting,submitSucceeded} = this.props;
        const {editHeading,heading} =this.state;
        return(
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <PreviewModal {...this.props}/>
                    <FieldArray name={"list"} 
                                handleSubmit={handleSubmit}
                                handleAddition={this.handleAddition}
                                deleteReference={this.deleteReference}
                                changeOrderingUp={this.changeOrderingUp}
                                changeOrderingDown={this.changeOrderingDown}
                                component={renderReferences}
                                updateInputValue={this.updateInputValue}
                                editHeading={editHeading}
                                editHeadingClick={this.editHeadingClick}
                                loader={this.props.loader.dataloader}
                                heading ={heading}/>
                    <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline" 
                                    onClick={()=>{this.props.updateModalStatus({modal_status:true})}} 
                                    type={'button'}>Preview</button>
                                <button className="btn btn__round btn__primary" disabled={submitting} type={'submit'}>
                                    {(length === pos +1) ?"Buy" :"Save & Continue"}
                                </button>
                            </div>
                        </li>
                    </ul>
                </form>
            </div>
        )
    }
}


export const ReferenceForm = reduxForm({
    form: 'reference',
    enableReinitialize: true,
    validate
})(References);


const mapStateToProps = (state) => {
    return {
        initialValues: state.reference,
        reference: state.reference
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userReference) => {
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserReference({userReference, resolve, reject}));
            })
        },
        "fetchUserReference": () => {
            return dispatch(actions.fetchUserReference())
        },
        "removeReference": (referenceId) => {
            return dispatch(actions.deleteReference(referenceId))
        },

        "bulkUpdateUserReference": (listItems) => {
            listItems = (listItems || []).map(userReference => {
                if (!userReference['id']) delete userReference['id'];
                return userReference;
            })
            return dispatch(actions.bulkUpdateUserReference({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ReferenceForm);
