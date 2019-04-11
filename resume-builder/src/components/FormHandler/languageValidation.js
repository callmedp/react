const languageValidation = values => {
    const errors = {};
    if (!values.list || !values.list.length) {
        errors.list = {_error: 'Atleast One Language should be entered.'}
        return errors;
    }
    const listErrors = []
    values.list.forEach((obj, objIndex) => {
        const objErrors = {}
        if (!obj || obj.name) {
            objErrors.name = 'Required';
            listErrors[objIndex] = objErrors
        }
        if (!obj || obj.proficiency) {
            objErrors.proficiency = 'Required';
            listErrors[objIndex] = objErrors
        }
    });
    if (listErrors.length) {
        errors.list = listErrors
    }
    return errors;
};

export default languageValidation;