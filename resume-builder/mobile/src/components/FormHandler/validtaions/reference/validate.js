const validate = values => {
    const errors = {};
    if (!values.list || !values.list.length) {
        errors.list = {_error: 'Atleast One Education should be entered.'}
        return errors;
    }
    else{
        const listErrors = []
        values.list.forEach((obj, objIndex) => {
            const objErrors = {}
            objErrors.reference_name = !obj || !obj.reference_name ? 'Required' : undefined;
            objErrors.reference_designation = !obj || !obj.reference_designation ? 'Required' : undefined;
            listErrors[objIndex] = objErrors
        });
        if (listErrors.length) {
            errors.list = listErrors;
            console.log(errors)
            return errors;
        }
    }
    
};


export default validate;