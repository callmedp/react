import React, {Component} from 'react';
import './preview.scss'
import queryString from "query-string";
import {entityList} from '../../../../../Utils/formCategoryList'
import {
    Accordion,
    AccordionItem,
    AccordionItemButton,
    AccordionItemHeading,
    AccordionItemPanel
} from "react-accessible-accordion";

export default class Preview extends Component {
    constructor(props) {
        super(props);
        this.goToBuyPage = this.goToBuyPage.bind(this);
        this.handleCustomization = this.handleCustomization.bind(this);
        this.selectCurrentTab = this.selectCurrentTab.bind(this);
        this.handleFontSize = this.handleFontSize.bind(this);
        this.handleActiveSection = this.handleActiveSection.bind(this);
        this.state = {
            currentTab: 1,
            selectedColor: 1,
            headingFontSize: 1,
            textFontSize: 1,
            activeSection: 'left'

        }
    }


    handleCustomization(data, color) {
        this.setState({
            selectedColor: color
        })
        this.props.customizeTemplate(data)
    }

    selectCurrentTab(tab) {
        this.setState({
            currentTab: Number(tab)
        })
    }


    goToBuyPage() {
        this.props.history.push('/resume-builder/buy')
    }


    static getDerivedStateFromProps(nextProp, prevState) {
        const {template: {color, heading_font_size, text_font_size}} = nextProp;
        let obj = prevState;
        if (color !== prevState['selectedColor']) {
            obj['selectedColor'] = color;
        }
        if (heading_font_size !== prevState['headingFontSize']) {
            obj['headingFontSize'] = heading_font_size;
        }
        if (text_font_size !== prevState['textFontSize']) {
            obj['textFontSize'] = text_font_size;
        }
        return obj;

    }

    handleFontSize() {
        let elem1 = this.refs.bar1;
        let slider1 = this.refs.slider1;
        let elem2 = this.refs.bar2;
        let slider2 = this.refs.slider2;

        if (!elem1 || !slider1 || !elem2 || !slider2)
            return;
        let rightEdge1 = slider1.offsetWidth - elem1.offsetWidth;
        let rightEdge2 = slider2.offsetWidth - elem2.offsetWidth;

        console.log('----', rightEdge1, rightEdge2, elem1, elem2, slider1, slider2);
        switch (this.state.headingFontSize) {
            case 1: {
                elem1.style.left = 0 + 'px';
                break;
            }
            case 2: {
                elem1.style.left = rightEdge1 / 2 + 'px';
                break;
            }
            case 3: {
                elem1.style.left = rightEdge1 + 'px';
                break;
            }
        }

        switch (this.state.textFontSize) {
            case 1: {
                elem2.style.left = 0 + 'px';
                break;
            }
            case 2: {
                elem2.style.left = rightEdge2 / 2 + 'px';
                break;
            }
            case 3: {
                elem2.style.left = rightEdge2 + 'px';
                break;
            }
        }

    }

    componentDidMount() {

        this.props.fetchDefaultCustomization(localStorage.getItem('selected_template'));

        let elem1 = this.refs.bar1;
        let slider1 = this.refs.slider1;
        let elem2 = this.refs.bar2;
        let slider2 = this.refs.slider2;

        const self = this;

        function handleElemEvent(event, element, sliderElement, section) {

            let shiftX = event.clientX - element.getBoundingClientRect().left;
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);

            let leftEdge = 0, rEdge = 0;

            function onMouseMove(event) {

                let newLeft = event.clientX - shiftX - sliderElement.getBoundingClientRect().left;

                // the pointer is out of slider => lock the thumb within the bounaries
                if (newLeft < 0) {
                    newLeft = 0;
                }


                let rightEdge = sliderElement.offsetWidth - element.offsetWidth;

                if (newLeft > rightEdge) {
                    newLeft = rightEdge;
                }

                leftEdge = newLeft;
                rEdge = rightEdge;


                element.style.left = newLeft + 'px';
            }


            function onMouseUp() {
                const {userInfo: {selected_template}} = self.props;

                let size = 1;
                if (leftEdge > ((rEdge / 2) + 50)) {
                    element.style.left = rEdge + 'px';
                    size = 3;

                } else if (leftEdge < ((rEdge / 2)) - 50) {
                    element.style.left = 0 + 'px';
                    size = 1;
                } else {
                    element.style.left = rEdge / 2 + 'px';
                    size = 2;
                }

                if (section === 'text') {
                    self.props.customizeTemplate({
                        'text_font_size': size,
                        'template': selected_template
                    })
                } else {
                    self.props.customizeTemplate({
                        'heading_font_size': size,
                        'template': selected_template
                    })
                }

                document.removeEventListener('mouseup', onMouseUp);
                document.removeEventListener('mousemove', onMouseMove);
            }

        }

