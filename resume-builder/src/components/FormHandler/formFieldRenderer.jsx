import React from 'react'
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import moment from 'moment';
// import AsyncSelect from 'react-select/lib/Async';
import Select from 'react-select';
import PropTypes from 'prop-types';


export const renderField = ({
                                input,
                                label,
                                type,
                                className,
                                meta: {touched, error, warning}
                            }) => (

    <input {...input} className={className} placeholder={label} type={type}/>
    // {touched &&
    // ((error && <span className={'Error-message'}>{error}</span>) ||
    //     (warning && <span className={'Warn-Message'}>{warning}</span>))}
);

export default class DatePickerField extends React.Component {
    constructor(props) {
        super(props);
        const input = props;
        this.handleChange = this.handleChange.bind(this)
        this.onBlur= this.onBlur.bind(this)
    }

    handleChange(date) {
        this.setState({
            startDate: date
        })
    }

    onBlur = (date) => {
        const {input} = this.props;
        input.onBlur(date, input);
    };

    render() {
        const {
            input,
            label,
            type,
            onDateChange,
            meta: {touched, error, warning}
        } = this.props;
        return (
            <DatePicker {...input} dateFormat="yyyy-MM-dd"
                        selected={ input.value ? new Date(input.value) : null}
                        onChange={date => input.onChange(date)}
                        onBlur={this.onBlur}
                        placeholderText={'Input Value'}

            />)

    }


}

export const renderSelect = ({
                                 input,
                                 label,
                                 meta: {touched, error, warning},
                                 options
                             }) => (
    <Select {...input}
            placeholder={label}
            options={options}
            onBlur={() => {
                input.onBlur(input.value)
            }}
    />
);

const adaptFileEventToValue = delegate => e => delegate(e.target.files[0]);

export const renderFileInput = ({
                                    input: {value: omitValue, onChange, onBlur, ...inputProps},
                                    meta: omitMeta,
                                    ...props
                                }) => {
    return (
        <input
            onChange={adaptFileEventToValue(onChange)}
            onBlur={adaptFileEventToValue(onBlur)}
            type="file"
            {...props.input}
            {...props}
        />
    );
};

//
// export const renderDynamicSelect = ({
//                                         input,
//                                         loadOptions,
//                                         label,
//                                         defaultOptions
//                                     }) => (
//     <AsyncSelect {...input}
//                  loadOptions={loadOptions}
//                  defaultOptions={defaultOptions}
//                  placeholder={label}
//                  isMulti={true}
//                  onBlur={() => {
//                      input.onBlur(input.value)
//                  }}
//     />
// )

export const renderTextArea = ({
                                   input,
                                   label,
                                   type,
                                   meta: {touched, error, warning}

                               }) => (

    <textarea {...input} placeholder={label} type={type}/>
    // {touched &&
    // ((error && <span className={'Error-message'}>{error}</span>) ||
    //     (warning && <span className={'Warn-Message'}>{warning}</span>))}


)

