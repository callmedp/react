import React from 'react'


export const renderField = ({
                                input,
                                label,
                                type,
                                className,
                                meta: {touched, error, warning}
                            }) => (

        <input {...input} className={className}  placeholder={label} type={type}/>
        // {touched &&
        // ((error && <span className={'Error-message'}>{error}</span>) ||
        //     (warning && <span className={'Warn-Message'}>{warning}</span>))}
)

/*

export const datePicker = ({
                               input,
                               label,
                               type,
                               onDateChange,
                               meta: {touched, error, warning}
                           }) => (
    <div>
        <div className={'Top-space'}>
            <DatePicker {...input} dateFormat="yyyy-MM-dd" placeholderText={label} className="Field-spacing"
                        selected={input.value ? moment(input.value).format("YYYY-MM-DD") : null}
                        onChange={date => input.onChange(moment(date).format("YYYY-MM-DD"))}
            />
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    </div>
)

export const renderSelect = ({
                                 input,
                                 label,
                                 meta: {touched, error, warning},
                                 options
                             }) => (
    <div>
        <div className={'Top-space'}>
            <Select {...input}
                    placeholder={label}
                    options={options}
                    onBlur={() => {
                        input.onBlur(input.value)
                    }}
            />
            {touched &&
            ((error && <span className={'Error-message'}>{error}</span>) ||
                (warning && <span className={'Warn-Message'}>{warning}</span>))}
        </div>
    </div>
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

export const renderDynamicSelect = ({
                                        input,
                                        loadOptions,
                                        label,
                                        defaultOptions
                                    }) => (
    <AsyncSelect {...input}
                 loadOptions={loadOptions}
                 defaultOptions={defaultOptions}
                 placeholder={label}
                 isMulti={true}
                 onBlur={() => {
                     input.onBlur(input.value)
                 }}
    />
)
*/

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

