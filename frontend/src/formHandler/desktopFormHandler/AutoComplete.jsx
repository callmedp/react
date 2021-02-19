import React, { Component } from "react";
import PropTypes from "prop-types";

class Autocomplete extends Component {
    static PropTypes = {
        suggestions: PropTypes.instanceOf(Array)
    };
    
    static defaultProps = {
        suggestions: []
    };

    constructor(props) {
        super(props);

        this.state = {
            activeSuggestion: 0,
            filterSuggestion: [],
            showSuggestion: false,
            input: ""
        };
    }
   
    onChange = e => {
        
    }

    render() {

        return (
            <div className="form-group">
                <input
                type="text"
                id="location"
                name="location"
                placeholder=" "
                autoComplete="off"
                className="form-control"
                aria-required="true"
                aria-invalid="true"
                onChange={onChange}
                value={userInput}
                />
            </div>
        );
    }
}

export default Autocomplete;