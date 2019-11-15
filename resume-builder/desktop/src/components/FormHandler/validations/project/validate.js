const validate = values => {
    const errors = {}, listErrors = [], valuesLength =3;
    values = (values && values.list) || [];
    values.forEach((obj, objIndex) => {
        const objErrors = {}
        objErrors.project_name = !obj || !obj.project_name ? 'Required' : undefined;
        objErrors.start_date = !obj || !obj.start_date ? 'Required' : undefined;
        objErrors.end_date = !obj || (!obj.end_date && !obj.currently_working) ? 'Required' : undefined;
        listErrors[objIndex] = objErrors
    });
    if (listErrors.length) {
        const errorElementsCount = Object.values(listErrors[0]).filter(el => el != undefined).length;
        if (listErrors.length <= 1 && errorElementsCount === valuesLength) {
            return errors;
        }
        errors.list = listErrors;
        return errors;
    }

};


export default validate;