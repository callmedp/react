const validate = values => {
    const errors = {};
    const listErrors = [];
    values = (values && values.list) || [];
    values.forEach((obj, objIndex) => {
        const objErrors = {};
        objErrors.reference_name = !obj || !obj.reference_name ? 'Required' : undefined;
        objErrors.reference_designation = !obj || !obj.reference_designation ? 'Required' : undefined;
        listErrors[objIndex] = objErrors
    });
    if (listErrors.length) {
        errors.list = listErrors;
        console.log("2 is ", errors);
        return errors;
    }
    return errors;
};


export default validate;