import Swal from 'sweetalert2';

const showSwal = (icon, title) => {
    return Swal.fire({
        icon : icon, 
        title : title
    });
}

export {
    showSwal
}