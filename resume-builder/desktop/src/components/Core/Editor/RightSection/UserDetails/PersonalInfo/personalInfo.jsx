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

const filterValues = (inputValue, values) => {
    return values.filter(i =>
        i.label.toLowerCase().includes(inputValue.toLowerCase())
    );
};

const promiseOptions = (inputValue, values) =>
    new Promise(resolve => {
        setTimeout(() => {
            resolve(filterValues(inputValue, values));
        }, 1000);
    });

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
        this.props.currentForm('profile');

    }


    componentDidMount() {
        this.props.fetchPersonalInfo();
        this.props.fetchInterestList();
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
        this.setState({
            imageURI: '',
            imageURL: '',
            flag: false
        });
    }


    componentWillUnmount() {
        let {formData: {profile: {values, syncErrors}}} = this.props;
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
            editHeading, saveTitle, entityName, nextEntity, handlePreview,  handleInputValue
        } = this.props;
        let elem = null;
        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-info1"/></span>
                    {!!(!isEditable) ?
                        <h2>{entityName}
                        </h2> :
                        <React.Fragment>
                            <input autoFocus type="text" name="" defaultValue={entityName}
                                   onChange={(value) => handleInputValue(value || entityName)}/>
                            <span onClick={(event) => saveTitle(event, 0)} className="icon-tick"/>
                        </React.Fragment>
                    }
                    <span onClick={() => editHeading(elem)}
                          className={!!(!isEditable) ? "icon-edit " + styles['icon-edit__cursor'] : ''}/>

                </section>
                <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
                    <section id="personal-section" className="flex-container right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <fieldset>
                                    <label>First Name</label>

                                    <Field component={renderField} type={"text"} iconClass={'icon-name'}
                                           name="first_name"/>
                                </fieldset>
                                <fieldset>
                                    <label>Last Name</label>
                                    <Field component={renderField}
                                           iconClass={'icon-surname'}
                                           type={"text"} name="last_name"/>
                                </fieldset>
                            </div>

                            <div className="flex-container">
                                <fieldset className="custom">
                                    <label>Gender</label>
                                    <Field
                                        name="gender"
                                        iconClass={'icon-gender'}
                                        component={renderSelect}
                                        label="Gender"
                                        isMulti={false}
                                        closeMenuOnSelect={true}
                                        options={[
                                            {value: '1', label: 'Male'},
                                            {value: '2', label: 'Female'},
                                            {value: '3', label: 'Other'}
                                        ]}
                                    />
                                </fieldset>
                                <fieldset>
                                    <label>Date Of Birth</label>
                                    <Field yearDropDownItemNumber={50}
                                           iconClass={'icon-date'}
                                           component={datepicker} name="date_of_birth"
                                           className={"input-control"}/>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Mobile</label>
                                    <Field component={renderField}
                                           type={"text"}
                                           name="number"
                                           iconClass={'icon-mobile'}
                                           className={"input-control"}/>
                                </fieldset>
                                <fieldset>
                                    <label>Email</label>
                                    <Field component={renderField} type={"text"}
                                           name="email"
                                           iconClass={'icon-email'}
                                           className={"input-control"}/>
                                </fieldset>
                            </div>

                            <div className="flex-container">
                                <fieldset>
                                    <label>Address</label>
                                    <Field component={renderTextArea}
                                           iconClass={'icon-address'}
                                           type={"textarea"}
                                           name="location"
                                           className={"input-control"} rows="3"/>
                                </fieldset>
                            </div>

                            <div className="flex-container">
                                <fieldset id="interest-select" className="custom">
                                    <label>Interest</label>
                                    <Field name="extracurricular" component={renderDynamicSelect}
                                        // loadOptions={this.fetchInterestList.bind(this)}
                                           defaultOptions={Object.keys(personalInfo.interest_list).map(key => personalInfo.interest_list[key])}
                                           value={personalInfo.extracurricular}
                                           isMulti={true}
                                           closeMenuOnSelect={false}
                                           iconClass={'icon-interest'}
                                           label="Select Interest"/>
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
                                <Field type={"text"} name={"image"} component={'input'}
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
    form: 'profile',
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
        "fetchInterestList": () => {
            return dispatch(actions.fetchInterestList())
        },
        "onSubmit": (personalDetails, imageURL, flag) => {
            const {gender, date_of_birth, extracurricular, image} = personalDetails;
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
