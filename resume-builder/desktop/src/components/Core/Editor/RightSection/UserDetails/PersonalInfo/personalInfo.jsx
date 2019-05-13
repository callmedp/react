import React, {Component} from 'react';
import styles from './personalInfo.scss'
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

import validate from '../../../../../FormHandler/validations/personalInfo/validate'

import moment from 'moment';
import LoaderSection from "../../../../../Loader/loaderSection.jsx";

export class PersonalInfo extends Component {
    constructor(props) {
        super(props);
        this.getImageURI = this.getImageURI.bind(this);
        this.removeImage = this.removeImage.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.fetchInterestList = this.fetchInterestList.bind(this);


        this.state = {
            'imageURI': '',
            'imageURL': '',
            flag: true,
            submit: false
        }
        this.staticUrl = window && window.config && window.config.staticUrl || '/media/static/'
    }


    componentDidMount() {
        this.props.fetchPersonalInfo();
    }

    async handleSubmit(values, entityLink) {
        await this.props.onSubmit(values, this.state.imageURL, this.state.flag);
        this.setState({
            submit: true
        })
        if (entityLink) this.props.history.push(entityLink);
        else this.props.history.push('/resume-builder/buy/')
    }

    removeImage() {
        console.log(' here');
        this.setState({
            imageURI: '',
            imageURL: '',
            flag: false
        });
    }


    componentWillUnmount() {
        let {formData: {personalInfo: {values, syncErrors}}} = this.props;
        let error = false;
        Object.keys(syncErrors || {}).map(key => (!!syncErrors[key] ? error = true : false));
        if (!error && !this.state.submit) this.props.onSubmit(values, this.state.imageURL, this.state.flag)
    }

    async fetchInterestList(inputValue, callback) {
        // try {
        //     const interests = await this.props.fetchInterest(inputValue);
        //     const listData = (skills && skills.results || []).map(skill => ({value: skill.id, label: skill.name}))
        //     callback(listData);
        // } catch (e) {
        //     console.log('--error-', e);
        // }
        console.log('---', inputValue);
        return [];
    }


    async getImageURI(event) {
        let reader = new FileReader();
        reader.onload = (event) => {

            this.setState({
                imageURI: event.target.result,
                flag: true
            })
        };
        reader.readAsDataURL(event.target.files[0]);

        let url = await this.props.fetchImageUrl(event.target.files[0]);
        this.setState({
            'imageURL': url,
            flag: true
        })
    }

    render() {
        const {
            handleSubmit, personalInfo, ui: {loader}, isEditable,
            editHeading, saveTitle, entityName, nextEntity, handlePreview
        } = this.props;
        let elem = null;
        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-info1"/></span>
                    {
                        <h2 ref={(value) => {
                            elem = value
                        }} onKeyUp={(event) => saveTitle(event, 0)}
                            contenteditable={!!(isEditable) ? "true" : "false"}>{entityName}
                        </h2>
                    }
                    <span onClick={() => editHeading(elem)}
                          className={!!(!isEditable) ? "icon-edit " + styles['icon-edit__cursor'] : ''}/>
                </section>
                <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                    <section className="flex-container right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <fieldset>
                                    <label>First Name</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-name"></span>
                                        </div>
                                        <Field component={renderField} type={"text"}
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
                                        <Field component={datepicker} name="date_of_birth"
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
                                        <Field component={renderField}
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
                                        <Field component={renderField} type={"text"}
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
                                this.state.imageURI || personalInfo.image && this.state.flag ?
                                    <div className={styles['upper-cross']} onClick={this.removeImage.bind(this)}>
                                        <i className='icon-close'></i>
                                    </div> : ''
                            }

                            <label>

                                {
                                    this.state.imageURI || personalInfo.image && this.state.flag ?
                                        <img alt={"User Profile"} className='img-responsive'
                                             src={this.state.imageURI || personalInfo.image}/> :
                                        <img alt={"User Profile"} className="img-responsive"
                                             src={`${this.staticUrl}react/assets/images/upload-image.jpg`}/>
                                }
                                <input accept="image/*" type="file" name="displayPicture"
                                       onChange={this.getImageURI.bind(this)}
                                       style={{opacity: 0}}/>
                                <Field type={"text"} name={"image"} component={renderField}
                                       value={this.state.imageURL} className={styles['zero-opacity']}/>
                            </label>

                        </section>
                    </section>


                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10" type={"button"} onClick={handlePreview}>Preview</button>
                        <button className="orange-button" type="submit">{!nextEntity ? "Download" : 'Save and Continue'}
                        </button>
                    </div>
                </form>
            </div>
        )
    }
}

export const PersonalInfoForm = reduxForm({
    form: 'personalInfo',
    enableReinitialize: true,
    validate
})(PersonalInfo);


const mapStateToProps = (state) => {
    return {
        initialValues: state.personalInfo,
        personalInfo: state.personalInfo,
        ui: state.ui,
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchPersonalInfo": () => {
            return dispatch(actions.fetchPersonalInfo())
        },
        "onSubmit": (personalDetails, imageURL, flag) => {
            const {gender, date_of_birth, extracurricular, image} = personalDetails;
            console.log('-------', image, flag)
            personalDetails = {
                ...personalDetails,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'gender': (gender && gender['value']) || '',
                    'image': imageURL || (flag ? image : ''),
                    'extracurricular': extracurricular instanceof Array ?
                        (extracurricular || []).map(el => el.value).join(',') : extracurricular
                }
            }
            console.log('----', personalDetails);
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
