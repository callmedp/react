import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './faq.scss';

const FAQ = (props) => {
        return(
            <div className="m-container m-faq" id="m-faq">
                <h2 className="m-heading2">What is a resume format?</h2>
                <div className="tabs">
                    <div className="tab">
                        <input type="radio" id="rd0" name="rd"/><label className="tab-label" for="rd0" itemprop="name">Who will write my resume?</label>
                        <div id="0" className="tab-content">
                            <p itemprop="text" hidden="">1 A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
                        </div>
                    </div>
                    <div className="tab">
                        <input type="radio" id="rd1" name="rd"/><label className="tab-label" for="rd1" itemprop="name">How to choose a resume format?</label>
                        <div id="1" className="tab-content">
                            <p itemprop="text" hidden="">2 A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
                        </div>
                    </div>
                    <div className="tab">
                        <input type="radio" id="rd2" name="rd"/><label className="tab-label" for="rd2" itemprop="name">Why are resume formats important?</label>
                        <div id="2" className="tab-content">
                            <p itemprop="text" hidden="">3 A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
                        </div>
                    </div>
                    <div className="tab">
                        <input type="radio" id="rd3" name="rd"/><label className="tab-label" for="rd3" itemprop="name">What makes a resume good and attractive?</label>
                        <div id="3" className="tab-content">
                            <p itemprop="text" hidden="">4 A resume format is a sample resume that can be edited and filled with the required details. It is often provided with instructions or sample text and needs a rigorous edit to make it useful.</p>
                        </div>
                    </div>
                    <Link to={"#"} className="m-load-more mt-20">Load More FAQS</Link>
                </div>
            </div>
        )
    }

export default FAQ;