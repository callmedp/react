const validate = values => {
    const errors = {};
    const listErrors = [];
    values = (values && values.list) || [];
    values.forEach((obj, objIndex) => {
        const objErrors = {}
        objErrors.title = !obj || !obj.title ? 'Required' : undefined;
        objErrors.date = !obj || !obj.date ? 'Required' : undefined;
        listErrors[objIndex] = objErrors
    });
    if (listErrors.length) {
        errors.list = listErrors;
        return errors;
    }
    return errors;

};


export default validate;