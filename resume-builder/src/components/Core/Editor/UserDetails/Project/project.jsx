import React, {Component} from 'react';
import './project.scss'
import {Field, reduxForm} from "redux-form";
import * as actions from "../../../../../store/project/actions";
import {connect} from "react-redux";
import {renderField} from "../../../../FormHandler/formFieldRenderer.jsx";


class Project extends Component {

    componentDidMount() {
        this.props.fetchUserProject()
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize} = this.props;

        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-projects1"></i></span>
                    <h2>Projects</h2>
                    <span className="icon-edit icon-projects__cursor"></span>
                    <button className="add-button add-button__right">Add new</button>
                </section>

                <section className="right-sidebar-scroll">
                    <section className="info-section">
                        <div className="flex-container">
                            <h3 className="add-section-heading">Project 1</h3>
                            <div className="addon-buttons mr-10">
                                <span className="icon-delete mr-15"></span>
                                <span className="icon-ascend mr-5"></span>
                                <span className="icon-descend"></span>
                            </div>
                        </div>
                        <div className="flex-container">
                            <fieldset>
                                <label>Project Name</label>
                                <Field component={renderField} type={"text"} name="project_name"/>
                            </fieldset>
                        </div>
                        <div className="flex-container">
                            <fieldset>
                                <label>Date from</label>
                                <div className="input-group">
                                    <div className="input-group--input-group-icon">
                                        <span className="icon-date"></span>
                                    </div>
                                    <input type="text" placeholder="" className="input-control"/>
                                </div>
                            </fieldset>
                            <fieldset>
                                <label>Date to</label>
                                <div className="input-group">
                                    <div className="input-group--input-group-icon">
                                        <span className="icon-date"></span>
                                    </div>
                                    <input type="text" placeholder="" className="input-control"/>
                                </div>
                                <span className="till-today">
									<input type="radio" name="" checked/>
									Till Today
								</span>
                            </fieldset>
                        </div>

                    </section>


                </section>

                <div className="flex-container items-right mr-20 mb-30">
                    <button className="blue-button mr-10">Preview</button>
                    <button className="orange-button">Save & Continue</button>
                </div>

            </div>
        )
    }
}


export const ProjectForm = reduxForm({
    form: 'project',
    enableReinitialize: true
})(Project);


const mapStateToProps = (state) => {
    return {
        initialValues: state.project
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchUserProject": () => {
            return dispatch(actions.fetchUserProject())
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(ProjectForm);
