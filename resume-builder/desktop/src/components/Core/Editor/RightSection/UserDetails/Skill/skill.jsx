import React, {Component} from 'react';
import {reduxForm, FieldArray} from "redux-form"
import * as actions from "../../../../../../store/skill/actions";
import {connect} from "react-redux";
import validate from '../../../../../FormHandler/validations/skill/validate'
import {SkillRenderer} from "./skillRenderer";
import {scroller} from "react-scroll/modules";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"


/*
styles
* */
import 'react-accessible-accordion/dist/fancy-example.css';
import SavePreviewButtons from '../../../../../Common/SavePreviewButtons/savePreviewButtons';

class Skill extends Component {
    constructor(props) {
        super(props);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleAccordionClick = this.handleAccordionClick.bind(this);
        this.handleAddition = this.handleAddition.bind(this);
        this.deleteSkill = this.deleteSkill.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
        this.state = {
            active: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            submit: false
        };
        this.props.currentForm('skill');

    }

    componentDidMount() {
        this.props.fetchUserSkill();
    }


    componentWillUnmount() {
        this.updateInfoBeforeLoss()
    }

    async handleSubmit(values, entityLink) {
        const {list} = values;
        if (list.length) {
            await this.props.bulkUpdateOrCreate(list);
            this.setState({
                submit: true
            })
            if (entityLink) this.props.history.push(entityLink);
            else this.props.history.push('/resume-builder/buy/')
        }
    }

    async componentDidUpdate(prevProps){
        const {ui:{previewClicked},previewButtonClicked,history} = this.props;
        if(previewClicked !== prevProps.ui.previewClicked && previewClicked){
            await this.updateInfoBeforeLoss()
            this.setState({submit:true})
            previewButtonClicked(false)
            history.push('/resume-builder/preview/')
        }
    }

    async updateInfoBeforeLoss(){
        let {formData: {skill: {values, syncErrors}},bulkUpdateOrCreate} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el || {}).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit) await bulkUpdateOrCreate(values && values['list'])
    }

    handleAddition(fields) {
        const listLength = fields.length;
        fields.push({
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": {
                value: 5, 'label': '5'
            },
            order: listLength
        });

        scroller.scrollTo(`skill${fields.length - 1}`, {
            duration: 800,
            delay: 0,
            smooth: 'easeInOutQuad',
            offset: 0,
            containerId: 'skill'
        })
    }

    deleteSkill(index, fields, event) {
        event.stopPropagation();
        const skill = fields.get(index);
        fields.remove(index);
        if (skill && skill.id) {
            this.props.removeSkill(skill.id)
        }


    }


    handleAccordionClick(value) {
        this.setState({active: value})
    }


    render() {
        const {
            handleSubmit, history, showAlertModal,
            ui: {loader}, isEditable, editHeading, saveTitle, entityName, nextEntity,
            changeOrderingUp, changeOrderingDown, handleInputValue
        } = this.props;
        return (
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                <FieldArray
                    name="list"
                    handleSubmit={handleSubmit}
                    handleAccordionClick={this.handleAccordionClick}
                    handleAddition={this.handleAddition}
                    deleteSkill={this.deleteSkill}
                    changeOrderingUp={changeOrderingUp}
                    changeOrderingDown={changeOrderingDown}
                    loader={loader}
                    component={SkillRenderer}
                    saveTitle={(event) => saveTitle(event, 5)}
                    editHeading={(value) => editHeading(value)}
                    isEditable={isEditable}
                    entityName={entityName}
                    expanded={this.state.active}
                    handleInputValue={handleInputValue}


                />

                <SavePreviewButtons 
                        showAlertModal={showAlertModal} context={this} history={history}
                        nextEntity={nextEntity} updateInfoBeforeLoss={this.updateInfoBeforeLoss}
                    />


            </form>
        )
    }
}


export const SkillForm = reduxForm({
    form: 'skill',
    enableReinitialize: true,
    onSubmitFail: (errors) => scrollOnErrors(errors,'skill',-100),
    validate

})(Skill);


const mapStateToProps = (state) => {
    return {
        initialValues: state.skill,
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (userSkill) => {
            const {proficiency} = userSkill;
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
        "bulkUpdateOrCreate": (userSkills) => {
            userSkills = (userSkills || []).map((userSkill, index) => {
                const {proficiency} = userSkill;
                if (!userSkill['id']) delete userSkill['id'];
                return {
                    ...userSkill,
                    ...{
                        proficiency: proficiency && proficiency.value,
                        order: index
                    }
                };
            });
            return new Promise((resolve, reject) => {
                return dispatch(actions.bulkUpdateOrCreateUserSkill({list: userSkills, resolve, reject}));
            })
        },
        "fetchUserSkill": () => {
            return dispatch(actions.fetchUserSkill())
        },
        "removeSkill": (skillId) => {
            return dispatch(actions.deleteSkill(skillId))
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(SkillForm);
