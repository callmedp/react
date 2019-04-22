import React, {Component} from 'react';
import {Field, reduxForm, FieldArray} from "redux-form"
import * as actions from "../../../../../../store/skill/actions";
import {connect} from "react-redux";
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";
import validate from "../../../../../FormHandler/validtaions/skill/validate"
import PreviewModal from "../../../Preview/previewModal";

class Skill extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteSkill = this.deleteSkill.bind(this)
        this.handleAddition = this.handleAddition.bind(this)
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);
    }

    componentDidMount() {
        this.props.fetchUserSkill();
    }

    deleteSkill(index, fields, event) {
        event.stopPropagation();
        console.log(index)
        console.log(fields.get(index))
        const skill = fields.get(index);
        fields.remove(index);
        if (skill && skill.id) {
            this.props.removeSkill(skill.id)
        }


    }

    handleAddition(fields, error) {
        
        fields.push({
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": '',
            "order": fields.length
        })

    }

    async handleSubmit(values) {
        const {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        if(currentLinkPos > listOfLinks.length){
            currentLinkPos = 0
        }
        await this.props.bulkUpdateUserSkill(values.list);
        this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
    }

    changeOrderingUp(index,fields,event){
        event.stopPropagation();
        console.log("Clicked Up")
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index - 1)
        fields.insert(index - 1, prevItem)
        fields.swap(index, index - 1)
    }

    changeOrderingDown(index,fields,event){
        event.stopPropagation();
        console.log("Clicked Down")
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index+1)
        fields.insert(index + 1, nextItem)
        fields.swap(index, index + 1);
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize, skill} = this.props;
        const renderSkills = ({fields, meta: {touched, error, submitFailed}}) => {
            return (
                <React.Fragment>
                    <div className="buildResume__wrap pb-0">
                        <div className="buildResume__heading heading">
                            <div className="heading__info">
                                <h1>Skills</h1>
                                <i className="sprite icon--edit"></i>
                            </div>
                            <button type={'button'} onClick={this.handleAddition.bind(this, fields, error)} 
                                className="btn btn__round btn--outline">+ Add new</button>
                        </div>
                    </div>
                    {fields.map((member, index) => {
                        return(
                            <React.Fragment key={index}>
                                <div className="subHeading pb-0">
                                    <h2>{fields.get(index).name || 'Skill'}</h2>
                                    <ul className="subHeading__control">
                                        <li className="subHeading__delete">
                                            <span onClick={(event) => this.deleteSkill(index, fields, event)}
                                             className="sprite icon--delete" role="button"></span>
                                        </li>
                                        {index == 0 ? '':
                                            <li className="subHeading__btn"
                                                onClick={(event) => this.changeOrderingUp(index, fields, event)}>
                                                <i className="sprite icon--upArrow"></i>
                                            </li>
                                        }
                                        {index == fields.length-1 ? '':
                                            <li className="subHeading__btn"
                                                onClick={(event) => this.changeOrderingDown(index, fields, event)}>
                                                <i className="sprite icon--downArrow"></i>
                                            </li>
                                        }
                                    </ul>
                                </div>
        
                                <ul className="form pb-0">
                                    <li className="form__group">
                                        <label className="form__label" htmlFor="name">Skill name</label>
                                        <div className="input-group">
                                            <div className="input-group__prepend">
                                            <span className="input-group__text">
                                                <i className="sprite icon--skills-grey"></i>
                                            </span>
                                            </div>
                                            <Field component={renderField}  type={"text"} name={`${member}.name`}
                                                className="form__input"/>
                                        </div>
                                    </li>
                                    
                                    <li className="form__group">
                                        <label className="form__label" htmlFor="proficiency">Skill rating (out of 10)</label>
                                        <Field name={`${member}.proficiency`}
                                                component={renderSelect}
                                                className="form__select"
                                                isMulti={false}
                                                options={[
                                                    {value: 1, label: '1'},
                                                    {value: 2, label: '2'},
                                                    {value: 3, label: '3'},
                                                    {value: 4, label: '4'},
                                                    {value: 5, label: '5'},
                                                    {value: 6, label: '6'},
                                                    {value: 7, label: '7'},
                                                    {value: 8, label: '8'},
                                                    {value: 9, label: '9'},
                                                    {value: 10, label: '10'}
                                                ]}
                                                />
                                    </li>
                                </ul>
                            </React.Fragment>
                    )})}
                    {error && <li>{error}</li>}
             
                </React.Fragment>         
            )
        }
        return (
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <PreviewModal {...this.props}/>
                    <FieldArray name="list" component={renderSkills}/>
                    <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline" 
                                    onClick={()=>{this.props.updateModalStatus({modal_status:true})}} 
                                    type={'button'}>Preview</button>
                                <button className="btn btn__round btn__primary" disabled={!submitting} type={'submit'}>Save &amp; Continue</button>
                            </div>
                        </li>
                    </ul>
                </form>
            </div>
            
        )
    }
}

export const SkillForm = reduxForm({
    form: 'Skill',
    validate,
    enableReinitialize: true
})(Skill);


const mapStateToProps = (state) => {
    return {
        initialValues: state.skill,
        skill: state.skill
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userSkill) => {
            const {proficiency} = userSkill
            userSkill = {
                ...userSkill,
                ...{
                    proficiency: proficiency && proficiency.value
                }
            };
            return new Promise((resolve, reject) => {
                return dispatch(actions.updateUserSkill({userSkill, resolve, reject}));
            })
        },
        "fetchUserSkill": () => {
            return dispatch(actions.fetchUserSkill())
        },
        "removeSkill": (skillId) => {
            return dispatch(actions.deleteSkill(skillId))
        },
        "bulkSaveUserSkill": (listItems) => {
            listItems = (listItems || []).map(userSkill => {
                const {proficiency} = userSkill;
                if (!userSkill['id']) delete userSkill['id'];
                userSkill = {
                    ...userSkill,
                    ...{
                        proficiency: proficiency && proficiency.value
                    }
                };
                return userSkill;
            })
            return dispatch(actions.bulkSaveUserSkill({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SkillForm);
