import React, {Component} from 'react';
import {reduxForm, FieldArray} from "redux-form"
import * as actions from "../../../../../../store/skill/actions";
import {connect} from "react-redux";
import validate from '../../../../../FormHandler/validations/skill/validate'
import {SkillRenderer} from "./skillRenderer";
import {scroller} from "react-scroll/modules";
import {scrollOnErrors} from "../../../../../../Utils/srollOnError"
import propTypes from 'prop-types';


/*
styles
* */
import '../../../../../../../node_modules/react-accessible-accordion/dist/fancy-example.css';
import SavePreviewButtons from '../../../../../Common/SavePreviewButtons/savePreviewButtons';

class Skill extends Component {
    static propTypes = {
        currentForm: propTypes.func,
        fetchUserSkill: propTypes.func,
        generateResumeAlert: propTypes.func,
        bulkUpdateOrCreate: propTypes.func,
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
        previewButtonClicked: propTypes.func,
        ui: propTypes.shape({
            alertModal: propTypes.bool,
            formName: propTypes.string,
            generateResumeModal: propTypes.bool,
            helpModal: propTypes.bool,
            loader: propTypes.bool,
            loginModal: propTypes.bool,
            modal: propTypes.bool,
            previewClicked: propTypes.bool,
            select_template_modal: propTypes.bool,
            showMoreSection: propTypes.bool,
            successLogin: propTypes.bool,
            suggestionModal: propTypes.bool,
            suggestionType: propTypes.string,
            suggestions: propTypes.array,
        }),
        initialValues: propTypes.shape({
            list: propTypes.array
        }),
        formData: propTypes.object,
        removeSkill: propTypes.func,
        handleSubmit: propTypes.func,
        saveTitle: propTypes.func,
        editHeading: propTypes.func,
        isEditable: propTypes.bool,
        entityName: propTypes.string,
        handleInputValue: propTypes.func,
        showAlertModal: propTypes.func,
        changeOrderingDown: propTypes.func,
        changeOrderingUp: propTypes.func,
        showAlertMessage: propTypes.func,
    }
    
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
        const {generateResumeAlert,bulkUpdateOrCreate,history} = this.props
        const {list} = values;
        if (list.length) {
            // skip the api call if there is a certain field which is required but empty (We skipped validation intentionally)
            let skipApiCall = false;
            
            list.map(el => {
                if(! el.name){
                    skipApiCall = true;
                }
                return; 
            })
            if(!skipApiCall){
                await bulkUpdateOrCreate(list);
            }
            
        }
        
        this.setState({
            submit: true
        })
        
        if (entityLink) history.push(entityLink);
        else{
            generateResumeAlert()
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
        let { initialValues, formData: {skill: {values, syncErrors}},bulkUpdateOrCreate} = this.props;
        let error = false;
        (syncErrors && syncErrors['list'] || []).map(el => Object.keys(el || {}).map(key => (!!el[key] ? error = true : false)))
        if (!error && !this.state.submit && JSON.stringify(initialValues)!==JSON.stringify(values)) await bulkUpdateOrCreate(values && values['list'])
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
        this.props.eventClicked({
            'action':'AddNew',
            'label':'Skills'
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
            handleSubmit,userInfo:{order_data}, history, showAlertModal,eventClicked,
            ui: {loader}, isEditable, editHeading, saveTitle, entityName, nextEntity,
            changeOrderingUp, changeOrderingDown, handleInputValue,showAlertMessage
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
            editHeading={() => editHeading(5)}
            isEditable={isEditable}
            entityName={entityName}
            expanded={this.state.active}
            handleInputValue={handleInputValue}
            showAlertMessage={showAlertMessage}
            />
            
            <SavePreviewButtons 
            showAlertModal={showAlertModal} context={this} history={history} order_data={order_data} form_name={'Skills'}
            nextEntity={nextEntity} updateInfoBeforeLoss={this.updateInfoBeforeLoss} eventClicked={eventClicked}
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
    