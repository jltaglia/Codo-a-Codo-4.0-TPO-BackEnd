document.getElementById("mi_footer").innerHTML = `
    <div class="social">
        <span><a href="https://www.facebook.com/profile.php?id=100075834332674" target="_blank"
                class="icon-facebook"><i class="fa-brands fa-facebook-square"></i></a></span>
        <span><a href="http://www.twitter.com/@JLPatagonico" target="_blank" class="icon-twitter"><i
                    class="fa-brands fa-twitter-square"></i></a></span>
        <span><a href="https://www.instagram.com/vendotodorawson/" target="_blank" class="icon-instagram"><i
                    class="fa-brands fa-instagram"></i></a></span>
        <span><a href="https://ar.pinterest.com/vendotodorawson/vendo-todo-por-mudanza/" target="_blank"
                class="icon-pinterest"><i class="fa-brands fa-pinterest-square"></i></a></span>
        <span><a href="mailto:vendotodorawson@gmail.com" class="icon-mail"><i
                    class="fa-solid fa-square-envelope"></i></a></span>
    </div>
`;


// ------------------------------ PARA CARGAR EL MENU SEGUN LA PAG ACTIVA ------------------------------
var pagina = document.title
var opciones = [ "<a href=\"./index.html\"><i class=\"fa-solid fa-house\"></i></a>", 
                "<a href=\"./articulos.html\">Mis Articulos</a>",
                "<a href=\"./acerca.html\">Nosotros</a>",
                "<a href=\"./contacto.html\">Contacto</a>"
                ];

switch (pagina) {
    case "Vendo Todo Por Mudanza!":
        opciones[0] = "<a href=\"./index.html\"><i class=\"fa-solid fa-house active\"></i></a>";
        break

    case "VTxM! - Mis Articulos":
        opciones[1] = "<a href=\"#Articulos\" class=\"active\">Mis Articulos</a>";
        break

    case "VTxM! - Acerca de Nosotros":
        opciones[2] = "<a href=\"#acerca\" class=\"active\">Nosotros</a>";
        break

    case "VTxM! - Contacto":
        opciones[3] = "<a href=\"#contacto\" class=\"active\">Contacto</a>";
        break
}
var header_completo = `
    <div class="topnav" id="miTopnav">
        ${opciones[0]}
        ${opciones[1]}
        ${opciones[2]}
        ${opciones[3]}
        <a href="javascript:void(0);" class="icon" onclick="funMenu()">
            <i class="fa fa-bars"></i>
        </a>
    </div>
    `;
document.getElementById("mi_header").innerHTML = header_completo;


// ---------------------- PARA CARGAR LOS ARTICULOS EN LA TABLA DE ARTICULOS ----------------------
if (document.getElementById("tabla_productos")) {

    tabla = `
        <table>
        <tr>
            <th>Descripción</th>
            <th>Cantidad</th>
            <th>Precio Oferta</th>
            <th>Código</th>
        </tr>
`;

    for (let i = 0; i < articulos.length; i++) {
        tabla += `
        <tr>
            <td>${articulos[i].descripcion}</td>
            <td>${articulos[i].cantidad}</td>
            <td>${articulos[i].precio_oferta}</td>
            <td>${articulos[i].codigo}</td>
        </tr>
    `;

    }
    tabla += `
        </table>
    `;
    console.log(tabla);
    document.getElementById("tabla_productos").innerHTML = tabla;
};

// ----------------------- PARA HACER RESPONSIVE EL MENU -----------------------
function funMenu() {
    var x = document.getElementById("miTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {
        x.className = "topnav";
    }
};

// ------------------------ PARA VALIDAR EL FORMULARIO DE CONTACTO ------------------------
function valida_contacto() {
    var nombre = document.forms["frmContacto"]["fnombre"].value;
    if (nombre == "") {
        alert("Completá tu nombre por favor...");
        return false;
    }
    var apellido = document.forms["frmContacto"]["fapellido"].value;
    if (apellido == "") {
        alert("Completá tu apellido por favor...");
        return false;
    }
    if (document.forms["frmContacto"]["ftelefono"].value !== "") {
        var telefono = document.forms["frmContacto"]["ftelefono"].value;
        if (telefono.length < 10) {
            alert("El número de teléfono es muy corto");
            return false;
        }
        if (isNaN(telefono)) {
            alert("El número de teléfono solo puede incluir un \"+\" y números");
            return false;
        }
    }
    var mail = document.forms["frmContacto"]["fmail"].value;
    if (mail == "") {
        alert("Completá tu email por favor...");
        return false;
    } else {
        var expresion = /\w+@\w+\.+[a-z]/;
        if (!expresion.test(mail)) {
            alert("El email ingresado no es válido...");
            return false;
        }
    }
    var mensaje = document.forms["frmContacto"]["fmensaje"].value;
    if (mensaje == "") {
        alert("Por favor escribinos por que nos contactás...");
        return false;
    }
};
// ---------------------------------------------------------------------------------------