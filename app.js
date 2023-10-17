const correoUsuario = document.getElementById('idEmail');

const buttonRegistrarme = document.getElementById('buttonRegistrarme');
const nameRegistro = document.getElementById('nameRegistro');
const lastnameRegistro = document.getElementById('lastnameRegistro');
const emailRegistro = document.getElementById('emailRegistro');
const passRegistro = document.getElementById('passRegistro');

const usuarioIngresado = document.getElementById('usuarioIngresado');



let nameGuardado = sessionStorage.getItem('nameGuardado');
let lastnameGuardado = sessionStorage.getItem('lastnameGuardado');
let emailGuardado = sessionStorage.getItem('emailGuardado');
let passGuardado = sessionStorage.getItem('passGuardado');


buttonRegistrarme.addEventListener('click', () => {    
    sessionStorage.setItem('nameGuardado', nameRegistro.value);
    sessionStorage.setItem('lastnameGuardado', lastnameRegistro.value);
    sessionStorage.setItem('emailGuardado', emailRegistro.value);
    sessionStorage.setItem('passGuardado', passRegistro.value);
    alert('Usuario registrado con éxito')
    // mostrarUsuario()
});


// const mostrarUsuario = () => {
//     var data = sessionStorage.getItem("nameGuardado");

//     if (data === 'milena') {
//         usuarioIngresado.innerHTML = `
//         <a class="nav-link itemsNavbar" data-bs-toggle="modal" data-bs-target="#exampleModal" href="#" id="usuarioIngresado">MILENA</a>                         
                            
//         `
//         console.log('es milena')
//     }
// };