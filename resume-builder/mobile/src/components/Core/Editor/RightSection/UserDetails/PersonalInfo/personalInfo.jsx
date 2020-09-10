import React, { Component } from 'react';
import { connect } from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import { Field, reduxForm } from 'redux-form';
import BottomCTC from '../../../../../Common/BottomCTC/bottom-ctc';
import './personalInfo.scss';
import {
    renderField,
    datepicker,
    renderSelect,
    renderTextArea,
    renderAsyncCreatableSelect
} from "../../../../../FormHandler/formFieldRenderer.jsx";

import moment from 'moment';
import PreviewModal from "../../../Preview/changeTemplateModal";
import Subscribe from "../../../RightSection/subscribe";
import validate from "../../../../../FormHandler/validtaions/profile/validate"
import { scrollOnErrors } from "../../../../../../Utils/srollOnError";
import { defaultInterests } from "../../../../../../Utils/defaultInterests";
import propTypes from 'prop-types';

class PersonalInfo extends Component {
    constructor(props) {
        super(props);
        this.getImageURI = this.getImageURI.bind(this);
        this.removeImage = this.removeImage.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.state = {
            'imageURI': '',
            'imageURL': '',
            'editHeading': false,
            'heading': '',
            'submit': false,
            'flag': true
        }
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
    }
    
