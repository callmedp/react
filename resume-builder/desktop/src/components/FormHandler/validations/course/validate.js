const validate = values => {
    const errors = {};
    const listErrors = [];
    values = (values && values.list) || [];
    values.forEach((obj, objIndex) => {
        const objErrors = {}
        objErrors.name_of_certification = !obj || !obj.name_of_certification ? 'Required' : undefined;
        objErrors.year_of_certification = !obj || !obj.year_of_certification ? 'Required' : undefined;
        listErrors[objIndex] = objErrors
    });
    if (listErrors.length) {
        errors.list = listErrors;
        return errors;
    }
    return errors;

};


export default validate;