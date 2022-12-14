function cambiarProvincia() {
    let id_region = document.getElementById('id_region').value;
    let url = 'http://localhost:8000/dash/usuarios/provincias/?id_region=' + id_region;
    fetch(url)
        .then(res => res.text())
        .then(resultado => {
            document.getElementById('id_provincia').innerHTML = resultado;
        });
}

function cambiarComuna() {
    let id_provincia = document.getElementById('id_provincia').value;
    let url = 'http://localhost:8000/dash/usuarios/comunas/?id_provincia=' + id_provincia;
    fetch(url)
        .then(res => res.text())
        .then(resultado => {
            document.getElementById('id_comuna_user').innerHTML = resultado;
        });
}

function mostrarApoderado(){
    document.getElementById('div-apoderado').style.display = 'block';
}

function ocultarApoderado(){
    document.getElementById('div-apoderado').style.display = 'none';
}

function perfilApoderado(radio){
    if(radio.checked){
        mostrarApoderado();
    }else{
        ocultarApoderado();
    }
}

function rd_perfil(id_radio){
    let radios = ['is_admin', 'is_alumno', 'is_profesor', 'is_administrativo', 'is_apoderado', 'is_inspector', 'is_auditor']
    radios.forEach(function(radio, index){
        document.getElementById(radio).checked = false;
        if(radio == id_radio.id){
            document.getElementById(radio).checked = true;
            if(radio=='is_apoderado'){
                mostrarApoderado();
            }else{
                ocultarApoderado();
            }
        }
        
    });
}
//document.getElementById('btn-limpiar-form').addEventListener('onclick', function(){
//    document.getElementById('form').reset();
//});


// const btns_eliminacion = document.querySelectorAll('.btn-eliminar');


// (function (){
//     Swal.fire({
//         'title': 'Hola',
//         'text': 'Wena Maui!!',
//         'icon': 'success',
//         'showCancelButton': true,
//         'cancelButtonText': 'Volver',
//         'confirmButtonText': 'Cancel',
//         'confirmButtonColor': '#dc3545',
//     });
// })();

const notificationSwal = (titulo, texto, icon, confirmButtonText)=>{
    Swal.fire({
        'title': titulo,
        'text': texto,
        'icon': icon, // warning, error, success, info
        'confirmButtonText': confirmButtonText,
        'confirmButtonColor': '#dc3545',
    });
}

const questionSwal = (titulo, texto, icon, showCancelButton, cancelButtonText, confirmButtonText) => {
    Swal.fire({
        'title': titulo,
        'text': texto,
        'icon': icon, // warning, error, success, info
        'showCancelButton': showCancelButton,
        'cancelButtonText': cancelButtonText,
        'confirmButtonText': confirmButtonText,
        'confirmButtonColor': '#dc3545',
    })
}