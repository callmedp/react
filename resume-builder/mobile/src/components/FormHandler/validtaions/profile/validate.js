const validate = values => {
    const errors = {};
    errors.first_name = !values || !values.first_name ? 'Required' : undefined;
    errors.last_name = !values || !values.last_name ? 'Required' : undefined;
    errors.date_of_birth = !values || !values.date_of_birth ? 'Required' : undefined;
    errors.gender = !values || !values.gender ? 'Required' : undefined;

    if (!values || !values.number) {
        errors.number = 'Required'
    }
    else if (values.number && !/^(0|[1-9][0-9]{9})$/i.test(values.number)) {
        errors.number = 'Invalid phone number, must be 10 digits'
    }
    if (!values || !values.email) {
        errors.email = 'Required'
    }
    if (values.email && !/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
        errors.email = 'Invalid email address'
    }
    errors.location = values && values.location && values.location.length > 100 ? 'Address limited to 100 characters' : undefined
    errors.extracurricular = values && values.extracurricular && values.extracurricular.length > 8 ? 'We recommend you not to add more interests.' : undefined
    return errors;
};


export default validate;