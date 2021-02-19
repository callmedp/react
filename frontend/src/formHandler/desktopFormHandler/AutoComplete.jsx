import React, { Component } from "react";
import PropTypes from "prop-types";

class Autocomplete extends Component {
    static propTypes = {
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
        const { suggestions } = this.props;
        const input = e.currentTarget.value;
        
        // Filter suggestion
        const filterSuggestion = suggestions.filter(
            suggestion => suggestion.toLowerCase().indexOf(input.toLowerCase()) > -1
        );

        this.setState({
            activeSuggestion: 0,
            filterSuggestion,
            showSuggestion: true,
            input: e.currentTarget.value
        });
    };

    render() {
        const {
            onChange,
            state: {
                activeSuggestion,
                filterSuggestion,
                showSuggestion,
                input
            }
        } = this;

        let suggestionList;

        if (showSuggestion && input) {
            if(filterSuggestion?.length) {
                suggestionList = (
                    <div className="user-intent-search-result">
                        {
                            filterSuggestion?.slice(0, 8)?.map((suggestion, index) => {
                                return(
                                    <span key={suggestion} onClick={onClick}>
                                        {suggestion}
                                    </span>
                                );
                            })
                        }
                    </div>
                )
            }
            else {
                suggestionList = (
                    <div>
                        <i> No suggestions, type manually</i>
                    </div>
                );
            }
        }

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
                value={input}
                />
            </div>
        );
    }
}

export default Autocomplete;