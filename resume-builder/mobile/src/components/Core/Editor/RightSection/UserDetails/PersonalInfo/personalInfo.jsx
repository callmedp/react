import React, {Component} from 'react';
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {interestList} from '../../../../../../Utils/interestList';
import './personalInfo.scss';
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
} from "../../../../../FormHandler/formValidations.js";

import moment from 'moment';
import PreviewModal from "../../../Preview/previewModal";

class PersonalInfo extends Component {
    constructor(props) {
        super(props);
        this.getImageURI = this.getImageURI.bind(this);
        this.removeImage = this.removeImage.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handlePreview = this.handlePreview.bind(this);
        this.fetchInterestList = this.fetchInterestList.bind(this);
        this.state = {
            'imageURI': '',
            'imageURL': ''
        }

    }

    componentDidMount() {
        this.props.fetchPersonalInfo()
    }

    async handleSubmit(values) {
        let {listOfLinks,currentLinkPos} = this.props.sidenav
        currentLinkPos++
        if(currentLinkPos > listOfLinks.length){
            currentLinkPos = 0
        }
        await this.props.onSubmit(values, this.state.imageURL);
        this.props.history.push(`/resume-builder/edit/?type=${listOfLinks[currentLinkPos]}`)
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
        console.log(url)

        this.setState({
            'imageURL': url
        })
    }

    render() {
        const {handleSubmit, personalInfo} = this.props;
        return (
        <div className="buildResume">
            <PreviewModal {...this.props}/>
            <div className="buildResume__wrap">
                <div className="buildResume__heading">
                    <h2>Personal Info</h2>
                    <i className="sprite icon--edit"></i>
                </div>
                <form onSubmit={handleSubmit(this.handleSubmit)}>
                    <ul className="form">
                        <li className="form__group">
                            <label className="form__label" htmlFor="first_name">First Name</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--firstName"></i>
                                    </span>
                                </div>
                                <Field component={renderField} type={"text"} name="first_name" validate={required}
                                    className="form__input" aria-label="first_name" id="first_name"/>
                            </div>
                        </li>

                        <li className="form__group">
                            <label className="form__label" htmlFor="last_name">Last Name</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--lastName"></i>
                                    </span>
                                </div>
                                <Field component={renderField} type={"text"} name="last_name" validate={required}
                                    className="form__input" aria-label="last_name" id="last_name"/>
                            </div>
                        </li>

                        <li className="form__group">
                            <label className="form__label" htmlFor="gender">Gender</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--designation"></i>
                                    </span>
                                </div>
                                <Field name="gender" validate={required} component={renderSelect} 
                                    className="form__input form__select">
                                    <option value="">Gender</option>
                                    <option value="1" >Male</option>
                                    <option value="2" >Female</option>
                                    <option value="3">Others</option>
                                </Field>
                            </div>
                        </li>
                        
                        <li className="form__group">
                            <label className="form__label" htmlFor="date_of_birth">Date Of Birth</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--date"></i>
                                    </span>
                                </div>
                                <Field component={datepicker} validate={required} type={"date"} 
                                 name="date_of_birth" aria-label="date_of_birth" id="date_of_birth"/>
                            </div>
                        </li>
                        
                        <li className="form__group">
                            <label className="form__label" htmlFor="number">Mobile</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--mobile"></i>
                                    </span>
                                </div>
                                <Field component={renderField} validate={[required,phoneNumber]} type={"text"} name="number"
                                        className="form__input" aria-label="number" id="number"/>
                            </div>
                        </li>

                        <li className="form__group">
                            <label className="form__label" htmlFor="email">Email</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--mail"></i>
                                    </span>
                                </div>
                                <Field component={renderField} validate={[required,email]} type={"email"} name="email"
                                    className="form__input" aria-label="email" id="email"/>
                            </div>
                        </li>

                        <li className="form__group">
                            <label className="form__label" htmlFor="location">Address</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--address"></i>
                                    </span>
                                </div>
                                <Field component={renderTextArea} type={"text"} name="location" row="4"
                                    aria-label="address" id="address" className="form__input"/>
                            </div>
                        </li>


                        <li className="form__group">
                            <label className="form__label" htmlFor="extracurricular">Interest</label>
                            <div className="input-group">
                                <div className="input-group__prepend">
                                    <span className="input-group__text">
                                        <i className="sprite icon--facebook"></i>
                                    </span>
                                </div>
                                <Field name="extracurricular" component={renderDynamicSelect}
                                            className="form__input"
                                           defaultOptions={Object.keys(interestList).map(key => interestList[key])}
                                           value={personalInfo.extracurricular}
                                           aria-label="extracurricular" id="extracurricular"
                                           label="Select Interest"/>
                            </div>
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
                            <span className="upload--image">
                            {
                                this.state.imageURI || personalInfo.image ?
                                    <img alt={"User Profile"}
                                            src={this.state.imageURI || personalInfo.image}/> :
                                    <img alt={"User Profile"}
                                            src="/media/static/react/assets/images/mobile/default-user.jpg"/>
                            }
                            </span>
                        </li>

                        <li className="form__group">
                            <div className="btn-wrap">
                                <button className="btn btn__round btn--outline" 
                                    onClick={()=>{this.props.updateModalStatus({modal_status:true})}} 
                                    type={'button'}>Preview</button>
                                <button className="btn btn__round btn__primary">Save &amp; Continue</button>
                            </div>
                        </li>
                    </ul>
                </form>
            </div>
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
        personalInfo: state.personalInfo
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
                    'image': imageURL,
                    'extracurricular' : ''
                    // 'extracurricular': extracurricular instanceof Array ?
                    //     (extracurricular || []).map(el => el.value).join(',') : extracurricular
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
