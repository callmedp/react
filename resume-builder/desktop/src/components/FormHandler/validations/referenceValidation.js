const validate = values => {
    const errors = {};
    if (!values.list || !values.list.length) {
        errors.list = {_error: 'Atleast One Language should be entered.'}
        return errors;
    }
    const listErrors = []
    values.list.forEach((obj, objIndex) => {
        const objErrors = {}
        objErrors.reference_name = !obj || !(obj.reference_name) ? 'Required' : null;
        objErrors.proficiency = !obj || !obj.proficiency ? 'Required' : null;
        objErrors.newError = 'Required';
        console.log('object value is ', obj, !obj, !obj.reference_name, objErrors);

        listErrors[objIndex] = objErrors
    });
    if (listErrors.length) {
        console.log('errors list', listErrors);
        errors.list = {_error: listErrors};
        console.log(errors);
        return errors;
    }
};


export default validate;