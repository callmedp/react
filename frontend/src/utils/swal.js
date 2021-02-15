import Swal from 'sweetalert2';

const showSwal = (icon, title) => {
    return Swal.fire({
        icon : icon, 
        title : title,
        confirmButtonClass: "btn btn-blue",
    });
}

export {
    showSwal
}