    componentDidMount() {
        if (this.props.personalInfo.entity_preference_data.length) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[0].entity_text })
        }
        
    }
    
    async handleSubmit(values) {
        let { sidenav: { listOfLinks, currentLinkPos }, generateResumeAlert, history, updateCurrentLinkPos,
        onSubmit, personalInfo } = this.props;

        const { imageURL, flag } = this.state
        currentLinkPos++
        this.setState({ submit: true })
        await onSubmit(values, imageURL, flag, personalInfo);
        if (currentLinkPos === listOfLinks.length) {
            currentLinkPos = 0
            generateResumeAlert()
        } else {
            updateCurrentLinkPos({ currentLinkPos })
            history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
        }
        
    }
    
    async updateInfoBeforeLoss() {
        if (!this.state.submit) {
            const { initialValues, personalInfo } = this.props
            const form_data = this.props.info.form.personalInfo;
            let error = false
            let error_values = form_data["syncErrors"]
            if (error_values) {
                for (let i of Object.keys(error_values)) {
                    if (error_values[i]) {
                        error = true;
                        break;
                    }
                }
            }
            if (!error && JSON.stringify(initialValues) !== JSON.stringify(form_data['values'])) {
                
                const { imageURL, flag } = this.state
                await this.props.onSubmit(form_data['values'], imageURL, flag, personalInfo);
            }
        }
        
    }
    
    async componentWillUnmount() {
        this.updateInfoBeforeLoss();
    }
    
    
    removeImage() {
        this.setState({
            imageURI: '',
            imageURL: ''
        })
    }
    
    
    componentDidUpdate(prevProps) {
        if (this.props.personalInfo.entity_preference_data !== prevProps.personalInfo.entity_preference_data) {
            this.setState({ heading: this.props.personalInfo.entity_preference_data[0].entity_text })
        }
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
            'imageURL': url,
            flag: true
        })
    }
    
    render() {
        const length = parseInt(this.props.sidenav.listOfLinks.length)
        const pos = parseInt(this.props.sidenav.currentLinkPos)
        const { handleSubmit, personalInfo, headingChange, submitting, personalInfo: { order_data }, history, fetchInterestList, updateAlertModalStatus, eventClicked } = this.props;
        const { editHeading, heading, flag } = this.state;
        const newUser = localStorage.getItem('newUser')
        return (
            
            <div className="buildResume">
                <PreviewModal {...this.props} />
                <Subscribe {...this.props} />

                <div className="buildResume__wrap">
                    <div className="buildResume__heading">
                        {!editHeading ?

                            <React.Fragment>
                                <h1 className="heading-style">{heading}</h1>
                                <i className="sprite icon--edit" onClick={() => {
                                    newUser ? updateAlertModalStatus(true) : this.setState({ editHeading: true });
                                    this.props.sendTrackingInfo('right_section_delete',1)
                                }}></i>
                                {/* <div className="toolTip">
                                <span className="toolTip--arrow-up"></span>
                                <span className="toolTip--close">+</span>
                                You can always edit the section title
                            </div> */}
                            </React.Fragment> :
                            <React.Fragment>
                                <input type="text" autoFocus defaultValue={heading} maxLength={'20'}
                                    onChange={(event) => this.setState({ heading: event.target.value })} />
                                <i className="sprite icon--editTick" onClick={() => {
                                    headingChange(personalInfo.entity_preference_data, heading, 0);
                                    this.setState({ editHeading: false })
                                }}></i>
                            </React.Fragment>

                        }
                        {/*  */}
                    </div>


                    <form onSubmit={handleSubmit(this.handleSubmit)}>

                        <ul className="form">
                            {/*  Temporary disabled closed due to expert assitance */}
                            <li className="form__group">
                                <Field component={renderField} label={"First Name"} type={"text"} name="first_name"
                                    id="first_name" disabled={order_data && order_data.id && false ? true : false}
                                    iconClass={"sprite icon--firstName"} className="form__input" prepend={true}
                                    maxLength={"20"} />
                            </li>
                            {/*  Temporary disabled closed due to expert assitance */}
                            <li className="form__group">
                                <Field component={renderField} label={"Last Name"} type={"text"} name="last_name"
                                    id="last_name" disabled={order_data && order_data.id && false ? true : false}
                                    iconClass={"sprite icon--lastName"} className="form__input" prepend={true}
                                    maxLength={"20"} />
                            </li>

                            <li className="form__group">
                                <Field component={renderSelect} label={"Gender"} name="gender" prepend={true}
                                    iconClass={"sprite icon--gender"} className="form__input form__select">
                                    <option value="">Gender</option>
                                    <option value="1">Male</option>
                                    <option value="2">Female</option>
                                    <option value="3">Others</option>
                                </Field>
                            </li>

                            <li className="form__group dob">
                                <Field component={datepicker} label={"Date Of Birth"} type={"date"} name="date_of_birth"
                                    id="date_of_birth"
                                    yearDropDownItemNumber={50} maxDateAllowed={'true'} />
                            </li>

                            <li className="form__group">
                                <Field component={renderField} label={"Mobile"} type={"number"} name="number"
                                    id="number" prepend={true}
                                    iconClass={"sprite icon--mobile"} className="form__input" pattern="\d*"
                                    maxLength={"10"} />
                            </li>

                            <li className="form__group">
                                <Field component={renderField} label={"Email"} type={"email"} name="email" id="email"
                                    prepend={true}
                                    iconClass={"sprite icon--mail"} className="form__input" />
                            </li>

                            <li className="form__group">
                                <Field component={renderTextArea} label={"Address"} type={"text"} name="location"
                                    id="location"
                                    prepend={true} iconClass={"sprite icon--address"} className="form__input"
                                    rows="4" maxLength={'100'} />
                            </li>

                            <li className="form__group">
                                <Field name="extracurricular" id="extracurricular"

                                    component={renderAsyncCreatableSelect}
                                    className={'multi-select'}
                                    defaultOptions={defaultInterests}
                                    iconClass={'sprite icon--interest'}
                                    label={'Interest'}
                                    loadOptions={(inputValue) => fetchInterestList(inputValue)}
                                    value={personalInfo.extracurricular}
                                    isMulti={true}
                                    closeMenuOnSelect={false}
                                />
                            </li>

                            <li className="form__group">
                                <div className="upload-btn-wrapper">

                                    <button className="upload-btn-wrapper__btn">
                                        <i className="sprite icon--camera"></i>
                                        Upload a file
                                    </button>
                                    <input type="file" accept="image/*" name="displayPicture"
                                        onChange={this.getImageURI.bind(this)} />
                                </div>
                            </li>

                            <li className="form__group">
                                <span className="upload--image overflow-hidden">
                                    {
                                        (this.state.imageURI || personalInfo.image) && flag ?
                                            <React.Fragment>
                                                <span className="close-wrap">
                                                    <i className="sprite icon--close" onClick={() => {
                                                        this.setState({ imageURL: '', imageURI: '', flag: false })
                                                    }}></i>
                                                </span>
                                                <img alt={"User Profile"}
                                                    src={this.state.imageURI || personalInfo.image} />
                                            </React.Fragment> :
                                            <img alt={"User Profile"}
                                                src="/media/static/react/assets/images/mobile/default-user.jpg" />
                                    }
                                </span>
                            </li>
                        </ul>
                        <BottomCTC disabled={submitting} context={this} history={history}
                            updateAlertModalStatus={updateAlertModalStatus}
                            length={length} pos={pos + 1} updateInfoBeforeLoss={this.updateInfoBeforeLoss}
                            order_data={order_data} eventClicked={eventClicked} form_name={'Personal Info'} />
                    </form>
                </div>

            </div>
        )
    }
}

