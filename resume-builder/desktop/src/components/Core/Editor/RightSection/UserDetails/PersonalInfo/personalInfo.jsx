import React, {Component} from 'react';
import styles from './personalInfo.scss'
import {connect} from "react-redux";
import * as actions from '../../../../../../store/personalInfo/actions/index';
import {Field, reduxForm} from 'redux-form';
import {defaultInterests} from '../../../../../../Utils/defaultInterests'
import {
    renderField,
    datepicker,
    renderSelect,
    renderTextArea,
} from "../../../../../FormHandler/formFieldRenderer.jsx";

import validate from '../../../../../FormHandler/validations/personalInfo/validate'

import moment from 'moment';
import {renderAsyncCreatableSelect} from "../../../../../FormHandler/formFieldRenderer";
import SavePreviewButtons from '../../../../../Common/SavePreviewButtons/savePreviewButtons';
import propTypes from 'prop-types';


export class PersonalInfo extends Component {
    constructor(props) {
        super(props);
        this.getImageURI = this.getImageURI.bind(this);
        this.removeImage = this.removeImage.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.updateInfoBeforeLoss = this.updateInfoBeforeLoss.bind(this);
        this.state = {
            'imageURI': '',
            'imageURL': '',
            flag: true,
            submit: false
        }
        this.staticUrl = (window && window.config && window.config.staticUrl) || '/media/static/'
        this.props.currentForm('profile');
    }
    
    // componentDidMount() {
    //     this.props.fetchPersonalInfo();
    // }
    
    async componentDidUpdate(prevProps) {
        const {ui: {previewClicked}, previewButtonClicked, history} = this.props;
        if (previewClicked !== prevProps.ui.previewClicked && previewClicked) {
            await this.updateInfoBeforeLoss()
            this.setState({submit: true})
            previewButtonClicked(false)
            history.push('/resume-builder/preview/')
        }
    }
    
    async updateInfoBeforeLoss() {
        let {initialValues, personalInfo, formData: {profile: {values, syncErrors}}} = this.props;
        let error = false;
        Object.keys(syncErrors || {}).map(key => (!!syncErrors[key] ? error = true : false));
        if (!error && !this.state.submit && JSON.stringify(initialValues) !== JSON.stringify(values)) await this.props.onSubmit(values, this.state.imageURL, this.state.flag, personalInfo)
    }
    
    async handleSubmit(values, entityLink) {
        const {personalInfo,history,onSubmit,generateResumeAlert} = this.props
        await onSubmit(values, this.state.imageURL, this.state.flag, personalInfo);
        this.setState({
            submit: true
        })
        if (entityLink) history.push(entityLink);
        else{
            generateResumeAlert()
        }
    }
    
