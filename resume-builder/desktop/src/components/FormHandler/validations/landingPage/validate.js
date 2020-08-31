const validate = values => {
    const errors = {};
    errors.name = !values || !values.name ? 'Required' : undefined;
    if (!values || !values.number) {
        errors.number = 'Required'
    } else if (values.number && !/^(0|[1-9][0-9]{9})$/i.test(values.number)) {
        errors.number = 'Invalid phone number, must be 10 digits'
    }
    if (values.email && !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
        errors.email = 'Invalid email address'
    }
    return errors

};


export default validate;