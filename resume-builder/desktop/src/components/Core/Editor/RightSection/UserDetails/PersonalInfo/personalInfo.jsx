import React, {Component} from 'react';
import './personalInfo.scss'
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {interestList} from '../../../../../../Utils/interestList'
import {
    renderField,
    datepicker,
    renderSelect,
    renderTextArea,
    renderDynamicSelect
} from "../../../../../FormHandler/formFieldRenderer.jsx";

import {
    required,
    phoneNumber,
    email
} from "../../../../../FormHandler/validations/formValidations.js";

import moment from 'moment';

export class PersonalInfo extends Component {
    constructor(props) {
        super(props);
        this.getImageURI = this.getImageURI.bind(this);
        this.removeImage = this.removeImage.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handlePreview = this.handlePreview.bind(this);
        this.fetchInterestList = this.fetchInterestList.bind(this);
        this.editHeading = this.editHeading.bind(this);
        this.saveTitle = this.saveTitle.bind(this);


        this.state = {
            'imageURI': '',
            'imageURL': '',
            'isEditable': false
        }
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
    }

    editHeading() {
        this.setState({
            'isEditable': true
        })
        setTimeout(() => {
            this.refs.personalInfo.focus();
        }, 0)


    }

    saveTitle(event) {
        event.stopPropagation()
        if (event.keyCode === 13) {
            this.setState({
                'isEditable': false
            })
        }
    }

    componentDidMount() {
        this.props.fetchPersonalInfo();
    }

    async handleSubmit(values) {
        await this.props.onSubmit(values, this.state.imageURL);
        this.props.history.push('/resume-builder/edit/?type=summary');
    }

    handlePreview() {
        this.props.history.push('/resume-builder/preview/');
    }

    removeImage() {
        this.setState({
            imageURI: '',
            imageURL: ''
        })
    }

    async fetchInterestList(inputValue, callback) {
        // try {
        //     const interests = await this.props.fetchInterest(inputValue);
        //     const listData = (skills && skills.results || []).map(skill => ({value: skill.id, label: skill.name}))
        //     callback(listData);
        // } catch (e) {
        //     console.log('--error-', e);
        // }
        console.log('---', inputValue)
        return [];
    }

    async getImageURI(event) {
        let reader = new FileReader();
        reader.onload = (event) => {

            this.setState({
                imageURI: event.target.result
            })

        };
        reader.readAsDataURL(event.target.files[0]);

        let url = await this.props.fetchImageUrl(event.target.files[0]);
        this.setState({
            'imageURL': url
        })
    }

