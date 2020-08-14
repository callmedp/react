const validate = values => {
    const errors = {};
    errors.extra_info = !values || !values.extra_info ? 'Required' : undefined;
    return errors
    
};


export default validate;