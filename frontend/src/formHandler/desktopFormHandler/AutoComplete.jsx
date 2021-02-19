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
            filterSuggestion: [],
            showSuggestion: false,
            input: ""
        };
    }

    onClick = e => {
        this.setState({
            filterSuggestion: [],
            showSuggestion: false,
            input: e.currentTarget.innerText
        })
    }
   
    onChange = e => {
        const { suggestions } = this.props;
        const input = e.currentTarget.value;
        
        // Filter suggestion
        const filterSuggestion = suggestions.filter(
            suggestion => suggestion.toLowerCase().indexOf(input.toLowerCase()) > -1
        );

        this.setState({
            filterSuggestion,
            showSuggestion: true,
            input: e.currentTarget.value
        });
    };

    render() {
        const {
            onChange,
            onClick,
            state: {
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
                <label htmlFor=""> Preferred Location </label>

                { suggestionList }
            </div>
        );
    }
}

export default Autocomplete;