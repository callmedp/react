import Swal from 'sweetalert2'

const fileUpload = event => {
    event.persist();
    let file1 = event.target.files[0];
    event.target.value = null
    if (file1.size / (1024 * 1024) > 5) {
        Swal.fire({
            icon: 'error',
            title: 'File size should be less than 5 MB'
        })
        return false
    }
    if (!(file1.name.slice(-4).toLowerCase() === '.pdf' || file1.name.slice(-4).toLowerCase() === '.doc' || file1.name.slice(-5).toLowerCase() === '.docx' || file1.name.slice(-4).toLowerCase() === '.txt')) {
        Swal.fire({
            icon: 'error',
            title: 'Please select the file in the format PDF,DOC,DOCX,TXT only'
        })
        return false
    }
    return file1
}
export default fileUpload