import React, { Component } from 'react';
import { connect } from "react-redux";
import './rightSection.scss';
import PersonalInfo from './UserDetails/PersonalInfo/personalInfo.jsx';
import Education from './UserDetails/Education/education.jsx';
import Experience from './UserDetails/Experience/experience.jsx';
import Language from './UserDetails/Language/language.jsx';
import Skill from './UserDetails/Skill/skill.jsx';
import Summary from './UserDetails/Summary/summary.jsx';
import Award from './UserDetails/Award/award.jsx';
import Project from './UserDetails/Project/project.jsx';
import Reference from './UserDetails/Reference/reference.jsx';
import Course from './UserDetails/Course/course.jsx';
import Template from './Template/template.jsx';
import queryString from 'query-string';
import * as actions from '../../../../store/personalInfo/actions';
import { currentForm, hideMoreSection, previewButtonClicked } from '../../../../store/ui/actions';
import { formCategoryList } from "../../../../Utils/formCategoryList";
import Swal from 'sweetalert2';
import { withRouter } from "react-router-dom";
import propTypes from 'prop-types';

class RightSection extends Component {
    constructor(props) {
        super(props);
        const values = queryString.parse(this.props.location.search)
        this.renderSwitch = this.renderSwitch.bind(this);
        this.saveTitle = this.saveTitle.bind(this);
        this.editHeading = this.editHeading.bind(this);
        this.handlePreview = this.handlePreview.bind(this);
        this.changeOrderingUp = this.changeOrderingUp.bind(this);
        this.changeOrderingDown = this.changeOrderingDown.bind(this);
        this.handleInputValue = this.handleInputValue.bind(this);
        this.showAlertMessage = this.showAlertMessage.bind(this);

        this.state = {
            type: (values && values.type) || '',
            'isEditable': false,
            'currentFields': [],
            'titleValue': ''
        }
    }


    componentDidUpdate(prevProps) {
        if (this.props.location !== prevProps.location) {
            const values = queryString.parse(this.props.location.search);
            this.setState({
                type: (values && values.type) || '',
                'isEditable': false
            })
        }
    }


    async handlePreview() {
        this.props.history.push('/resume-builder/preview/');
    }


    editHeading(entityId) {
        this.setState({
            'isEditable': true
        });
        this.props.eventClicked({
            'action': 'EditSection',
            'label': formCategoryList[entityId].name
        })
    }

    saveTitle(event, entityId) {
        event.stopPropagation();
        this.setState({
            'isEditable': false
        });
        const { titleValue } = this.state;
        let { entityList } = this.props;
        if (entityList && entityList.length) {
            let index = entityList.findIndex(el => el.entity_id === entityId);
            entityList[index]['entity_text'] = titleValue || '';
            this.props.updateEntityPreference(entityList)
        }
    }

    handleInputValue(value) {
        this.setState({
            titleValue: value
        })
    }

