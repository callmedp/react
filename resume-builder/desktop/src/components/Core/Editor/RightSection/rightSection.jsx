import React, {Component} from 'react';
import {connect} from "react-redux";
import './rightSection.scss'
import PersonalInfo from './UserDetails/PersonalInfo/personalInfo.jsx'
import Education from './UserDetails/Education/education.jsx'
import Experience from './UserDetails/Experience/experience.jsx'
import Language from './UserDetails/Language/language.jsx'
import Skill from './UserDetails/Skill/skill.jsx'
import Summary from './UserDetails/Summary/summary.jsx'
import Award from './UserDetails/Award/award.jsx'
import Project from './UserDetails/Project/project.jsx'
import Reference from './UserDetails/Reference/reference.jsx'
import Course from './UserDetails/Course/course.jsx'
import Template from './Template/template.jsx'
import queryString from 'query-string'
import * as actions from '../../../../store/personalInfo/actions'
import {formCategoryList} from "../../../../Utils/formCategoryList";


class RightSection extends Component {
    constructor(props) {
        super(props);
        const values = queryString.parse(this.props.location.search)
        this.renderSwitch = this.renderSwitch.bind(this);
        this.saveTitle = this.saveTitle.bind(this);
        this.editHeading = this.editHeading.bind(this);
        this.handlePreview = this.handlePreview.bind(this);


        this.state = {
            type: (values && values.type) || '',
            'isEditable': false
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


    handlePreview() {
        this.props.history.push('/resume-builder/preview/');
    }


    editHeading(elem) {
        this.setState({
            'isEditable': true
        });
        setTimeout(() => {
            elem.focus()
        }, 0)


    }

    saveTitle(event, entityId) {
        event.stopPropagation();
        if (event.keyCode === 13) {
            this.setState({
                'isEditable': false
            });
            let {entityList} = this.props;
            if (entityList && entityList.length) {
                entityList[entityId]['entity_text'] = event.target.textContent || '';
                this.props.updateEntityPreference(entityList)
            }

        }
    }

    changeOrderingUp(index, fields, event) {
        event.stopPropagation();
        console.log('---', fields.getAll());
        let currentItem = fields.get(index);
        let prevItem = fields.get(index - 1);
        currentItem['order'] = index - 1;
        prevItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index - 1)
        fields.insert(index - 1, prevItem)
        fields.swap(index, index - 1)
        // this.props.handleSwap([currentItem, prevItem])
    }

    changeOrderingDown(index, fields, event) {
        event.stopPropagation();
        let currentItem = fields.get(index);
        let nextItem = fields.get(index + 1);
        currentItem['order'] = index + 1;
        nextItem['order'] = index;
        fields.remove(index)
        fields.insert(index, currentItem)
        fields.remove(index + 1)
        fields.insert(index + 1, nextItem)
        fields.swap(index, index + 1);

        // this.props.handleSwap([currentItem, nextItem])
    }

    renderSwitch() {
        const {entityList} = this.props;
        let entity, nextEntity;
        const {isEditable} = this.state;

        switch (this.state.type) {
            case 'profile': {
                entity = entityList && entityList[0];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = nextEntity && formCategoryList[nextEntity['entity_id']] || undefined;
                return <PersonalInfo {...this.props}
                                     isEditable={isEditable}
                                     saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                                     handlePreview={this.handlePreview}
                                     entityName={entity && entity['entity_text'] || 'Personal Info'}
                                     nextEntity={nextEntity && nextEntity['link'] || nextEntity}
                                     editHeading={(elem) => this.editHeading(elem)}
                />
            }

            case 'education': {
                entity = entityList && entityList[1];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = nextEntity && formCategoryList[nextEntity['entity_id']] || undefined;

                return !!(!(entity && entity.active)) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button">Back to Edit</button>
                    </div>
                    : <Education {...this.props}
                                 isEditable={isEditable}
                                 handlePreview={this.handlePreview}
                                 editHeading={(elem) => this.editHeading(elem)}
                                 entityName={entity && entity['entity_text'] || 'Education'}
                                 nextEntity={nextEntity && nextEntity['link'] || nextEntity}
                                 changeOrderingUp={this.changeOrderingUp}
                                 changeOrderingDown={this.changeOrderingDown}
                                 saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                    />
            }

            case 'experience': {
                entity = entityList && entityList[2];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = nextEntity && formCategoryList[nextEntity['entity_id']] || undefined;
                return !!(!(entity && entity.active)) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button">Back to Edit</button>
                    </div>
                    : <Experience {...this.props}
                                  isEditable={isEditable}
                                  handlePreview={this.handlePreview}
                                  nextEntity={nextEntity && nextEntity['link'] || nextEntity}
                                  entityName={entity && entity['entity_text'] || 'Experience'}
                                  saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                                  changeOrderingUp={this.changeOrderingUp}
                                  changeOrderingDown={this.changeOrderingDown}
                                  editHeading={(elem) => this.editHeading(elem)}
                    />
            }

            case 'project': {
                entity = entityList && entityList[3];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = nextEntity && formCategoryList[nextEntity['entity_id']] || undefined;
                return !!(!(entity && entity.active)) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button">Back to Edit</button>
                    </div>
                    : <Project {...this.props}
                               isEditable={isEditable}
                               handlePreview={this.handlePreview}
                               nextEntity={nextEntity && nextEntity['link'] || nextEntity}
                               entityName={entity && entity['entity_text'] || 'Project'}
                               saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                               changeOrderingUp={this.changeOrderingUp}
                               changeOrderingDown={this.changeOrderingDown}
                               editHeading={(elem) => this.editHeading(elem)}
                    />
            }
            case 'skill': {
                entity = entityList && entityList[4];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = nextEntity && formCategoryList[nextEntity['entity_id']] || undefined;

                return !!(!(entity && entity.active)) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button">Back to Edit</button>
                    </div>
                    : <Skill {...this.props}
                             isEditable={isEditable}
                             handlePreview={this.handlePreview}
                             nextEntity={nextEntity && nextEntity['link'] || nextEntity}
                             entityName={entity && entity['entity_text'] || 'Skill'}
                             saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                             changeOrderingUp={this.changeOrderingUp}
                             changeOrderingDown={this.changeOrderingDown}
                             editHeading={(elem) => this.editHeading(elem)}
                    />
            }
            case 'summary': {
                entity = entityList && entityList[5];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = nextEntity && formCategoryList[nextEntity['entity_id']] || undefined;

                return !!(!(entity && entity.active)) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button">Back to Edit</button>
                    </div>
                    : <Summary {...this.props}
                               isEditable={isEditable}
                               handlePreview={this.handlePreview}
                               nextEntity={nextEntity && nextEntity['link'] || nextEntity}
                               entityName={entity && entity['entity_text'] || 'Summary'}
                               saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                               editHeading={(elem) => this.editHeading(elem)}
                    />
            }
            case 'award': {
                entity = entityList && entityList[6];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = nextEntity && formCategoryList[nextEntity['entity_id']] || undefined;

                return !!(!(entity && entity.active)) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button">Back to Edit</button>
                    </div>
                    : <Award {...this.props}
                             isEditable={isEditable}
                             handlePreview={this.handlePreview}
                             nextEntity={nextEntity && nextEntity['link'] || nextEntity}
                             entityName={entity && entity['entity_text'] || 'Award'}
                             saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                             changeOrderingUp={this.changeOrderingUp}
                             changeOrderingDown={this.changeOrderingDown}
                             editHeading={(elem) => this.editHeading(elem)}
                    />
            }
            case 'course': {
                entity = entityList && entityList[7];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = nextEntity && formCategoryList[nextEntity['entity_id']] || undefined;

                return !!(!(entity && entity.active)) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button">Back to Edit</button>
                    </div>
                    : <Course {...this.props}
                              isEditable={isEditable}
                              handlePreview={this.handlePreview}
                              nextEntity={nextEntity && nextEntity['link'] || nextEntity}
                              entityName={entity && entity['entity_text'] || 'Course'}
                              saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                              changeOrderingUp={this.changeOrderingUp}
                              changeOrderingDown={this.changeOrderingDown}
                              editHeading={(elem) => this.editHeading(elem)}
                    />
            }
            case 'language': {
                entity = entityList && entityList[8];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = nextEntity && formCategoryList[nextEntity['entity_id']] || undefined;

                return !!(!(entity && entity.active)) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button">Back to Edit</button>
                    </div>
                    : <Language {...this.props}
                                isEditable={isEditable}
                                handlePreview={this.handlePreview}
                                nextEntity={nextEntity && nextEntity['link'] || nextEntity}
                                entityName={entity && entity['entity_text'] || 'Language'}
                                saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                                changeOrderingUp={this.changeOrderingUp}
                                changeOrderingDown={this.changeOrderingDown}
                                editHeading={(elem) => this.editHeading(elem)}
                    />
            }
            case 'reference': {
                entity = entityList && entityList[9];
                nextEntity = entityList && entityList.find(el => el['entity_id'] > entity['entity_id'] && el['active'] === true);
                nextEntity = nextEntity && formCategoryList[nextEntity['entity_id']] || undefined;
                return !!(!(entity && entity.active)) ?
                    <div className="backtoedit">
                        <p>Add more section in your resume from left panel</p>
                        <button className="orange-button">Back to Edit</button>
                    </div>
                    : <Reference {...this.props}
                                 isEditable={isEditable}
                                 handlePreview={this.handlePreview}
                                 nextEntity={nextEntity && nextEntity['link'] || nextEntity}
                                 entityName={entity && entity['entity_text'] || 'Reference'}
                                 saveTitle={(event, entityId) => this.saveTitle(event, entityId)}
                                 changeOrderingUp={this.changeOrderingUp}
                                 changeOrderingDown={this.changeOrderingDown}
                                 editHeading={(elem) => this.editHeading(elem)}
                    />
            }
            default: {
                return <Template {...this.props} />
            }

        }

    }

    render() {
        const {type} = this.state;
        return (
            <section className="right-sidebar">
                {
                    this.renderSwitch()
                }
            </section>
        )
    }

}


const mapStateToProps = (state) => {
    return {
        entityList: state.personalInfo && state.personalInfo.entity_preference_data,
        formData: state && state.form
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        "updateEntityPreference": (entityList) => {
            return dispatch(actions.updateEntityPreference({'entity_preference_data': entityList}));
        }
    }
}

export default connect(mapStateToProps, mapDispatchToProps)(RightSection)
