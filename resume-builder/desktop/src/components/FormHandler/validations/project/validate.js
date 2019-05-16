const validate = values => {
    const errors = {};

    const listErrors = []
    values = values && values.list || [];
    values.forEach((obj, objIndex) => {
        const objErrors = {}
        objErrors.project_name = !obj || !obj.project_name ? 'Required' : undefined;
        objErrors.start_date = !obj || !obj.start_date ? 'Required' : undefined;
        objErrors.end_date = !obj || (!obj.end_date && !obj.currently_working) ? 'Required' : undefined;
        listErrors[objIndex] = objErrors
    });
    if (listErrors.length) {
        errors.list = listErrors;
        ////console.log(errors)
        return errors;
    }

};


export default validate;