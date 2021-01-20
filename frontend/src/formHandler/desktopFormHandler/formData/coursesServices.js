export default {
    'name': {
        className: "form-control",
        type: "text",
        name: "comment",
        id: "name",
        label: "Comment*",
        inputType: 'input',
        rows: 3,
        validation: {
            required:true,
        },
        // errorMessage: {
        //     required: "This field is required",
        // }
        
    },
    'email': {
        className: "input_field form-control",
        type: "text",
        name: "email",
        id: "email",
        label: "Email",
        inputType: 'input',
        validation: {
            // required:true,
            pattern:/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/,
        },
        errorMessage: {
            // required: "This field is required",
            pattern: "Email address is invalid!",
            
        }
    },
    'mobile': {
        className: "input_field form-control",
        type: "number",
        name: "number",
        id: "number",
        label: "Mobile*",
        inputType: 'input',
        validation: {
            required:true,
            pattern:/^[0-9-]+$/,
            validate : {
                mobLength : value =>  value?.toString().length === 10 
            }
        },
        errorMessage: {
            required: "This field is required",
            pattern: "Mobile number is invalid!",
            mobLength : "Mobile number is invalid!"
        }
    },
}