PersonalInfo.propTypes = {
    eventClicked: propTypes.func,
    fetchImageUrl: propTypes.func,
    fetchInterestList: propTypes.func,
    form: propTypes.string,
    generateResumeAlert: propTypes.func,
    handleSubmit: propTypes.func,
    headingChange: propTypes.func,
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
    initialValues: propTypes.shape({
        // currentLinkPos: propTypes.number,
        listOfLinks: propTypes.array,
        sidenavStatus: propTypes.bool
    }),
    onSubmit: propTypes.func,
    personalInfo: propTypes.shape({
        date_of_birth: propTypes.string,
        email: propTypes.string,
        entity_preference_data: propTypes.array,
        extra_info: propTypes.string,
        extracurricular: propTypes.array,
        first_name: propTypes.string,
        gender: propTypes.string,
        hide_subscribe_button: propTypes.bool,
        image: propTypes.string,
        interest_list: propTypes.array,
        last_name: propTypes.string,
        location: propTypes.string,
        number: propTypes.string,
    }),
    sidenav: propTypes.shape({
        currentLinkPos: propTypes.number,
        listOfLinks: propTypes.array,
        sidenavStatus: propTypes.bool
    }),
    submitting: propTypes.bool,
    updateAlertModalStatus: propTypes.func,
    updateCurrentLinkPos: propTypes.func,
}

export const PersonalInfoForm = reduxForm({
    form: 'personalInfo',
    enableReinitialize: true,
    validate,
    onSubmitFail: (errors) => scrollOnErrors(errors, 'profile', -100),
})(PersonalInfo);


const mapStateToProps = (state) => {
    return {
        initialValues: state.personalInfo,
        personalInfo: state.personalInfo
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "onSubmit": (personalDetails, imageURL, flag, storeInfo) => {
            let { date_of_birth, extracurricular, gender, image } = personalDetails;
            const { entity_preference_data } = storeInfo;
            let interest = extracurricular
            interest = ((interest || []).filter((item) => item !== null).map((item) => item.value)).join(",")
            personalDetails = {
                ...personalDetails,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'image': imageURL || (flag ? image : ''),
                    'extracurricular': interest,
                    'gender': parseInt(gender || 0) === 0 ? '': gender,
                    'entity_preference_data': (entity_preference_data || []).map(el => el)
                }
            };
            return new Promise((resolve, reject) => {
                dispatch(actions.updatePersonalInfo({ personalDetails, resolve, reject }));
            })
        },
        "fetchImageUrl": (imageFile) => {
            return new Promise((resolve, reject) => {
                dispatch(actions.fetchImageUrl({ imageFile, resolve, reject }));
            })
        },
        "fetchInterestList": (value) => {
            if (value.length < 3) return new Promise(resolve => resolve([]));
            return new Promise((resolve, reject) => {
                return dispatch(actions.fetchInterestList({ value, resolve, reject }))
            })
        }
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(PersonalInfoForm);
