export const awardNewData = (fields) => {
    return {
        "candidate_id": '',
        "id": '',
        "title": '',
        "date": '',
        "summary": '',
        "order": fields.length
    }
}

export const courseNewData = (fields) => {
    return {
        "candidate_id": '',
        "id": '',
        "name_of_certification": '',
        "year_of_certification": '',
        order: fields.length
    }

}

export const educationNewData = (fields) => {
    return {
            "candidate_id": '',
            "id": '',
            "specialization": '',
            "institution_name": '',
            "course_type": '',
            "start_date": '',
            "percentage_cgpa": '',
            "end_date": '',
            "is_pursuing": false,
            order: fields.length 
    }
}

export const experienceNewData = (fields) => {
    return {
            "candidate_id": '',
            "id": '',
            "job_profile": '',
            "company_name": '',
            "start_date": '',
            "end_date": '',
            "is_working": false,
            "job_location": '',
            "work_description": '',
            order: fields.length    
    }
}

export const languageNewData = (fields) => {
    return {
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": 5,
            order: fields.length  
    }
}

export const projectNewData = (fields) => {
    return {
            "candidate_id": '',
            "id": '',
            "project_name": '',
            "start_date": '',
            "end_date": '',
            "skills": [],
            "description": '',
            order: fields.length
    }
}

export const referenceNewData = (fields) => {
    return {
            "candidate_id": '',
            "id": '',
            "reference_name": '',
            "reference_designation": '',
            "about_user": "",
            order: fields.length
    }
}

export const skillNewData = (fields) => {
    return {
            "candidate_id": '',
            "id": '',
            "name": '',
            "proficiency": 5,
            "order": fields.length  
    }
}