    removeImage() {
        this.setState({
            imageURI: '',
            imageURL: '',
            flag: false
        });
    }
    
    
    componentWillUnmount() {
        this.updateInfoBeforeLoss()
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
            handleSubmit, userInfo: {order_data}, personalInfo, ui: {loader}, isEditable, fetchInterests,eventClicked,
            editHeading, currentAddress, saveTitle, entityName, nextEntity, history, handleInputValue, showAlertModal
        } = this.props;
        const newUser = localStorage.getItem('newUser')
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
                onChange={(event) => handleInputValue(event.target.value || entityName)}
                maxLength="20"/>
                <span onClick={(event) => saveTitle(event, 1)} className="icon-tick"/>
                </React.Fragment>
            }
            {newUser ?
                <span onClick={() => editHeading(elem)} onClick={showAlertModal}
                className={"icon-edit " + styles['icon-edit__cursor']}/> :
                <span onClick={() => editHeading(1)}
                className={!!(!isEditable) ? "icon-edit " + styles['icon-edit__cursor'] : ''}/>
            }
            
            </section>
            <form onSubmit={handleSubmit((values) => this.handleSubmit(values, nextEntity))}>
            <section id="personal-section" className="flex-container right-sidebar-scroll">
            <section className="info-section">
            <div className="flex-container">
            <fieldset>
            <label>First Name</label>
            {/*  Temporary disabled closed due to expert assitance */}
            <Field component={renderField} type={"text"} iconClass={'icon-name'}
            name="first_name" maxLength={"20"} disabled={order_data && order_data.id && false ? true: false}/>
            </fieldset>
            <fieldset>
            <label>Last Name</label>
            {/*  Temporary disabled closed due to expert assitance */}
            <Field component={renderField}
            iconClass={'icon-surname'} disabled={order_data && order_data.id && false ? true: false}
            type={"text"} name="last_name" maxLength={"20"}/>
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
            <Field yearDropDownItemNumber={60}
            iconClass={'icon-date'}
            component={datepicker} name="date_of_birth"
            maxDateAllowed={'true'}
            className={"input-control"}/>
            </fieldset>
            </div>
            <div className="flex-container">
            <fieldset>
            <label>Mobile</label>
            <Field component={renderField}
            type={"number"}
            name="number"
            maxLength={"10"}
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
            maxLength={'100'}
            showWordCounter={false}
            className={"input-control"} rows="3"/>
            <span className="word-counter mt-5">{currentAddress && currentAddress.length ?
                currentAddress.length : '0'}/100</span>
                </fieldset>
                </div>
                
                <div className="flex-container">
                <fieldset id="interest-select" className="">
                <label>Interest</label>
                <Field name="extracurricular" component={renderAsyncCreatableSelect}
                defaultOptions={defaultInterests}
                loadOptions={(inputValue) => fetchInterests(inputValue)}
                value={personalInfo.extracurricular}
                isMulti={true}
                closeMenuOnSelect={false}
                iconClass={'icon-interest'}
                maxItems={5}
                label="Select Interest"/>
                </fieldset>
                </div>
                
                </section>
                <section className="pic-section mt-30">
                {
                    (this.state.imageURI) || (personalInfo.image && this.state.flag) ?
                    <div className={styles['upper-cross']} onClick={this.removeImage.bind(this)}>
                    <i className='icon-close'></i>
                    </div> : ''
                }
                
                <label>
                
                {
                    (this.state.imageURI) || (personalInfo.image && this.state.flag) ?
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
                <SavePreviewButtons
                showAlertModal={showAlertModal} context={this} history={history} order_data={order_data} form_name={'Personal Info'} 
                nextEntity={nextEntity} updateInfoBeforeLoss={this.updateInfoBeforeLoss} eventClicked={eventClicked}
                />
                </form>
                </div>
                )
            }
        }
        
        PersonalInfo.propTypes = {
            currentForm: propTypes.func,
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
            previewButtonClicked: propTypes.func,
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
            initialValues: propTypes.object,
            formData: propTypes.object,
            personalInfo: propTypes.shape({
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
            }),
            onSubmit: propTypes.func,
            generateResumeAlert: propTypes.func,
            fetchImageUrl: propTypes.func,
            handleSubmit: propTypes.func,
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
            }),
            saveTitle: propTypes.func,
            editHeading: propTypes.func,
            isEditable: propTypes.bool,
            entityName: propTypes.string,
            handleInputValue: propTypes.func,
            showAlertModal: propTypes.func,
            changeOrderingDown: propTypes.func,
            changeOrderingUp: propTypes.func,
            showAlertMessage: propTypes.func,
            eventClicked: propTypes.func,
            fetchInterests: propTypes.func,
            currentAddress: propTypes.string,
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
                currentAddress: (state.form && state.form.profile && state.form.profile && state.form.profile.values
                    && state.form.profile.values.location) || ''
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
                    "onSubmit": (personalDetails, imageURL, flag, storeInfo) => {
                        const {gender, date_of_birth, extracurricular, image} = personalDetails;
                        const {entity_preference_data} = storeInfo;
                        personalDetails = {
                            ...personalDetails,
                            ...{
                                'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                                'gender': (gender && gender['value']) || '',
                                'image': imageURL || (flag ? image : ''),
                                'extracurricular': extracurricular instanceof Array ?
                                (extracurricular || []).filter(el => el !== undefined).map(el => el.value).join(',') : '',
                                'entity_preference_data': (entity_preference_data || []).map(el => el)
                            }
                        }
                        personalDetails = {
                            ...personalDetails,
                            ...{
                                'extracurricular': personalDetails.extracurricular instanceof Array && personalDetails.extracurricular.length ?
                                '' : personalDetails.extracurricular
                                
                            }
                        };
                        return new Promise((resolve, reject) => {
                            dispatch(actions.updatePersonalInfo({personalDetails, resolve, reject}));
                        })
                    },
                    "fetchImageUrl": (imageFile) => {
                        return new Promise((resolve, reject) => {
                            dispatch(actions.fetchImageUrl({imageFile, resolve, reject}));
                        })
                    },
                    "fetchInterests": (value) => {
                        if (value.length < 3) return new Promise(res => res([]));
                        return new Promise((res, rej) => {
                            return dispatch(actions.fetchInterestList({value, res, rej}))
                        })
                        
                    }
                }
            };
            
            export default connect(mapStateToProps, mapDispatchToProps)(PersonalInfoForm);
            