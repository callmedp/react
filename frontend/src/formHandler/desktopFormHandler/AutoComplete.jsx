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
            <div>
                
            </div>
        );
    }
}

export default Autocomplete;