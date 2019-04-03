import React, {Component} from 'react';
import './personalInfo.scss'
import {connect} from "react-redux";
import * as actions from '../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {renderField, datepicker, renderSelect} from "../../../../FormHandler/formFieldRenderer.jsx";
import moment from 'moment';

export class PersonalInfo extends Component {
    constructor(props) {
        super(props);
        this.getImageURI = this.getImageURI.bind(this);
        this.removeImage = this.removeImage.bind(this);
        this.state = {
            'imageURI': '',
            'imageURL': ''
        }

    }

    componentDidMount() {
        this.props.fetchPersonalInfo()
    }


    removeImage() {
        this.setState({
            imageURI: '',
            imageURL: ''
        })
    }

    async getImageURI(event) {
        let reader = new FileReader();
        reader.onload = (event) => {

            this.setState({
                imageURI: event.target.result
            })
            console.log('---', event.target.result)

        };
        reader.readAsDataURL(event.target.files[0]);

        let url = await this.props.fetchImageUrl(event.target.files[0]);

        this.setState({
            'imageURL': url
        })
    }

    render() {
        const {error, handleSubmit, pristine, reset, submitting, enableReinitialize, personalInfo} = this.props;
        console.log('---', this.props);
        return (
            <div>
                <section className="head-section">
                    <span className="icon-box"><i className="icon-info1"></i></span>
                    <h2>Personal Info</h2>
                    <span className="icon-edit icon-edit__cursor"></span>
                </section>
                <form onSubmit={handleSubmit((values) => {
                    this.props.onSubmit(values, this.state.imageURL);
                })}>
                    <section className="flex-container right-sidebar-scroll">
                        <section className="info-section">
                            <div className="flex-container">
                                <fieldset className="error">
                                    <label>First Name</label>
                                    <Field component={renderField} type={"text"} name="first_name"/>
                                    <span className="error-txt"></span>
                                </fieldset>
                                <fieldset>
                                    <label>Last Name</label>
                                    <Field component={renderField} type={"text"} name="last_name"/>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Gender</label>
                                    <Field
                                        name="gender"
                                        component={renderSelect}
                                        label="Gender"
                                        options={[
                                            {value: '1', label: 'Male'},
                                            {value: '2', label: 'Female'},
                                            {value: '3', label: 'Other'}
                                        ]}
                                    />
                                </fieldset>
                                <fieldset>
                                    <label>Date Of Birth</label>
                                    <Field component={datepicker} name="date_of_birth" className={"input-control"}/>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Mobile</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-mobile"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="number"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                                <fieldset>
                                    <label>Email</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-email"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="email"
                                               className={"input-control"}/>
                                    </div>
                                </fieldset>
                            </div>
                            <div className="flex-container">
                                <fieldset>
                                    <label>Address</label>
                                    <div className="input-group">
                                        <div className="input-group--input-group-icon">
                                            <span className="icon-address"></span>
                                        </div>
                                        <Field component={renderField} type={"text"} name="location"
                                               className={"input-control"}/>
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
                            <img className="img-responsive" src="/media/static/react/assets/images/upload-image.jpg"/>

                            <label>
                                        <span className="plus-img"><i className="fa fa-plus"
                                                                      aria-hidden="true"></i></span>
                                <input accept="image/*" type="file" name="displayPicture"
                                       onChange={this.getImageURI.bind(this)}
                                       style={{opacity: 0}}/>
                                <Field type={"text"} name={"image"} component={renderField}
                                       value={this.state.imageURL} className={'zero-opacity'}/>
                            </label>
                            {
                                this.state.imageURI || personalInfo.image ?
                                    <div className='upper-cross' onClick={this.removeImage.bind(this)}>
                                        <i className='fa fa-times'></i>
                                    </div> : ''
                            }
                            {
                                this.state.imageURI || personalInfo.image ?
                                    <img className='img-responsive'
                                         src={this.state.imageURI || personalInfo.image}/> : ""
                            }

                        </section>
                    </section>


                    <div className="flex-container items-right mr-20 mb-30">
                        <button className="blue-button mr-10">Preview</button>
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
        personalInfo: state.personalInfo
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchPersonalInfo": () => {
            return dispatch(actions.fetchPersonalInfo())
        },
        "onSubmit": (personalDetails, imageURL) => {
            console.log('0----', imageURL);
            personalDetails = {
                ...personalDetails,
                ...{
                    'date_of_birth': personalDetails['date_of_birth'] && moment(personalDetails['date_of_birth']).format('YYYY-MM-DD') || '',
                    'gender': personalDetails['gender'] && personalDetails['gender']['value'] || '',
                    'image': imageURL
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
