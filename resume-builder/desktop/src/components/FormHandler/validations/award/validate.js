const validate = values => {
    const errors = {};
    if (!values.list || !values.list.length) {
        errors.list = {_error: 'Atleast One Language should be entered.'}
        return errors;
    }
    else{
        const listErrors = []
        values.list.forEach((obj, objIndex) => {
            const objErrors = {}
            objErrors.title = !obj || !obj.title ? 'Required' : undefined;
            objErrors.date = !obj || !obj.date ? 'Required' : undefined;
            listErrors[objIndex] = objErrors
        });
        if (listErrors.length) {
            errors.list = listErrors;
            return errors;
        }
    }
    
};


export default validate;