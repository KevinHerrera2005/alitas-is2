function inicializarPantallasAccionesAdmin() {
    const selectorAccion = document.getElementById("accion_disponible")
    const listaAcciones = document.getElementById("acciones_seleccionadas")
    const hiddenAcciones = document.getElementById("acciones_ids")
    const btnAgregar = document.getElementById("btn_agregar_accion")
    const btnEliminar = document.getElementById("btn_eliminar_accion")

    if (!selectorAccion || !listaAcciones || !hiddenAcciones || !btnAgregar || !btnEliminar) {
        return
    }

    function actualizarHidden() {
        depurarEstado("despues de agregar")
        const ids = Array.from(listaAcciones.options).map(opcion => opcion.value)
        hiddenAcciones.value = ids.join(",")
    }

    function existeEnLista(valor) {
        return Array.from(listaAcciones.options).some(opcion => opcion.value === String(valor))
    }

    function agregarALaLista(valor, texto) {
        if (!valor || String(valor) === "0") {
            return
        }

        if (existeEnLista(valor)) {
            return
        }

        const nuevaOpcion = new Option(texto, valor)
        listaAcciones.add(nuevaOpcion)
    }

    function cargarAccionesIniciales() {
        const ids = (hiddenAcciones.value || "")
            .split(",")
            .map(valor => valor.trim())
            .filter(valor => valor !== "" && valor !== "0")

        ids.forEach(function (id) {
            const opcion = Array.from(selectorAccion.options).find(op => op.value === id)
            if (opcion) {
                agregarALaLista(opcion.value, opcion.text)
            }
        })

        actualizarHidden()
        function depurarEstado(origen) {
    console.log("---- " + origen + " ----")
    console.log("hidden:", hiddenAcciones.value)
    console.log("lista:", Array.from(listaAcciones.options).map(opcion => ({
        value: opcion.value,
        text: opcion.text,
        selected: opcion.selected
    })))
}
    }

    btnAgregar.addEventListener("click", function () {
        const valor = selectorAccion.value
        const texto = selectorAccion.options[selectorAccion.selectedIndex]?.text || ""

        if (!valor || valor === "0") {
            return
        }

        agregarALaLista(valor, texto)
        actualizarHidden()
    })

btnEliminar.addEventListener("click", function () {
    const seleccionadas = Array.from(listaAcciones.options).filter(opcion => opcion.selected)

    if (!seleccionadas.length) {
        return
    }

    seleccionadas.forEach(opcion => opcion.remove())
    actualizarHidden()
    depurarEstado("despues de eliminar")
})

    cargarAccionesIniciales()
    depurarEstado("despues de cargar iniciales")
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", inicializarPantallasAccionesAdmin)
} else {
    inicializarPantallasAccionesAdmin()
const formulario = hiddenAcciones.closest("form")

if (formulario) {
    formulario.addEventListener("submit", function () {
        actualizarHidden()
        depurarEstado("antes de enviar formulario")
    })
}
}