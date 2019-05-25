import React ,{Component} from 'react';
import Header from '../../../Common/Header/header.jsx';
import './preview.scss';
import {connect} from "react-redux";
import {fetchTemplate,updateModalStatus,customizeTemplate,fetchDefaultCustomization} from "../../../../store/template/actions/index"
import {updatePersonalInfo,fetchPersonalInfo} from "../../../../store/personalInfo/actions/index"
import Loader from '../../../Common/Loader/loader.jsx';
import ChangeTemplateModal from './changeTemplateModal.jsx';
import moment from 'moment'
import {
    Accordion,
    AccordionItem,
    AccordionItemButton,
    AccordionItemHeading,
    AccordionItemPanel
} from "react-accessible-accordion";

class Preview extends Component {

    constructor(props){
        super(props)
        this.state={
            'customize' : false,
            currentTab: 1,
            selectedColor: 1,
            headingFontSize: 1,
            textFontSize: 1
        }
        this.handleCustomization = this.handleCustomization.bind(this);
    }

    componentWillUpdate(prevProps){
        const {initialValues} = this.props
        if(initialValues !== prevProps.initialValues){

            this.setState({
                selectedColor:initialValues.color,
                headingFontSize:initialValues.heading_font_size,
                textFontSize:initialValues.text_font_size
            })
        }
    }

    async componentDidMount(){
        await this.props.fetchPersonalInfo();
        this.props.fetchTemplate();
        this.props.fetchDefaultCustomization();
    }

    async handleCustomization(data) {
        await this.props.customizeTemplate(data)
        this.props.fetchTemplate();
        this.setState({customize:false})
    }

    render(){
        const {customize,currentTab,selectedColor} = this.state
        const {initialValues:{html},loader:{mainloader},personalInfo:{selected_template}} = this.props
        return(
            <div className="preview">
               <Header page={'preview'} {...this.props}/>
               <ChangeTemplateModal {...this.props}/>
               {mainloader ? <Loader/> :""}

               {/* <div className="preview__resume"
                 dangerouslySetInnerHTML={{
                     __html: html
                 }}/> */}

                <iframe srcDoc={html} className={"iframe-new"}></iframe>

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
                                    <Accordion preExpanded={["1"]}>
                                        <AccordionItem uuid="1">
                                            <div className={"filter__accordion__card " +(currentTab === 1 ? "filter__accordion--active":"")}>
                                            <AccordionItemHeading>
                                                <AccordionItemButton>
                                                    <div className="filter__accordion__card__heading" onClick={()=>{this.setState({currentTab:1})}}>
                                                        <div className="filter__accordion__card__heading--left">
                                                            <i className="sprite icon--theme mr-10"></i>
                                                            <span>Change theme</span>
                                                        </div>

                                                        <div className="filter__accordion__card__heading--right">
                                                            <i className={"sprite "  +(currentTab === 1 ? "icon--minus":"icon--plus")}></i>
                                                        </div>
                                                    </div>
                                                </AccordionItemButton>
                                            </AccordionItemHeading>
                                            <AccordionItemPanel>
                                                <div className="filter__accordion__card--content">  
                                                    <ul className="resume-color-theme">
                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="green" value="green"
                                                                onClick={()=>{this.setState({selectedColor:1})}}
                                                                checked={selectedColor === 1} />
                                                            <label htmlFor="green" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--green"></span>
                                                            </label>
                                                        </li>

                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="blue" value="blue"
                                                                onClick={()=>{this.setState({selectedColor:2})}} 
                                                                checked={selectedColor === 2}/>
                                                            <label htmlFor="blue" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--blue"></span>
                                                            </label>
                                                        </li>
                                                        
                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="red" value="red"
                                                                onClick={()=>{this.setState({selectedColor:3})}}
                                                                checked={selectedColor === 3}/>
                                                            <label htmlFor="red" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--red"></span>
                                                            </label>
                                                        </li>
                                                        
                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="black" value="black" 
                                                                onClick={()=>{this.setState({selectedColor:4})}}
                                                                checked={selectedColor === 4}/>
                                                            <label htmlFor="black" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--black"></span>
                                                            </label>
                                                        </li>
                                                        
                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="brown" value="brown"
                                                                onClick={()=>{this.setState({selectedColor:5})}} 
                                                                checked={selectedColor === 5}/>
                                                            <label htmlFor="brown" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--brown"></span>
                                                            </label>
                                                        </li>
                                                        
                                                        <li className="resume-color-theme__item">
                                                            <input className="resume-color-theme__item--input" type="radio" name="radio1" id="violet" value="violet" 
                                                                onClick={()=>{this.setState({selectedColor:6})}} 
                                                                checked={selectedColor === 6}/>
                                                            <label htmlFor="violet" className="resume-color-theme__item__label">
                                                                <span className="resume-color-theme__item__theme resume-color-theme__item--violet"></span>
                                                            </label>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </AccordionItemPanel>
                                            </div>
                                        </AccordionItem>
                                        <AccordionItem>
                                            <div className={"filter__accordion__card " +(currentTab === 2 ? "filter__accordion--active":"")}>
                                            <AccordionItemHeading>
                                                <AccordionItemButton>
                                                <div className="filter__accordion__card__heading" onClick={()=>{this.setState({currentTab:2})}}>
                                                    <div className="filter__accordion__card__heading--left">
                                                        <i className="sprite icon--font mr-10"></i>
                                                        <span>Font size</span>
                                                    </div>

                                                    <div className="filter__accordion__card__heading--right">
                                                        <i className={"sprite "  +(currentTab === 2 ? "icon--minus":"icon--plus")}></i>
                                                    </div>
                                                </div>
                                                </AccordionItemButton>
                                            </AccordionItemHeading>
                                            <AccordionItemPanel>
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
                                            </AccordionItemPanel>
                                        </div>
                                        </AccordionItem>
                                        <AccordionItem>
                                            <div className={"filter__accordion__card " +(currentTab === 3 ? "filter__accordion--active":"")}>
                                            <AccordionItemHeading>
                                                <AccordionItemButton>
                                                <div className="filter__accordion__card__heading" onClick={()=>{this.setState({currentTab:3})}}>
                                                    <div className="filter__accordion__card__heading--left">
                                                        <i className="sprite icon--reorder mr-10"></i>
                                                        <span>Reorder section</span>
                                                    </div>

                                                    <div className="filter__accordion__card__heading--right">
                                                        <i className={"sprite "  +(currentTab === 3 ? "icon--minus":"icon--plus")}></i>
                                                    </div>
                                                </div>
                                                </AccordionItemButton>
                                            </AccordionItemHeading>
                                            <AccordionItemPanel>
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
                                            </AccordionItemPanel>
                                            </div>
                                        </AccordionItem>
                                    </Accordion>
                                </div>

                                <div className="filter__apply-btn">
                                    <span className="btn" onClick={()=>{this.setState({customize:false})}}>Cancel</span>
                                    <span className="btn btn__round btn--outline" 
                                    onClick={() => this.handleCustomization({
                                                                    color: selectedColor,
                                                                    template: selected_template
                                                                })} >Apply</span>
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
        personalInfo: state.personalInfo,
        allinfo:state
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
        "customizeTemplate": (template_data) => {
            return new Promise((resolve, reject) => {
                return dispatch(customizeTemplate({template_data,resolve,reject}))
            })
        },
        "fetchDefaultCustomization": () => {
            return dispatch(fetchDefaultCustomization(1))
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