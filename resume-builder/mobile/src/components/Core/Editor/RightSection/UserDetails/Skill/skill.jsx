import React, {Component} from 'react';
import {Field, reduxForm, FieldArray} from "redux-form"
import * as actions from "../../../../../../store/skill/actions";
import {connect} from "react-redux";
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";
import {required} from "../../../../../FormHandler/formValidations"

class Skill extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
        this.deleteSkill = this.deleteSkill.bind(this)
        this.handleAddition = this.handleAddition.bind(this)
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
        const listLength = fields.length;
        fields.push({
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": '',
            "order": listLength
        })

    }


    async handleSubmit(values) {
        this.props.bulkSaveUserSkill(values.list);
        this.props.history.push('/resume-builder/edit/?type=language')
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
                                        <li className="subHeading__btn">
                                            <i className="sprite icon--upArrow"></i>
                                        </li>
                                        <li className="subHeading__btn">
                                            <i className="sprite icon--downArrow"></i>
                                        </li>
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
             
                </React.Fragment>         
            )
        }
        return (
            <div className="buildResume">
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <FieldArray name="list" component={renderSkills}/>
                    <ul className="form">
                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline">Preview</button>
                                <button className="btn btn__round btn__primary" type={'submit'}>Save &amp; Continue</button>
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
            console.log(listItems)
            return dispatch(actions.bulkSaveUserSkill({list: listItems}))
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SkillForm);
