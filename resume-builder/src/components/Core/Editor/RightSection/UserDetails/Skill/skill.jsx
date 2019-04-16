import React, {Component} from 'react';
import {Field, reduxForm} from "redux-form"
import * as actions from "../../../../../../store/skill/actions";
import {connect} from "react-redux";
import {renderField, renderSelect} from "../../../../../FormHandler/formFieldRenderer.jsx";
import moment from "moment";
import {required} from "../../../../../FormHandler/formValidations"

class Skill extends Component {

    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this)
    }

    componentDidMount() {
        this.props.fetchUserSkill();
    }

    async handleSubmit(values) {
        //console.log(values)
        await this.props.onSubmit(values);
        this.props.history.push('/resume-builder/edit/?type=language')
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize, skill} = this.props;
        return (
            <div className="buildResume">
                <div className="buildResume__wrap pb-0">
                    <div className="buildResume__heading heading">
                        <div className="heading__info">
                            <h1>Skills</h1>
                            <i className="sprite icon--edit"></i>
                        </div>
                        <button role="button" className="btn btn__round btn--outline">+ Add new</button>
                    </div>
                    <form onSubmit={handleSubmit(this.handleSubmit)}>
                        <div className="subHeading pb-0">
                            <h2>{skill.name}</h2>
                            <ul className="subHeading__control">
                                <li className="subHeading__delete">
                                    <span className="sprite icon--delete" role="button"></span>
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
                                <label className="form__label" for="name">Skill name</label>
                                <div className="input-group">
                                    <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--skills-grey"></i>
                                    </span>
                                    </div>
                                    <Field component={renderField} validate={required} type={"text"} name="name"
                                        className="form__input" aria-label="name" id="name"/>
                                </div>
                            </li>
                            
                            <li className="form__group">
                                <label className="form__label" for="proficiency">Skill rating (out of 10)</label>
                                <Field name="proficiency" id="proficiency"
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
                                           validate={required}/>
                            </li>
                        </ul>

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
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SkillForm);