    changeOrderingUp(index, fields, event) {
        event.stopPropagation();
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index - 1)
        fields.insert(index - 1, prevItem)
        fields.swap(index, index - 1)
        this.setState({
            currentFields: fields
        })
        // this.props.handleSwap([currentItem, prevItem])
    }

    changeOrderingDown(index, fields, event) {
        event.stopPropagation();
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.remove(index);
        fields.insert(index, currentItem)
        fields.remove(index + 1)
        fields.insert(index + 1, nextItem)
        fields.swap(index, index + 1);
        this.setState({
            currentFields: fields
        })

        // this.props.handleSwap([currentItem, nextItem])
    }

    showAlertMessage() {
        Swal.fire(
            'You Can\'t add more!',
            'Please Fill current list first',
            'error'
        )
    }

    // handleResumeGeneration(orderId){
    //     showGenerateResumeModal()
    //         reGeneratePDF(order_data.id)
    //         setTimeout(function() {
    //             window.location.href = `${siteDomain}/dashboard`
    //             hideGenerateResumeModal()
    //         }, 5000);
    // }
    renderSwitch() {
        const { entityList, ui: { showMoreSection }, hideMoreSection } = this.props;
        let entity, nextEntity;
        const { isEditable } = this.state;

        switch (this.state.type) {
            case 'profile': {
                entity = entityList && entityList[0];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = (nextEntity && formCategoryList[nextEntity['entity_id']]) || undefined;
                return !!((showMoreSection)) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button" onClick={hideMoreSection}>Back to Edit</button>
                    </div>
                    : <PersonalInfo {...this.props}
                        isEditable={isEditable}
                        saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                        handlePreview={this.handlePreview}
                        entityName={(entity && entity['entity_text']) || 'Personal Info'}
                        nextEntity={(nextEntity && nextEntity['link']) || nextEntity}
                        editHeading={(elem) => this.editHeading(elem)}
                        handleInputValue={(value) => this.handleInputValue(value)}

                    />
            }

            case 'education': {
                entity = entityList && entityList[1];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = (nextEntity && formCategoryList[nextEntity['entity_id']]) || undefined;

                return !!((showMoreSection)) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button" onClick={hideMoreSection}>Back to Edit</button>
                    </div>
                    : <Education {...this.props}
                        isEditable={isEditable}
                        handlePreview={this.handlePreview}
                        editHeading={(elem) => this.editHeading(elem)}
                        entityName={(entity && entity['entity_text']) || 'Education'}
                        nextEntity={(nextEntity && nextEntity['link']) || nextEntity}
                        changeOrderingUp={this.changeOrderingUp}
                        changeOrderingDown={this.changeOrderingDown}
                        saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                        currentFields={this.state.currentFields}
                        handleInputValue={this.handleInputValue}
                        showAlertMessage={this.showAlertMessage}

                    />
            }

            case 'experience': {
                entity = entityList && entityList[2];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = (nextEntity && formCategoryList[nextEntity['entity_id']]) || undefined;
                return !!(showMoreSection) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button" onClick={hideMoreSection}>Back to Edit</button>
                    </div>
                    : <Experience {...this.props}
                        isEditable={isEditable}
                        handlePreview={this.handlePreview}
                        nextEntity={(nextEntity && nextEntity['link']) || nextEntity}
                        entityName={(entity && entity['entity_text']) || 'Experience'}
                        saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                        changeOrderingUp={this.changeOrderingUp}
                        changeOrderingDown={this.changeOrderingDown}
                        editHeading={(elem) => this.editHeading(elem)}
                        currentFields={this.state.currentFields}
                        handleInputValue={this.handleInputValue}
                        showAlertMessage={this.showAlertMessage}


                    />
            }

            case 'project': {
                entity = entityList && entityList[3];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = (nextEntity && formCategoryList[nextEntity['entity_id']]) || undefined;
                return !!(showMoreSection) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button" onClick={hideMoreSection}>Back to Edit</button>
                    </div>
                    : <Project {...this.props}
                        isEditable={isEditable}
                        handlePreview={this.handlePreview}
                        nextEntity={(nextEntity && nextEntity['link']) || nextEntity}
                        entityName={(entity && entity['entity_text']) || 'Project'}
                        saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                        changeOrderingUp={this.changeOrderingUp}
                        changeOrderingDown={this.changeOrderingDown}
                        editHeading={(elem) => this.editHeading(elem)}
                        currentFields={this.state.currentFields}
                        handleInputValue={this.handleInputValue}
                        showAlertMessage={this.showAlertMessage}


                    />
            }
            case 'skill': {
                entity = entityList && entityList[4];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = (nextEntity && formCategoryList[nextEntity['entity_id']]) || undefined;

                return !!(showMoreSection) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button" onClick={hideMoreSection}>Back to Edit</button>
                    </div>
                    : <Skill {...this.props}
                        isEditable={isEditable}
                        handlePreview={this.handlePreview}
                        nextEntity={(nextEntity && nextEntity['link']) || nextEntity}
                        entityName={(entity && entity['entity_text']) || 'Skill'}
                        saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                        changeOrderingUp={this.changeOrderingUp}
                        changeOrderingDown={this.changeOrderingDown}
                        editHeading={(elem) => this.editHeading(elem)}
                        currentFields={this.state.currentFields}
                        handleInputValue={this.handleInputValue}
                        showAlertMessage={this.showAlertMessage}


                    />
            }
            case 'summary': {
                entity = entityList && entityList[5];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = (nextEntity && formCategoryList[nextEntity['entity_id']]) || undefined;

                return !!(showMoreSection) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button" onClick={hideMoreSection}>Back to Edit</button>
                    </div>
                    : <Summary {...this.props}
                        isEditable={isEditable}
                        handlePreview={this.handlePreview}
                        nextEntity={(nextEntity && nextEntity['link']) || nextEntity}
                        entityName={(entity && entity['entity_text']) || 'Summary'}
                        saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                        editHeading={(elem) => this.editHeading(elem)}
                        handleInputValue={this.handleInputValue}

                    />
            }
            case 'award': {
                entity = entityList && entityList[6];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = (nextEntity && formCategoryList[nextEntity['entity_id']]) || undefined;

                return !!(showMoreSection) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button" onClick={hideMoreSection}>Back to Edit</button>
                    </div>
                    : <Award {...this.props}
                        isEditable={isEditable}
                        handlePreview={this.handlePreview}
                        nextEntity={(nextEntity && nextEntity['link']) || nextEntity}
                        entityName={(entity && entity['entity_text']) || 'Award'}
                        saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                        changeOrderingUp={this.changeOrderingUp}
                        changeOrderingDown={this.changeOrderingDown}
                        editHeading={(elem) => this.editHeading(elem)}
                        currentFields={this.state.currentFields}
                        handleInputValue={this.handleInputValue}
                        showAlertMessage={this.showAlertMessage}

                    />
            }
            case 'course': {
                entity = entityList && entityList[7];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = (nextEntity && formCategoryList[nextEntity['entity_id']]) || undefined;

                return !!(showMoreSection) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button" onClick={hideMoreSection}>Back to Edit</button>
                    </div>
                    : <Course {...this.props}
                        isEditable={isEditable}
                        handlePreview={this.handlePreview}
                        nextEntity={(nextEntity && nextEntity['link']) || nextEntity}
                        entityName={(entity && entity['entity_text']) || 'Course'}
                        saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                        changeOrderingUp={this.changeOrderingUp}
                        changeOrderingDown={this.changeOrderingDown}
                        editHeading={(elem) => this.editHeading(elem)}
                        currentFields={this.state.currentFields}
                        handleInputValue={this.handleInputValue}
                        showAlertMessage={this.showAlertMessage}

                    />
            }
            case 'language': {
                entity = entityList && entityList[8];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = (nextEntity && formCategoryList[nextEntity['entity_id']]) || undefined;

                return !!(showMoreSection) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button" onClick={hideMoreSection}>Back to Edit</button>
                    </div>
                    : <Language {...this.props}
                        isEditable={isEditable}
                        handlePreview={this.handlePreview}
                        nextEntity={(nextEntity && nextEntity['link']) || nextEntity}
                        entityName={(entity && entity['entity_text']) || 'Language'}
                        saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                        changeOrderingUp={this.changeOrderingUp}
                        changeOrderingDown={this.changeOrderingDown}
                        editHeading={(elem) => this.editHeading(elem)}
                        currentFields={this.state.currentFields}
                        handleInputValue={this.handleInputValue}
                        showAlertMessage={this.showAlertMessage}

                    />
            }
            case 'reference': {
                entity = entityList && entityList[9];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = (nextEntity && formCategoryList[nextEntity['entity_id']]) || undefined;
                return !!(showMoreSection) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button" onClick={hideMoreSection}>Back to Edit</button>
                    </div>
                    : <Reference {...this.props}
                        isEditable={isEditable}
                        handlePreview={this.handlePreview}
                        nextEntity={(nextEntity && nextEntity['link']) || nextEntity}
                        entityName={(entity && entity['entity_text']) || 'Reference'}
                        saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                        changeOrderingUp={this.changeOrderingUp}
                        changeOrderingDown={this.changeOrderingDown}
                        editHeading={(elem) => this.editHeading(elem)}
                        currentFields={this.state.currentFields}
                        handleInputValue={this.handleInputValue}
                        showAlertMessage={this.showAlertMessage}

                    />
            }
            default: {
                return <Template {...this.props} />
            }

        }

    }

    render() {
        return (
            <section id='right-sidebar' className="right-sidebar">
                {
                    this.renderSwitch()
                }
            </section>
        )
    }

}

