import React ,{Component} from 'react';
import Header from '../../../Common/Header/header.jsx';
import './preview.scss';
import {connect} from "react-redux";
import {fetchTemplate,updateModalStatus} from "../../../../store/template/actions/index"
import {updatePersonalInfo,fetchPersonalInfo} from "../../../../store/personalInfo/actions/index"
import Loader from '../../../Common/Loader/loader.jsx';
import ChangeTemplateModal from './changeTemplateModal.jsx';
import moment from 'moment'

class Preview extends Component {

    constructor(props){
        super(props)
        this.state={
            'customize' : false
        }
    }

    componentDidMount(){
        this.props.fetchTemplate();
        this.props.fetchPersonalInfo();
    }
    render(){
        const {customize} = this.state
        const {initialValues:{html},loader:{mainloader}} = this.props
        return(
            <div className="preview">
               <Header page={'preview'} {...this.props}/>
               <ChangeTemplateModal {...this.props}/>
               {mainloader ? <Loader/> :""}

               <div className="preview__resume"
                 dangerouslySetInnerHTML={{
                     __html: html
                 }}/>

               <div className="preview__bottom-btns">
                    <span className="btn btn__round btn--outline" onClick={()=>{this.setState({customize:true})}}>Customize template</span>
                    <span className="btn btn__round btn__primary">Get your resume</span>
               </div>

               {customize ?
                    <div className="filter">
                            <div className="filter__overlay"></div>
                            <div className="filter__wrap">
                                
                                <div className="filter__accordion">
                                    <h2 className="filter__wrap--heading">Customize template</h2>

                                    <div className="filter__accordion__card filter__accordion--active">
                                        <div className="filter__accordion__card__heading">
                                            <div className="filter__accordion__card__heading--left">
                                                <i className="sprite icon--theme mr-10"></i>
                                                <span>Change theme</span>
                                            </div>

                                            <div className="filter__accordion__card__heading--right">
                                                <i className="sprite icon--plus icon--minus"></i>
                                            </div>
                                        </div>

                                        <div className="filter__accordion__card--content">  
                                            <ul className="resume-color-theme">
                                                <li className="resume-color-theme__item">
                                                    <input className="resume-color-theme__item--input" type="radio" name="radio1" id="green" value="green" />
                                                    <label htmlFor="green" className="resume-color-theme__item__label">
                                                        <span className="resume-color-theme__item__theme resume-color-theme__item--green"></span>
                                                    </label>
                                                </li>

                                                <li className="resume-color-theme__item">
                                                    <input className="resume-color-theme__item--input" type="radio" name="radio1" id="blue" value="blue" />
                                                    <label htmlFor="blue" className="resume-color-theme__item__label">
                                                        <span className="resume-color-theme__item__theme resume-color-theme__item--blue"></span>
                                                    </label>
                                                </li>
                                                
                                                <li className="resume-color-theme__item">
                                                    <input className="resume-color-theme__item--input" type="radio" name="radio1" id="red" value="red"/>
                                                    <label htmlFor="red" className="resume-color-theme__item__label">
                                                        <span className="resume-color-theme__item__theme resume-color-theme__item--red"></span>
                                                    </label>
                                                </li>
                                                
                                                <li className="resume-color-theme__item">
                                                    <input className="resume-color-theme__item--input" type="radio" name="radio1" id="black" value="black" />
                                                    <label htmlFor="black" className="resume-color-theme__item__label">
                                                        <span className="resume-color-theme__item__theme resume-color-theme__item--black"></span>
                                                    </label>
                                                </li>
                                                
                                                <li className="resume-color-theme__item">
                                                    <input className="resume-color-theme__item--input" type="radio" name="radio1" id="brown" value="brown"/>
                                                    <label htmlFor="brown" className="resume-color-theme__item__label">
                                                        <span className="resume-color-theme__item__theme resume-color-theme__item--brown"></span>
                                                    </label>
                                                </li>
                                                
                                                <li className="resume-color-theme__item">
                                                    <input className="resume-color-theme__item--input" type="radio" name="radio1" id="violet" value="violet" />
                                                    <label htmlFor="violet" className="resume-color-theme__item__label">
                                                        <span className="resume-color-theme__item__theme resume-color-theme__item--violet"></span>
                                                    </label>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                    
                                    <div className="filter__accordion__card">
                                        <div className="filter__accordion__card__heading">
                                            <div className="filter__accordion__card__heading--left">
                                                <i className="sprite icon--font mr-10"></i>
                                                <span>Font size</span>
                                            </div>

                                            <div className="filter__accordion__card__heading--right">
                                                <i className="sprite icon--plus"></i>
                                            </div>
                                        </div>

                                        <div className="filter__accordion__card--content">
                                            <div className="font-filter">
                                                <h3>Section Heading</h3>
                                                <div className="font-filter__slide-bar">
                                                    <span className="font-filter__dot"></span>
                                                    <span className="font-filter--small mt-10 fs-12">S</span>
                                                    <span className="font-filter--medium mt-10 fs-12">M</span>
                                                    <span className="font-filter--large mt-10 fs-12">L</span>
                                                </div>

                                            </div>
                                        </div>
                                    </div>

                                    <div className="filter__accordion__card mt-20">
                                        <div className="filter__accordion__card__heading">
                                            <div className="filter__accordion__card__heading--left">
                                                <i className="sprite icon--reorder mr-10"></i>
                                                <span>Reorder section</span>
                                            </div>

                                            <div className="filter__accordion__card__heading--right">
                                                <i className="sprite icon--plus"></i>
                                            </div>
                                        </div>

                                        <div className="filter__accordion__card--content">
                                            <div className="reorder">
                                                <ul className="reorder__items">
                                                    <li className="reorder__item reorder--select">
                                                        <span className="reorder__title">Personal Info</span>
                                                        <div className="reorder__nav">
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--upArrow"></i>
                                                            </span>
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--downArrow"></i>
                                                            </span>
                                                        </div>
                                                    </li>
                                                    
                                                    <li className="reorder__item">
                                                        <span className="reorder__title">Summary</span>
                                                        <div className="reorder__nav">
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--upArrow"></i>
                                                            </span>
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--downArrow"></i>
                                                            </span>
                                                        </div>
                                                    </li>
                                                    
                                                    <li className="reorder__item">
                                                        <span className="reorder__title">Experience</span>
                                                        <div className="reorder__nav">
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--upArrow"></i>
                                                            </span>
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--downArrow"></i>
                                                            </span>
                                                        </div>
                                                    </li>
                                                    
                                                    <li className="reorder__item">
                                                        <span className="reorder__title">Education</span>
                                                        <div className="reorder__nav">
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--upArrow"></i>
                                                            </span>
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--downArrow"></i>
                                                            </span>
                                                        </div>
                                                    </li>
                                                    
                                                    <li className="reorder__item">
                                                        <span className="reorder__title">Skills</span>
                                                        <div className="reorder__nav">
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--upArrow"></i>
                                                            </span>
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--downArrow"></i>
                                                            </span>
                                                        </div>
                                                    </li>
                                                    
                                                    <li className="reorder__item">
                                                        <span className="reorder__title">Language</span>
                                                        <div className="reorder__nav">
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--upArrow"></i>
                                                            </span>
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--downArrow"></i>
                                                            </span>
                                                        </div>
                                                    </li>
                                                    
                                                    <li className="reorder__item">
                                                        <span className="reorder__title">Awards</span>
                                                        <div className="reorder__nav">
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--upArrow"></i>
                                                            </span>
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--downArrow"></i>
                                                            </span>
                                                        </div>
                                                    </li>
                                                    
                                                    <li className="reorder__item">
                                                        <span className="reorder__title">Courses</span>
                                                        <div className="reorder__nav">
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--upArrow"></i>
                                                            </span>
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--downArrow"></i>
                                                            </span>
                                                        </div>
                                                    </li>
                                                    
                                                    <li className="reorder__item">
                                                        <span className="reorder__title">Projects</span>
                                                        <div className="reorder__nav">
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--upArrow"></i>
                                                            </span>
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--downArrow"></i>
                                                            </span>
                                                        </div>
                                                    </li>
                                                    
                                                    <li className="reorder__item">
                                                        <span className="reorder__title">References</span>
                                                        <div className="reorder__nav">
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--upArrow"></i>
                                                            </span>
                                                            <span className="reorder__nav--item">
                                                                <i className="sprite icon--downArrow"></i>
                                                            </span>
                                                        </div>
                                                    </li>
                                                </ul>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="filter__apply-btn">
                                    <span className="btn" onClick={()=>{this.setState({customize:false})}}>Cancel</span>
                                    <span className="btn btn__round btn--outline">Apply</span>
                                </div>
                            </div>
                        </div>
                    :''
                }        
            </div>

            
        )
    }

}

const mapStateToProps = (state) => {
    return {
        initialValues: state.template,
        loader: state.loader,
        personalInfo: state.personalInfo
    }
};

const mapDispatchToProps = (dispatch) => {
    return {
        "fetchTemplate": () => {
            return dispatch(fetchTemplate())
        },
        "updateModalStatus": (data) => {
            return dispatch(updateModalStatus(data))
        },
        "fetchPersonalInfo": (data) => {
            return dispatch(fetchPersonalInfo(data))
        },
        "updateSelectedTemplate": (personalInfo) => {
            let { date_of_birth, extracurricular} = personalInfo;
            let interest = extracurricular
            interest =  ((interest|| []).map((item)=>item.value)).join(",")
            let personalDetails = {
                ...personalInfo,
                ...{
                    'date_of_birth': (date_of_birth && moment(date_of_birth).format('YYYY-MM-DD')) || '',
                    'extracurricular': interest,
                }
            }
            return new Promise((resolve, reject) => {
                dispatch(updatePersonalInfo({personalDetails, resolve, reject}));
            })
        },
    }
};

export default connect(mapStateToProps, mapDispatchToProps)(Preview);