    render() {
        const {handleSubmit, personalInfo, ui: {loader}} = this.props;
        const {isEditable} = this.state;
        console.log('staticUrl -----', `${this.staticUrl}react/assets/images/upload-image.jpg`)
        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-info1"/></span>
                    <h2  ref={"personalInfo"} onKeyUp={(event) => this.saveTitle(event)}
                        contenteditable={!!(isEditable) ? "true" : "false"}>Personal Info</h2>
                    <span onClick={this.editHeading} className={!!(!isEditable) ? "icon-edit icon-edit__cursor" : ''}/>
                </section>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <section className="flex-container right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <fieldset className="error">
                                    <label>First Name</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-name"></span>
                                        </div>
                                        <Field component={renderField} validate={required} type={"text"}
                                               name="first_name"/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Last Name</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-surname"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="last_name"/>
                                    </div>
                                </fieldset>
                            </div>

                            <div className="flex-container">
                                <fieldset className="custom">
                                    <label>Gender</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-gender"></span>
                                        </div>
                                        <Field
                                            name="gender"
                                            component={renderSelect}
                                            label="Gender"
                                            isMulti={false}
                                            options={[
                                                {value: '1', label: 'Male'},
                                                {value: '2', label: 'Female'},
                                                {value: '3', label: 'Other'}
                                            ]}
                                        />
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Date Of Birth</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-date"></span>
                                        </div>
                                        <Field component={datepicker} validate={required} name="date_of_birth"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Mobile</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-mobile"></span>
                                        </div>
                                        <Field component={renderField} validate={[required, phoneNumber]}
                                               type={"text"}
                                               name="number"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Email</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-email"></span>
                                        </div>
                                        <Field component={renderField} validate={[required, email]} type={"text"}
                                               name="email"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>

                            </div>

                            <div className="flex-container">
                                <fieldset className="custom">
                                    <label>Interest</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-interest"></span>
                                        </div>
                                        <Field name="extracurricular" component={renderDynamicSelect}
                                            // loadOptions={this.fetchInterestList.bind(this)}
                                               defaultOptions={Object.keys(interestList).map(key => interestList[key])}
                                               value={personalInfo.extracurricular}
                                               label="Select Interest"/>
                                    </div>
                                </fieldset>
                            </div>

                            <div className="flex-container">
                                <fieldset>
                                    <label>Address</label>
                                    <div className="input-group address">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-address"></span>
                                        </div>
                                        <Field component={renderTextArea} type={"textarea"} name="location"
                                               className={"input-control"} rows="3"/>
                                    </div>
                                </fieldset>
                            </div>

                            {/*<div className="flex-container">*/}
                            {/*<fieldset>*/}
                            {/*<label>Linkedin</label>*/}
                            {/*<div className="input-group">*/}
                            {/*<div className="input-group--input-group-icon">*/}
                            {/*<span className="icon-linkedin"></span>*/}
                            {/*</div>*/}
                            {/*<Field component={renderField} type={"text"} name="linkedIn"*/}
                            {/*className={"input-control"}/>*/}
                            {/*</div>*/}
                            {/*</fieldset>*/}
                            {/*<fieldset>*/}
                            {/*<label>Facebook</label>*/}
                            {/*<div className="input-group">*/}
                            {/*<div className="input-group--input-group-icon">*/}
                            {/*<span className="icon-facebook"></span>*/}
                            {/*</div>*/}
                            {/*<Field component={renderField} type={"text"} name="facebook"*/}
                            {/*className={"input-control"}/>*/}
                            {/*</div>*/}
                            {/*</fieldset>*/}
                            {/*</div>*/}

                        </section>
                        <section className="pic-section mt-30">
                            {
                                this.state.imageURI || personalInfo.image ?
                                    <div className='upper-cross' onClick={this.removeImage.bind(this)}>
                                        <i className='icon-close'></i>
                                    </div> : ''
                            }

                            <label>

                                {
                                    this.state.imageURI || personalInfo.image ?
                                        <img alt={"User Profile"} className='img-responsive'
                                             src={this.state.imageURI || personalInfo.image}/> :
                                        <img alt={"User Profile"} className="img-responsive"
                                             src={`${this.staticUrl}react/assets/images/upload-image.jpg`}/>
                                }
                                <input accept="image/*" type="file" name="displayPicture"
                                       onChange={this.getImageURI.bind(this)}
                                       style={{opacity: 0}}/>
                                <Field type={"text"} name={"image"} component={renderField}
                                       value={this.state.imageURL} className={'zero-opacity'}/>
                            </label>

                        </section>
                    </section>


                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10" onClick={this.handlePreview}>Preview</button>
                        <button className="orange-button" type="submit">Save &
                            Continue
                        </button>
                    </div>
                </form>
            </div>
        )
    }
}

export const PersonalInfoForm = reduxForm({
    form: 'personalInfo',
    enableReinitialize: true
})(PersonalInfo);


const mapStateToProps = (state) => {
    return {
        initialValues: state.personalInfo,
        personalInfo: state.personalInfo,
        ui: state.ui
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchPersonalInfo": () => {
            return dispatch(actions.fetchPersonalInfo())
        },
        "onSubmit": (personalDetails, imageURL) => {
            const {gender, date_of_birth, extracurricular} = personalDetails;
            personalDetails = {
                ...personalDetails,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'gender': (gender && gender['value']) || '',
                    'image': imageURL,
                    'extracurricular': extracurricular instanceof Array ?
                        (extracurricular || []).map(el => el.value).join(',') : extracurricular
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(actions.updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
        "fetchImageUrl": (imageFile) => {
            return new Promise((resolve, reject) => {
                dispatch(actions.fetchImageUrl({imageFile, resolve, reject}));
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(PersonalInfoForm);