RightSection.propTypes = {
    location: propTypes.shape({
        hash: propTypes.string,
        pathname: propTypes.string,
        search: propTypes.string,
        state: undefined
    }),
    eventClicked: propTypes.func,
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
    updateEntityPreference: propTypes.func,
    entityList: propTypes.array,
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
    hideMoreSection: propTypes.func,
    userInfo: propTypes.shape({
        active_subscription: propTypes.bool,
        candidate_id: propTypes.string,
        date_of_birth: propTypes.string,
        email: propTypes.string,
        entity_preference_data: propTypes.array,
        extra_info: propTypes.string,
        extracurricular: propTypes.array,
        first_name: propTypes.string,
        free_resume_downloads: propTypes.number,
        gender: propTypes.object,
        id: propTypes.number,
        image: propTypes.string,
        interest_list: propTypes.array,
        last_name: propTypes.string,
        location: propTypes.string,
        number: propTypes.string,
        selected_template: propTypes.string,
    })
}

const mapStateToProps = (state) => {
    return {
        entityList: state.personalInfo && state.personalInfo.entity_preference_data,
        formData: state && state.form,
        ui: state && state.ui,
        userInfo: state.personalInfo
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        "updateEntityPreference": (entityList) => {
            return dispatch(actions.updateEntityPreference({ 'entity_preference_data': entityList }));
        },
        "currentForm": (formName = '') => {
            return dispatch(currentForm({ formName: formName }))
        },
        "hideMoreSection": () => {
            return dispatch(hideMoreSection())
        },
        'previewButtonClicked': (data) => {
            return dispatch(previewButtonClicked(data))
        },
    }
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(RightSection))
