import React, {Component} from 'react';



export default class Summary extends Component {
    render() {
        return (
        <div className="buildResume">
            <div className="buildResume__wrap pb-0">
                <div className="buildResume__heading">
                    <h2>Summary</h2>
                    <i className="sprite icon--edit"></i>
                </div>

                <ul className="form">
                  
                    <li className="form__group">
                        <label className="form__label" for="summary">Summary</label>
                        <textarea  name="address" className="form__input h-300" aria-label="summary" id="summary" ></textarea>
                    </li>
                    

                    <li className="form__group">
                        <div className="btn-wrap">
                            <button className="btn btn__round btn--outline">Preview</button>
                            <button className="btn btn__round btn__primary">Save &amp; Continue</button>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
        )
    }
}