        elem1.onmousedown = function (event) {
            event.preventDefault(); // prevent selection start (browser action)

            handleElemEvent(event, elem1, slider1, 'heading');
        };

        elem2.onmousedown = function (event) {
            event.preventDefault(); // prevent selection start (browser action)

            handleElemEvent(event, elem2, slider2, 'text');
        };


        elem1.ondragstart = function () {
            return false;
        };


        elem2.ondragstart = function () {
            return false;
        };
    }


    handleActiveSection(section) {
        this.setState({
            activeSection: section
        })
    }

    render() {

        const {userInfo: {selected_template}, template: {heading_font_size, text_font_size, entity_position}} = this.props;
        const {currentTab, selectedColor, headingFontSize, textFontSize, activeSection} = this.state;
        const entity_elements = entity_position && eval(entity_position) || [];
        console.log('---', entity_elements);

        // this.handleFontSize(headingFontSize, textFontSize)

        return (
            <div className="preview-section">
                <strong>Complete your customisation</strong>
                <Accordion>
                    <div className="preivew-scroll">
                        <AccordionItem>
                            <div className="change-theme">
                                <AccordionItemHeading>
                                    <AccordionItemButton>
                                        <div
                                            onClick={() => this.selectCurrentTab(1)}
                                            className={"change-theme--theme-heading " + (currentTab === 1 ? 'change-theme--active' : '')}>
                                            <span className="icon-change-theme mr-20"></span>
                                            Change theme
                                        </div>
                                    </AccordionItemButton>
                                </AccordionItemHeading>
                                <AccordionItemPanel>
                                    <ul className="change-theme-content">
                                        <li>
                                            <input
                                                onClick={() => this.handleCustomization({
                                                    color: 1,
                                                    template: selected_template
                                                }, 1)}
                                                readOnly
                                                type="radio"
                                                name="radio1" id="green" value="green"
                                                checked={selectedColor === 1}/>
                                            <label htmlFor="green"><span className="theme-green"></span></label>
                                        </li>
                                        <li>
                                            <input
                                                onClick={() => this.handleCustomization({
                                                    color: 2, template: selected_template
                                                }, 2)}
                                                type="radio"
                                                name="radio1"
                                                readOnly
                                                id="blue"
                                                value="blue"
                                                checked={selectedColor === 2}
                                            />
                                            <label htmlFor="blue"><span className="theme-blue"></span></label>
                                        </li>
                                        <li>
                                            <input
                                                onClick={() => this.handleCustomization({
                                                    color: 3,
                                                    template: selected_template
                                                }, 3)}
                                                type="radio"
                                                name="radio1"
                                                readOnly
                                                id="red"
                                                value="red"
                                                checked={selectedColor === 3}
                                            />
                                            <label htmlFor="red"><span className="theme-red"></span></label>
                                        </li>
                                        <li>
                                            <input
                                                onClick={() => this.handleCustomization({
                                                    color: 4,
                                                    template: selected_template
                                                }, 4)}
                                                type="radio"
                                                readOnly
                                                name="radio1" id="black" value="black"
                                                checked={selectedColor === 4}/>
                                            <label htmlFor="black"><span className="theme-black"></span></label>
                                        </li>
                                        <li>
                                            <input
                                                onClick={() => this.handleCustomization({
                                                    color: 5,
                                                    template: selected_template
                                                }, 5)}
                                                type="radio"
                                                name="radio1"
                                                readOnly
                                                id="brown" value="brown"
                                                checked={selectedColor === 5}
                                            />
                                            <label htmlFor="brown"><span className="theme-brown"></span></label>
                                        </li>
                                        <li>
                                            <input
                                                onClick={() => this.handleCustomization({
                                                    color: 6,
                                                    template: selected_template
                                                }, 6)}
                                                type="radio"
                                                readOnly
                                                name="radio1" id="violet" value="violet"
                                                checked={selectedColor === 6}/>
                                            <label htmlFor="violet"><span className="theme-violet"></span></label>
                                        </li>
                                    </ul>
                                </AccordionItemPanel>
                            </div>
                        </AccordionItem>
                        <AccordionItem>
                            <div className="change-theme">
                                <AccordionItemHeading>
                                    <AccordionItemButton>
                                        <div onClick={() => this.selectCurrentTab(2)}
                                             className={"change-theme--theme-heading " + (currentTab === 2 ? 'change-theme--active' : '')}>
                                            <span className="icon-change-font mr-20"></span>
                                            Font size
                                        </div>
                                    </AccordionItemButton>
                                </AccordionItemHeading>
                                <AccordionItemPanel>
                                    <ul className="change-font-content">
                                        <li>
                                            <strong>Section Heading</strong>
                                            <div ref="slider1" className="change-font-content--font-box">
                                                <div role="progressbar" aria-valuenow="40" aria-valuemin="0"
                                                     aria-valuemax="100"
                                                     className="change-font-content--font-bar">
                                                    <span ref="bar1" className="change-font-content--font-bar__bar"/>
                                                </div>
                                            </div>
                                            <div className="change-font-content--text-align">
                                                <span>S</span>
                                                <span>M</span>
                                                <span>L</span>
                                            </div>
                                        </li>
                                        <li>
                                            <strong>Section Text</strong>
                                            <div ref="slider2" className="change-font-content--font-box">
                                                <div role="progressbar" aria-valuenow="40" aria-valuemin="0"
                                                     aria-valuemax="100"

                                                     className="change-font-content--font-bar">
                                                    <span ref="bar2"
                                                          className="change-font-content--font-bar__bar"></span>
                                                </div>
                                                <div className="change-font-content--text-align">
                                                    <span>S</span>
                                                    <span>M</span>
                                                    <span>L</span>
                                                </div>
                                            </div>
                                        </li>
                                    </ul>
                                </AccordionItemPanel>
                            </div>

                        </AccordionItem>
                        <AccordionItem>
                            <div className="change-theme">
                                <AccordionItemHeading>
                                    <AccordionItemButton>
                                        <div
                                            onClick={() => this.selectCurrentTab(3)}
                                            className={"change-theme--theme-heading " + (currentTab === 3 ? 'change-theme--active' : '')}>
                                            <span className="icon-change-reorder mr-20"></span>
                                            Reorder section
                                        </div>
                                    </AccordionItemButton>
                                </AccordionItemHeading>
                                <AccordionItemPanel>
                                    <ul class="reorder-tab-heading">
                                        <li
                                            onClick={() => this.handleActiveSection('left')}
                                            className={"tab-heading--top-left-right-radius no-shadow " + (activeSection === 'left' ? 'active shadow2' : '')}>
                                            <span>Left</span>
                                        </li>
                                        <li
                                            onClick={() => this.handleActiveSection('right')}
                                            className={"tab-heading--top-left-right-radius no-shadow " + (activeSection === 'right' ? 'active shadow2' : ' ')}>
                                            <span>Right</span></li>
                                    </ul>
                                    <ul className="reorder-content">
                                        <li className="reorder-content--select-box reorder-content--select-box__select">
                                            Personal Info
                                            <span className="addon-buttons">
	                				<span className="icon-ascend1 mr-5 ml-0"></span>
	                				<span className="icon-descend1 ml-0"></span>
	                			</span>
                                        </li>
                                        {
                                            (entity_elements || []).filter(els => els['alignment'] === activeSection).map(el => {

                                                const entityValue = entityList.find(elm => elm.entity_id == el.entity_id);
                                                return (
                                                    <li className="reorder-content--select-box">{entityValue['entity_text']}</li>
                                                )


                                            })
                                        }
                                    </ul>
                                </AccordionItemPanel>
                            </div>
                        </AccordionItem>
                    </div>
                </Accordion>
                < button
                    className="orange-button preview-section__orange-button mt-40"
                    onClick={this.goToBuyPage}> Get your resume
                </button>
            </div>
        )
    }
}

