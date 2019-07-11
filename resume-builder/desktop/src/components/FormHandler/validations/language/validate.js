const validate = values => {
    const errors = {};
    const listErrors = []
    values = (values && values.list) || [];
    values.forEach((obj, objIndex) => {
        const objErrors = {}
        objErrors.name = !obj || !obj.name ? 'Required' : undefined;
        objErrors.proficiency = !obj || !obj.proficiency ? 'Required' : undefined;
        listErrors[objIndex] = objErrors
    });
    if (listErrors.length) {
        errors.list = listErrors;
        return errors;
    }

    return errors;

};


export default validate;