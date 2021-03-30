import React, { Component } from "react";
import PropTypes from "prop-types";

class Autocomplete extends Component {
    static propTypes = {
        suggestions: PropTypes.instanceOf(Array),
        name: PropTypes.string,
        className: PropTypes.string,
        autoComplete: PropTypes.string,
        lableFor: PropTypes.string,
        type: PropTypes.string,
        placeholder: PropTypes.string
    };
    
    static defaultProps = {
        suggestions: [],
        name: 'input',
        className: 'form-control',
        autoComplete: "",
        labelFor: ""
    };

    constructor(props) {
        super(props);

        this.state = {
            filterSuggestion: [],
            showSuggestion: false,
            input: "",
            Activeclass: "form-group"
            
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
            input: e.currentTarget.value,
            Activeclass: "form-group checked"
        });
    };

    render() {
        const { name, className, autoComplete, lableFor, type, placeholder } = this.props;
        const {
            onChange,
            onClick,
            state: {
                filterSuggestion,
                showSuggestion,
                input,
                Activeclass
            }
        } = this;

        let suggestionList;

        if (showSuggestion && input) {
            if(filterSuggestion?.length) {
                suggestionList = (
                    <div className="m-user-intent-search-result">
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
                        {/* <i> No suggestions, type manually</i> */}
                    </div>
                );
            }
        }

        return (
            <div className={Activeclass}>
                <input
                type={type}
                id={name}
                name={name}
                placeholder={placeholder}
                autoComplete={autoComplete}
                className={className}
                aria-required="true"
                aria-invalid="true"
                onChange={onChange}
                value={input}
                />
                <label htmlFor=""> {lableFor} </label>

                { suggestionList }
            </div>
        );
    }
}

export default Autocomplete;