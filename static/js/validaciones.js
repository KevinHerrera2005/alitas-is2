function msgAnchor(el) {
  if (!el) return null;
  if (el.classList && el.classList.contains("select2-hidden-accessible")) {
    const cont = el.nextElementSibling;
    if (cont && cont.classList && (cont.classList.contains("select2") || cont.classList.contains("select2-container"))) {
      return cont;
    }
  }
  return el;
}

function ensureMsgElem(input) {
  const anchor = msgAnchor(input) || input;
  let next = anchor.nextElementSibling;
  if (!next || !next.classList || !next.classList.contains("msg")) {
    let div = document.createElement("div");
    div.className = "msg";
    anchor.insertAdjacentElement("afterend", div);
    return div;
  }
  return next;
}

function mostrarMensaje(input, mensaje, ok = false) {
  if (!input) return;

  const anchor = msgAnchor(input) || input;
  let msg = anchor.nextElementSibling;

  if (!msg || !msg.classList || !msg.classList.contains("msg")) {
    msg = document.createElement("div");
    msg.className = "msg";
    anchor.insertAdjacentElement("afterend", msg);
  }

  msg.textContent = mensaje || "";
  msg.className = ok ? "msg ok" : "msg error";
  msg.style.color = ok ? "green" : "red";
  msg.style.fontSize = "0.85rem";
  msg.style.marginTop = "4px";
}

function mostrarMensajeDebajo(input, texto, esOk) {
  if (!input) return;

  const anchor = msgAnchor(input) || input;
  let msg = anchor.nextElementSibling;

  if (!msg || !msg.classList || !msg.classList.contains("msg")) {
    msg = document.createElement("div");
    msg.className = "msg";
    msg.style.fontSize = "0.8rem";
    msg.style.marginTop = "4px";
    anchor.insertAdjacentElement("afterend", msg);
  }

  msg.textContent = texto || "";
  msg.className = esOk ? "msg ok" : "msg error";
  msg.style.color = esOk ? "green" : "red";
}

function tieneTresIguales(valor) {
  const lower = (valor || "").toLowerCase();
  return /(.)\1\1/.test(lower);
}

function activarBotonEnFormulario(form) {
  if (!form) return;

  const botones = form.querySelectorAll('button[type="submit"], input[type="submit"]');
  const hayError = Array.from(form.querySelectorAll(".msg")).some((m) => m.classList.contains("error"));

  botones.forEach((b) => {
    b.disabled = hayError;
  });
}

function validarPuntosEnNombre(value) {
  const v = String(value || "");

  if (/^\s*\./.test(v)) return { ok: false, msg: "No se permite puntos al inicio" };
  if (/\.\s*\./.test(v)) return { ok: false, msg: "No se permiten doble puntos" };

  return { ok: true, msg: "" };
}

function sanitizeAndFormatNameField(el) {
  if (!el) return;

  const start = el.selectionStart;
  const end = el.selectionEnd;

  let v = String(el.value || "");

  v = v.replace(/^ +/, "").replace(/ {2,}/g, " ");
  v = v.replace(/ +\./g, ".");
  v = v.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ .]/g, "");

  v = v.toLowerCase();
  v = v.replace(/(^|[.\s])([a-záéíóúñ])/gu, (m, p1, p2) => p1 + p2.toUpperCase());

  el.value = v;

  try {
    const len = el.value.length;
    const ns = Math.min(start, len);
    const ne = Math.min(end, len);
    el.setSelectionRange(ns, ne);
  } catch (e) {}
}

function attachDotRulesToNameInput(input) {
  if (!input || input.dataset.dotRulesAttached === "1") return;
  input.dataset.dotRulesAttached = "1";

  input.addEventListener("keydown", function (e) {
    const k = e.key;
    if (k !== ".") return;

    const pos = typeof input.selectionStart === "number" ? input.selectionStart : 0;
    const before = String(input.value || "").slice(0, pos);

    const form = input.closest("form");

    if (before.trim().length === 0) {
      e.preventDefault();
      mostrarMensaje(input, "No se permite puntos al inicio", false);
      activarBotonEnFormulario(form);
      return;
    }

    const beforeNoTrailSpaces = before.replace(/\s+$/g, "");
    if (beforeNoTrailSpaces.endsWith(".")) {
      e.preventDefault();
      mostrarMensaje(input, "No se permiten doble puntos", false);
      activarBotonEnFormulario(form);
      return;
    }
  });
}

function initValidacionesOrdenEntrega() {
  var selectEstado = document.getElementById("estado");
  var txtMotivo = document.getElementById("Motivo_Cancelacion");

  if (!selectEstado || !txtMotivo) return;

  var estadoInicial = parseInt(selectEstado.value || "0", 10);
  if (isNaN(estadoInicial)) estadoInicial = 0;

  function actualizarMotivo() {
    var estadoActual = parseInt(selectEstado.value || "0", 10);
    if (estadoActual === 4) {
      txtMotivo.disabled = false;
    } else {
      txtMotivo.value = "";
      txtMotivo.disabled = true;
    }
  }

  actualizarMotivo();

  selectEstado.addEventListener("change", function () {
    var nuevoEstado = parseInt(this.value || "0", 10);

    if (nuevoEstado < estadoInicial && nuevoEstado !== 4) {
      alert("estado no puede retroceder");
      this.value = String(estadoInicial);
      actualizarMotivo();
      return;
    }

    if (nuevoEstado === 4) {
      var ok = confirm("¿Estás seguro que quieres cancelar esta orden?");
      if (!ok) {
        this.value = String(estadoInicial);
        actualizarMotivo();
        return;
      }
    }

    actualizarMotivo();
  });

  txtMotivo.addEventListener("input", function () {
    if (this.disabled) {
      this.value = "";
      return;
    }
    if (typeof validarDescripcion === "function") {
      validarDescripcion(this);
      const form = this.closest("form");
      activarBotonEnFormulario(form);
    }
  });
}

function initValidacionDocumentoEmpleado() {
  const tipoSel =
    document.getElementById("emp_doc_tipo") ||
    document.querySelector('select[name="tipo_documento_empleado"]');

  const numInp =
    document.getElementById("emp_doc_numero") ||
    document.querySelector('input[name="numero_identificador"]');

  if (!tipoSel || !numInp) return;

  const form = numInp.closest("form");

  function tipoActual() {
    const v = String(tipoSel.value || "").trim().toLowerCase();
    const opt = tipoSel.options && tipoSel.selectedIndex >= 0 ? tipoSel.options[tipoSel.selectedIndex] : null;
    const t = String((opt ? opt.textContent : "") || "").trim().toLowerCase();
    return { value: v, text: t };
  }

  function reglas() {
    const t = tipoActual();
    const v = t.value;
    const txt = t.text;

    if (v === "1" || txt.includes("dni")) return { kind: "num", len: 13, label: "DNI" };
    if (v === "2" || txt.includes("rtn")) return { kind: "num", len: 14, label: "RTN" };
    if (v === "3" || txt.includes("pasaporte")) return { kind: "alnum", len: 6, label: "Pasaporte" };
    if (v === "4" || txt.includes("otro")) return { kind: "alnum", len: 14, label: "Otro" };

    return { kind: "alnum", len: 14, label: "Documento" };
  }

  function filtrar(valor, kind, maxLen) {
    let v = String(valor || "");
    if (kind === "num") v = v.replace(/\D/g, "");
    else v = v.replace(/[^A-Za-z0-9]/g, "");
    return v.slice(0, maxLen);
  }

  function validarValor() {
    const r = reglas();
    const v = String(numInp.value || "").trim();

    if (!v) return { ok: false, msg: "Este campo es obligatorio." };

    if (r.kind === "num") {
      if (!/^\d+$/.test(v)) return { ok: false, msg: "Solo se permiten números." };
      if (v.length !== r.len) return { ok: false, msg: "Debe tener exactamente " + r.len + " dígitos para " + r.label + "." };
    } else {
      if (!/^[A-Za-z0-9]+$/.test(v)) return { ok: false, msg: "Solo letras y números (sin caracteres especiales)." };
      if (v.length !== r.len) return { ok: false, msg: "Debe tener exactamente " + r.len + " caracteres para " + r.label + "." };
    }

    return { ok: true, msg: "Documento válido ✔" };
  }

  function refrescar() {
    const r = reglas();

    numInp.value = filtrar(numInp.value, r.kind, r.len);

    numInp.setAttribute("maxlength", String(r.len));
    numInp.setAttribute("minlength", String(r.len));
    numInp.setAttribute("inputmode", r.kind === "num" ? "numeric" : "text");
    numInp.setAttribute("autocomplete", "off");

    const res = validarValor();
    mostrarMensaje(numInp, res.msg, res.ok);
    activarBotonEnFormulario(form);
  }

  tipoSel.addEventListener("change", function () {
    numInp.value = "";
    refrescar();
  });

  numInp.addEventListener("input", refrescar);
  numInp.addEventListener("blur", refrescar);
  numInp.addEventListener("paste", function () {
    setTimeout(refrescar, 0);
  });

  if (form) {
    form.addEventListener("submit", function (e) {
      refrescar();
      const res = validarValor();
      if (!res.ok) {
        e.preventDefault();
        numInp.focus();
      }
    });
  }

  refrescar();
}

function normalizarYFormatearCAI(valor) {
  const raw = String(valor || "").replace(/[^A-Za-z0-9]/g, "").toUpperCase().slice(0, 32);

  const lens = [6, 6, 6, 6, 6, 2];
  const partes = [];
  let idx = 0;

  for (let i = 0; i < lens.length; i++) {
    const seg = raw.slice(idx, idx + lens[i]);
    if (seg.length) partes.push(seg);
    idx += lens[i];
  }

  return { raw, formatted: partes.join("-") };
}

function validarCAIFormateado(valor) {
  const v = String(valor || "").trim();
  if (!v) return { ok: false, msg: "El número CAI es obligatorio" };
  if (v.length !== 37) return { ok: false, msg: "Debe tener exactamente 37 caracteres (XXXXXX-XXXXXX-XXXXXX-XXXXXX-XXXXXX-XX)" };
  if (!/^[A-Z0-9]{6}(?:-[A-Z0-9]{6}){4}-[A-Z0-9]{2}$/.test(v)) return { ok: false, msg: "Formato CAI inválido" };
  return { ok: true, msg: "Número CAI válido ✔" };
}

function initNumeroCAIAdmin() {
  const input = document.getElementById("num_cai") || document.querySelector('input[name="num_cai"]');
  if (!input) return;

  const form = input.closest("form");

  input.setAttribute("maxlength", "37");
  input.setAttribute("autocomplete", "off");

  function aplicar() {
    const old = input.value || "";
    const caret = input.selectionStart || 0;
    const rawBefore = old.slice(0, caret).replace(/[^A-Za-z0-9]/g, "").length;

    const norm = normalizarYFormatearCAI(old);
    input.value = norm.formatted;

    const cortes = [6, 12, 18, 24, 30];
    const hyphens = cortes.filter((c) => c <= rawBefore).length;
    let newPos = rawBefore + hyphens;
    if (newPos > input.value.length) newPos = input.value.length;

    try {
      input.setSelectionRange(newPos, newPos);
    } catch (e) {}

    const res = validarCAIFormateado(input.value);
    mostrarMensaje(input, res.msg, res.ok);
    activarBotonEnFormulario(form);
  }

  input.addEventListener("input", aplicar);
  input.addEventListener("blur", aplicar);
  input.addEventListener("paste", function () { setTimeout(aplicar, 0); });

  if (form) {
    form.addEventListener("submit", function (e) {
      aplicar();
      const res = validarCAIFormateado(input.value);
      if (!res.ok) {
        e.preventDefault();
        input.focus();
      }
    });
  }

  aplicar();
}

function validarRangosCAI() {
  const rangoInicial = document.getElementById("rango_inicial");
  const rangoFinal = document.getElementById("rango_final");
  if (!rangoInicial || !rangoFinal) return;

  const form = (rangoFinal.closest && rangoFinal.closest("form")) || null;

  function verificar() {
    const ini = parseInt(rangoInicial.value, 10);
    const fin = parseInt(rangoFinal.value, 10);

    if (isNaN(ini) || isNaN(fin)) {
      mostrarMensajeDebajo(rangoFinal, "", true);
      activarBotonEnFormulario(form);
      return;
    }

    if (ini >= fin) {
      mostrarMensajeDebajo(rangoFinal, "⚠ El rango inicial debe ser menor que el rango final.", false);
    } else {
      mostrarMensajeDebajo(rangoFinal, "", true);
    }

    activarBotonEnFormulario(form);
  }

  rangoInicial.addEventListener("input", verificar);
  rangoFinal.addEventListener("input", verificar);

  verificar();
}

function validarSecuenciaCAI() {
  const rangoInicial = document.getElementById("rango_inicial");
  const rangoFinal = document.getElementById("rango_final");
  const secuencia = document.getElementById("secuencia_actual");
  if (!rangoInicial || !rangoFinal || !secuencia) return;

  const form = (secuencia.closest && secuencia.closest("form")) || null;

  function verificar() {
    const ini = parseInt(rangoInicial.value, 10);
    const fin = parseInt(rangoFinal.value, 10);
    const sec = parseInt(secuencia.value, 10);

    if (isNaN(ini) || isNaN(fin) || isNaN(sec)) {
      mostrarMensajeDebajo(secuencia, "", true);
      activarBotonEnFormulario(form);
      return;
    }

    if (sec < ini) {
      mostrarMensajeDebajo(secuencia, "La secuencia actual no puede ser menor que el rango inicial.", false);
      activarBotonEnFormulario(form);
      return;
    }

    if (sec >= fin) {
      mostrarMensajeDebajo(secuencia, "La secuencia actual debe ser menor que el rango final.", false);
      activarBotonEnFormulario(form);
      return;
    }

    mostrarMensajeDebajo(secuencia, "", true);
    activarBotonEnFormulario(form);
  }

  rangoInicial.addEventListener("input", verificar);
  rangoFinal.addEventListener("input", verificar);
  secuencia.addEventListener("input", verificar);
  secuencia.addEventListener("blur", verificar);

  verificar();
}

function validarFechasCAI() {
  const fechaEmision = document.getElementById("fecha_emision");
  const fechaFinal = document.getElementById("fecha_final");
  if (!fechaEmision || !fechaFinal) return;

  const form = (fechaFinal.closest && fechaFinal.closest("form")) || null;

  function revisar() {
    const v1 = fechaEmision.value;
    const v2 = fechaFinal.value;

    if (!v1 || !v2) {
      mostrarMensajeDebajo(fechaFinal, "", true);
      activarBotonEnFormulario(form);
      return;
    }

    const inicio = new Date(v1);
    const fin = new Date(v2);

    if (fin < inicio) {
      mostrarMensajeDebajo(fechaFinal, "⚠ La fecha final no puede ser anterior a la fecha de emisión.", false);
    } else {
      mostrarMensajeDebajo(fechaFinal, "", true);
    }

    activarBotonEnFormulario(form);
  }

  fechaEmision.addEventListener("change", revisar);
  fechaFinal.addEventListener("change", revisar);

  revisar();
}

function validarNumero(input) {
  let valor = input.value;
  valor = valor.replace(/[^0-9.]/g, "");
  valor = valor.replace(/(\..*)\./g, "$1");
  input.value = valor;

  if (valor === "") return mostrarMensaje(input, "Este campo es obligatorio");

  let num = parseFloat(valor);
  if (isNaN(num)) return mostrarMensaje(input, "Debe ingresar un número válido");
  if (num < 0) return mostrarMensaje(input, "No se permiten números negativos");

  return mostrarMensaje(input, "Válido ✔", true);
}

function validarNumeroPositivo(input) {
  let valor = input.value;
  valor = valor.replace(/[^0-9.]/g, "");
  valor = valor.replace(/(\..*)\./g, "$1");
  input.value = valor;

  if (valor === "") {
    mostrarMensaje(input, "Este campo es obligatorio");
    return false;
  }

  const num = parseFloat(valor);
  if (isNaN(num)) {
    mostrarMensaje(input, "Debe ingresar un número válido");
    return false;
  }

  if (num <= 0) {
    mostrarMensaje(input, "El número debe ser mayor a 0");
    return false;
  }

  mostrarMensaje(input, "Válido ✔", true);
  return true;
}

function validarCantidadUsada(input) {
  let valor = input.value.replace(",", ".");
  valor = valor.replace(/[^0-9.]/g, "");
  valor = valor.replace(/(\..*)\./g, "$1");
  input.value = valor;

  if (valor === "") {
    mostrarMensaje(input, "La cantidad usada es obligatoria");
    return false;
  }

  const soloDigitos = valor.replace(".", "");
  if (soloDigitos.length > 5) {
    mostrarMensaje(input, "La cantidad usada no puede tener más de 5 dígitos");
    return false;
  }

  const num = parseFloat(valor);
  if (isNaN(num)) {
    mostrarMensaje(input, "Debe ingresar un número válido");
    return false;
  }

  if (num <= 0) {
    mostrarMensaje(input, "La cantidad usada debe ser mayor que 0");
    return false;
  }

  mostrarMensaje(input, "Cantidad válida ✔", true);
  return true;
}

function validarPrecioInsumo(input) {
  let valor = input.value.replace(",", ".");
  valor = valor.replace(/[^0-9.]/g, "");
  valor = valor.replace(/(\..*)\./g, "$1");
  input.value = valor;

  if (valor === "") {
    mostrarMensaje(input, "El precio es obligatorio");
    return false;
  }

  const soloDigitos = valor.replace(".", "");
  if (soloDigitos.length > 10) {
    mostrarMensaje(input, "El precio no puede tener más de 10 dígitos");
    return false;
  }

  const num = parseFloat(valor);
  if (isNaN(num)) {
    mostrarMensaje(input, "Debe ingresar un número válido");
    return false;
  }

  if (num <= 0) {
    mostrarMensaje(input, "El precio debe ser mayor a 0");
    return false;
  }

  mostrarMensaje(input, "Válido ✔", true);
  return true;
}

function validarNombre(input) {
  const valorOriginal = String(input.value || "");
  const valor = valorOriginal.trim();

  const puntos = validarPuntosEnNombre(valorOriginal);
  if (!puntos.ok) return mostrarMensaje(input, puntos.msg, false);

  if (valor.length < 3 || valor.length > 40) {
    return mostrarMensaje(input, "Debe tener entre 3 y 40 caracteres", false);
  }

  if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ .]+$/.test(valorOriginal)) {
    return mostrarMensaje(input, "Solo se permiten letras, espacios y punto", false);
  }

  const sinSeparadores = valor.replace(/[ .]/g, "");
  if (sinSeparadores.length < 3) {
    return mostrarMensaje(input, "Debe contener al menos 3 letras", false);
  }

  if (tieneTresIguales(sinSeparadores)) {
    return mostrarMensaje(input, "No puede tener 3 caracteres iguales seguidos", false);
  }

  return mostrarMensaje(input, "Campo válido ✔", true);
}

function validarUsername(input) {
  let username = (input.value || "").trim();
  username = username.replace(/\s+/g, "");
  input.value = username;

  if (username.length === 0) return mostrarMensaje(input, "El usuario es obligatorio");
  if (username.length < 3 || username.length > 20) return mostrarMensaje(input, "El usuario debe tener entre 3 y 20 caracteres");
  if (!/^[A-Za-z0-9_]+$/.test(username)) return mostrarMensaje(input, "El usuario solo puede contener letras, números o guiones bajos (_).");

  return mostrarMensaje(input, "Usuario válido ✔", true);
}

function validarPassword(input) {
  const pass = input.value;

  if (pass.length < 8 || pass.length > 20) return mostrarMensaje(input, "Debe tener entre 8 y 20 caracteres");
  if (!/[A-Z]/.test(pass)) return mostrarMensaje(input, "Debe contener una mayúscula");
  if (!/[a-z]/.test(pass)) return mostrarMensaje(input, "Debe contener una minúscula");
  if (!/\d/.test(pass)) return mostrarMensaje(input, "Debe contener un número");
  if (!/[!@#$&]/.test(pass)) return mostrarMensaje(input, "Debe incluir !, @, #, $, &");

  mostrarMensaje(input, "Contraseña válida ✔", true);
  return true;
}

function validarConfirmar(input) {
  const passInput = document.querySelector("[data-validacion='password']");
  const pass = passInput ? passInput.value : "";

  if (input.value !== pass) return mostrarMensaje(input, "Las contraseñas no coinciden");

  mostrarMensaje(input, "Coinciden ✔", true);
  return true;
}

function validarEmail(input) {
  let valor = (input.value || "").trim();
  input.value = valor;

  if (valor.length === 0) return mostrarMensaje(input, "El correo es obligatorio");
  if (valor.length < 6 || valor.length > 60) return mostrarMensaje(input, "El correo debe tener entre 6 y 60 caracteres");
  if (/\s/.test(valor)) return mostrarMensaje(input, "El correo no puede tener espacios");

  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!regex.test(valor)) return mostrarMensaje(input, "Debe ingresar un correo válido");

  return mostrarMensaje(input, "Correo válido ✔", true);
}

function validarTelefono(input) {
  let tel = (input.value || "").replace(/\D/g, "");
  input.value = tel;

  if (tel.length !== 8) return mostrarMensaje(input, "Debe tener 8 dígitos");
  if (!/^[3789]/.test(tel)) return mostrarMensaje(input, "Debe iniciar con 3, 7, 8 o 9");
  if (/^(\d)\1{7}$/.test(tel)) return mostrarMensaje(input, "El teléfono no puede tener todos los dígitos iguales");

  return mostrarMensaje(input, "Teléfono válido ✔", true);
}

function validarDireccion(input) {
  const valor = input.value.trim();
  const sinEspacios = valor.replace(/\s+/g, "");

  if (sinEspacios.length < 5 || sinEspacios.length > 100) return mostrarMensaje(input, "Entre 5 y 100 caracteres");
  if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$/.test(valor)) return mostrarMensaje(input, "Solo letras y números");
  if (tieneTresIguales(sinEspacios)) return mostrarMensaje(input, "No 3 iguales seguidos");

  mostrarMensaje(input, "Dirección válida ✔", true);
  return true;
}

function validarDescripcion(input) {
  let valor = input.value;
  valor = valor.replace(/^ +/, "").replace(/ {2,}/g, " ");
  input.value = valor;

  const limpio = valor.replace(/\s+/g, "").toLowerCase();

  if (limpio.length < 3 || limpio.length > 100) return mostrarMensaje(input, "Debe tener entre 3 y 100 caracteres");
  if (!/^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 ]+$/.test(valor)) return mostrarMensaje(input, "Solo letras y números");
  if (tieneTresIguales(limpio)) return mostrarMensaje(input, "No puede tener 3 caracteres iguales seguidos");

  mostrarMensaje(input, "Descripción válida ✔", true);
  return true;
}

function validarAbreviatura(input) {
  let valor = (input.value || "").trim();

  if (valor.length === 0) return mostrarMensaje(input, "La abreviatura es obligatoria");
  if (valor.length < 1 || valor.length > 4) return mostrarMensaje(input, "Debe tener entre 1 y 4 caracteres");
  if (!/^[A-Za-zÁÉÍÓÚÑáéíóúñ0-9]+$/.test(valor)) return mostrarMensaje(input, "Solo se permiten letras y números, sin espacios");

  input.value = valor.toUpperCase();
  return mostrarMensaje(input, "Abreviatura válida ✔", true);
}

function validarNumeroCai(input) {
  const form = input.closest("form");
  const norm = normalizarYFormatearCAI(input.value || "");
  input.value = norm.formatted;

  const res = validarCAIFormateado(input.value);
  mostrarMensaje(input, res.msg, res.ok);
  activarBotonEnFormulario(form);
  return res.ok;
}

function conectarValidacionesGenerales() {
  const form = document.querySelector("form");
  if (!form) return;

  const inputs = form.querySelectorAll("[data-validacion]");

  inputs.forEach((inp) => ensureMsgElem(inp));

  inputs.forEach((input) => {
    const t = input.dataset.validacion;

    if (t === "nombre" || t === "apellido") attachDotRulesToNameInput(input);

    input.addEventListener("input", () => {
      const k = input.dataset.validacion;

      if (k === "nombre" || k === "apellido") {
        sanitizeAndFormatNameField(input);
        validarNombre(input);
      }
      if (k === "username") validarUsername(input);
      if (k === "password") validarPassword(input);
      if (k === "confirmar") validarConfirmar(input);
      if (k === "telefono") validarTelefono(input);
      if (k === "direccion") validarDireccion(input);
      if (k === "numero") validarNumero(input);
      if (k === "numero_positivo") validarNumeroPositivo(input);
      if (k === "precio_insumo") validarPrecioInsumo(input);
      if (k === "descripcion") validarDescripcion(input);
      if (k === "abreviatura") validarAbreviatura(input);
      if (k === "numero_cai") validarNumeroCai(input);
      if (k === "correo") validarEmail(input);
      if (k === "email") validarEmail(input);

      activarBotonEnFormulario(form);
    });

    input.addEventListener("blur", () => {
      const k = input.dataset.validacion;
      if (k === "nombre" || k === "apellido") {
        sanitizeAndFormatNameField(input);
        validarNombre(input);
      }
      if (k === "numero_cai") validarNumeroCai(input);
      activarBotonEnFormulario(form);
    });

    input.addEventListener("paste", () => {
      setTimeout(() => {
        const k = input.dataset.validacion;
        if (k === "nombre" || k === "apellido") {
          sanitizeAndFormatNameField(input);
          validarNombre(input);
        }
        if (k === "numero_cai") validarNumeroCai(input);
        activarBotonEnFormulario(form);
      }, 0);
    });
  });

  inputs.forEach((input) => {
    const k = input.dataset.validacion;

    if (k === "nombre" || k === "apellido") {
      sanitizeAndFormatNameField(input);
      validarNombre(input);
    }
    if (k === "username") validarUsername(input);
    if (k === "password") validarPassword(input);
    if (k === "confirmar") validarConfirmar(input);
    if (k === "telefono") validarTelefono(input);
    if (k === "direccion") validarDireccion(input);
    if (k === "numero") validarNumero(input);
    if (k === "numero_positivo") validarNumeroPositivo(input);
    if (k === "precio_insumo") validarPrecioInsumo(input);
    if (k === "descripcion") validarDescripcion(input);
    if (k === "abreviatura") validarAbreviatura(input);
    if (k === "numero_cai") validarNumeroCai(input);
    if (k === "correo") validarEmail(input);
    if (k === "email") validarEmail(input);
  });

  activarBotonEnFormulario(form);

  form.addEventListener("submit", function (e) {
    inputs.forEach((input) => input.dispatchEvent(new Event("input", { bubbles: true })));
    activarBotonEnFormulario(form);

    const hayError = Array.from(form.querySelectorAll(".msg")).some((m) => m.classList.contains("error"));
    if (hayError) e.preventDefault();
  });
}

function initRecetaValidaciones() {
  const nombre = document.getElementById("nombre");
  const descripcion = document.getElementById("descripcion");
  if (!nombre || !descripcion) return;

  const msgNombre = document.getElementById("msgNombre");
  const msgDescripcion = document.getElementById("msgDescripcion");
  const guardarBtn = document.getElementById("guardarBtn");

  const selectInsumo = document.getElementById("insumo");
  const selectUnidad = document.getElementById("unidad");
  const inputCantidad = document.getElementById("cantidad");
  const listaInsumosDiv = document.getElementById("listaInsumos");
  const insumosJsonInput = document.getElementById("insumos_json");

  if (inputCantidad) {
    inputCantidad.addEventListener("input", function () {
      validarCantidadUsada(inputCantidad);
    });
  }

  let insumosSeleccionados = [];

  function sanitizeSpaces(el) {
    const start = el.selectionStart;
    const end = el.selectionEnd;

    el.value = el.value.replace(/^ +/, "").replace(/ {2,}/g, " ");

    try {
      const len = el.value.length;
      el.setSelectionRange(Math.min(start, len), Math.min(end, len));
    } catch (e) {}
  }

  function validarNombreReceta() {
    const valor = nombre.value.trim();
    const lower = valor.toLowerCase();
    const sinEspacios = valor.replace(/\s+/g, "");

    if (!msgNombre) return true;

    if (valor.startsWith(" ")) {
      msgNombre.textContent = "No puede iniciar con espacio ✖";
      msgNombre.className = "msg error";
      return false;
    }
    if (/ {2,}/.test(valor)) {
      msgNombre.textContent = "No puede tener múltiples espacios ✖";
      msgNombre.className = "msg error";
      return false;
    }

    const soloNumeros = /^[0-9.]+$/.test(sinEspacios);
    const mezclaNumerosSimbolos = /^[0-9+,.]+$/.test(sinEspacios);
    const letras = (sinEspacios.match(/[A-Za-zÁÉÍÓÚáéíóúÑñ]/g) || []).length;

    if (soloNumeros) {
      msgNombre.textContent = "El nombre no puede ser solo números ✖";
      msgNombre.className = "msg error";
      return false;
    }

    if (mezclaNumerosSimbolos && letras === 0) {
      msgNombre.textContent = "Debe incluir letras además de números o símbolos ✖";
      msgNombre.className = "msg error";
      return false;
    }

    if (letras > 0 && letras < 3) {
      msgNombre.textContent = "Debe contener al menos 3 letras válidas ✖";
      msgNombre.className = "msg error";
      return false;
    }

    if (sinEspacios.length < 3 || sinEspacios.length > 20) {
      msgNombre.textContent = "Debe tener entre 3 y 20 caracteres válidos ✖";
      msgNombre.className = "msg error";
      return false;
    }

    if (tieneTresIguales(lower)) {
      msgNombre.textContent = "No puede tener tres letras seguidas iguales ✖";
      msgNombre.className = "msg error";
      return false;
    }

    if (!/^[A-Za-z0-9 +=ÁÉÍÓÚáéíóúÑñ]+( [A-Za-z0-9 +=ÁÉÍÓÚáéíóúÑñ]+)*$/.test(valor)) {
      msgNombre.textContent = "Solo letras, números, espacios y + = ✖";
      msgNombre.className = "msg error";
      return false;
    }

    msgNombre.textContent = "Campo válido ✔";
    msgNombre.className = "msg ok";
    return true;
  }

  function validarDescripcionReceta() {
    const valor = descripcion.value;
    const sinEspacios = valor.replace(/\s+/g, "");

    if (!msgDescripcion) return true;

    if (/^[ \n]/.test(valor)) {
      msgDescripcion.textContent = "No puede iniciar con espacio o salto de línea ✖";
      msgDescripcion.className = "msg error";
      return false;
    }

    if (/ {2,}/.test(valor)) {
      msgDescripcion.textContent = "No puede tener múltiples espacios ✖";
      msgDescripcion.className = "msg error";
      return false;
    }

    const lineas = valor.split("\n");
    for (let i = 0; i < lineas.length; i++) {
      const linea = lineas[i].trim();
      if (linea === "") {
        msgDescripcion.textContent = "No se permiten saltos de línea vacíos ✖";
        msgDescripcion.className = "msg error";
        return false;
      }
      if (linea.replace(/\s+/g, "").length < 3) {
        msgDescripcion.textContent = "Cada línea debe tener al menos 3 caracteres ✖ (línea " + (i + 1) + ")";
        msgDescripcion.className = "msg error";
        return false;
      }
      if (tieneTresIguales(linea)) {
        msgDescripcion.textContent = "No 3 iguales seguidos ✖ (línea " + (i + 1) + ")";
        msgDescripcion.className = "msg error";
        return false;
      }
      if (!/^[A-Za-z0-9 +=:,().ÁÉÍÓÚáéíóúÑñ]+$/.test(linea)) {
        msgDescripcion.textContent = "Caracteres no permitidos ✖ (línea " + (i + 1) + ")";
        msgDescripcion.className = "msg error";
        return false;
      }
    }

    if (sinEspacios.length < 3 || sinEspacios.length > 200) {
      msgDescripcion.textContent = "Debe tener entre 3 y 200 caracteres válidos ✖";
      msgDescripcion.className = "msg error";
      return false;
    }

    msgDescripcion.textContent = "Campo válido ✔";
    msgDescripcion.className = "msg ok";
    return true;
  }

  function actualizarBotonReceta() {
    if (!guardarBtn) return;
    guardarBtn.disabled = !(validarNombreReceta() && validarDescripcionReceta());
  }

  nombre.addEventListener("input", function (e) {
    sanitizeSpaces(e.target);
    validarNombreReceta();
    actualizarBotonReceta();
  });

  descripcion.addEventListener("input", function (e) {
    sanitizeSpaces(e.target);
    validarDescripcionReceta();
    actualizarBotonReceta();
  });

  function actualizarLista() {
    if (!listaInsumosDiv || !insumosJsonInput) return;

    listaInsumosDiv.innerHTML = "";
    insumosSeleccionados.forEach((item, i) => {
      listaInsumosDiv.innerHTML += "<p>" + (i + 1) + ". " + item.nombre_insumo + " - " + item.cantidad + " " + item.nombre_unidad + "</p>";
    });
    insumosJsonInput.value = JSON.stringify(insumosSeleccionados);
    if (listaInsumosDiv.style.display === "") {
      listaInsumosDiv.style.display = "none";
    }
  }

  function agregarInsumo() {
    if (!selectInsumo || !selectUnidad || !inputCantidad) return;

    if (!selectInsumo.value || !inputCantidad.value || !selectUnidad.value) {
      alert("Por favor, completa todos los campos del insumo.");
      return;
    }
    if (!validarCantidadUsada(inputCantidad)) return;

    const tipoInsumo = selectInsumo.options[selectInsumo.selectedIndex] && selectInsumo.options[selectInsumo.selectedIndex].getAttribute("data-tipo");
    const tipoUnidad = selectUnidad.options[selectUnidad.selectedIndex] && selectUnidad.options[selectUnidad.selectedIndex].getAttribute("data-tipo");

    if (tipoInsumo && tipoUnidad && tipoInsumo !== tipoUnidad) {
      alert("⚠ No puedes asignar medidas erróneas.");
      return;
    }

    const nuevoInsumo = {
      id_insumo: selectInsumo.value,
      nombre_insumo: selectInsumo.options[selectInsumo.selectedIndex].text,
      cantidad: parseFloat(inputCantidad.value),
      id_unidad: selectUnidad.value,
      nombre_unidad: selectUnidad.options[selectUnidad.selectedIndex].text,
    };

    insumosSeleccionados.push(nuevoInsumo);
    actualizarLista();

    selectInsumo.value = "";
    inputCantidad.value = "";
    selectUnidad.value = "";
  }

  function toggleLista() {
    if (!listaInsumosDiv) return;
    if (listaInsumosDiv.style.display === "none" || listaInsumosDiv.style.display === "") {
      listaInsumosDiv.style.display = "block";
    } else {
      listaInsumosDiv.style.display = "none";
    }
  }

  if (typeof window.agregarInsumo !== "function") window.agregarInsumo = agregarInsumo;
  if (typeof window.toggleLista !== "function") window.toggleLista = toggleLista;

  actualizarBotonReceta();
}

function initValidacionesInsumo() {
  const ids = ["stock_total", "stock_minimo", "stock_maximo", "precio_base", "peso_individual"];
  const inputs = ids.map((id) => document.getElementById(id)).filter(Boolean);

  if (inputs.length === 0) return;

  function limpiarNumero(input) {
    let valor = input.value || "";
    valor = valor.replace(/[^0-9.]/g, "");
    const partes = valor.split(".");
    if (partes.length > 2) valor = partes[0] + "." + partes.slice(1).join("");
    input.value = valor;
  }

  function actualizarBotones(estadoDeshabilitado) {
    const botones = document.querySelectorAll("form .btn.btn-primary[type='submit'], form .btn.btn-success[type='submit']");
    botones.forEach((b) => (b.disabled = estadoDeshabilitado));
  }

  function evaluar() {
    const stockTotal = parseFloat((document.getElementById("stock_total") && document.getElementById("stock_total").value) || 0);
    const stockMinimo = parseFloat((document.getElementById("stock_minimo") && document.getElementById("stock_minimo").value) || 0);
    const stockMaximo = parseFloat((document.getElementById("stock_maximo") && document.getElementById("stock_maximo").value) || 0);
    const precioBase = parseFloat((document.getElementById("precio_base") && document.getElementById("precio_base").value) || 0);
    const pesoIndividual = parseFloat((document.getElementById("peso_individual") && document.getElementById("peso_individual").value) || 0);

    const errores = { stock_total: "", stock_minimo: "", stock_maximo: "", precio_base: "", peso_individual: "" };

    if (stockMinimo <= 0) errores.stock_minimo = "El stock mínimo no puede ser 0 o negativo.";
    if (stockMaximo <= 0) errores.stock_maximo = "El stock máximo no puede ser 0 o negativo.";
    if (precioBase <= 0) errores.precio_base = "El precio base no puede ser 0 o negativo.";
    if (pesoIndividual <= 0) errores.peso_individual = "El peso individual no puede ser 0 o negativo.";

    if (stockMinimo > stockMaximo) {
      const msg = "El stock mínimo no puede ser mayor al stock máximo.";
      errores.stock_minimo = msg;
      errores.stock_maximo = msg;
    }
    if(stockMinimo==stockMaximo){
      const msg = "El stock mínimo no puede ser igual al stock máximo.";
      errores.stock_minimo = msg;
      errores.stock_maximo = msg;

    }

    if (stockTotal > stockMaximo) {
      const msg = "El stock total no puede ser mayor al stock máximo.";
      errores.stock_total = msg;
      if (!errores.stock_maximo) errores.stock_maximo = msg;
    }

    let hayError = false;

    Object.entries(errores).forEach(([id, mensaje]) => {
      const input = document.getElementById(id);
      if (!input) return;

      mostrarMensaje(input, mensaje || "Válido ✔", mensaje === "");
      if (mensaje) {
        hayError = true;
        input.classList.add("is-invalid");
      } else {
        input.classList.remove("is-invalid");
      }
    });

    actualizarBotones(hayError);
  }

  inputs.forEach((input) => {
    input.addEventListener("input", function () {
      limpiarNumero(input);
      evaluar();
    });
  });

  evaluar();
}

function initValidacionTipoCategoriaUnidadInsumo() {
  const path = window.location.pathname || "";
  if (!path.includes("/admin/insumo")) return;

  const categoriaSel =
    document.getElementById("ID_Categoria") ||
    document.querySelector('select[name="ID_Categoria"]') ||
    document.querySelector('select[name="categoria_id"]');

  const unidadSel =
    document.getElementById("ID_Unidad") ||
    document.querySelector('select[name="ID_Unidad"]');

  if (!categoriaSel || !unidadSel) return;

  const form = unidadSel.closest("form") || categoriaSel.closest("form") || null;

  ensureMsgElem(unidadSel);

  function joinUrl(base, tail) {
    if (!base) return tail;
    if (base.endsWith("/") && tail.startsWith("/")) return base + tail.slice(1);
    if (!base.endsWith("/") && !tail.startsWith("/")) return base + "/" + tail;
    return base + tail;
  }

  function resolverTipoUrl() {
    const a1 = categoriaSel.getAttribute("data-tipo-url");
    const a2 = unidadSel.getAttribute("data-tipo-url");
    if (a1) return a1;
    if (a2) return a2;

    const any = document.querySelector("[data-tipo-url]");
    if (any) {
      const u = any.getAttribute("data-tipo-url");
      if (u) return u;
    }

    const base = path.replace(/\/(edit|new|create)\/?$/, "/");
    if (base && base !== path) return joinUrl(base, "tipo_lookup/");
    return joinUrl(path.endsWith("/") ? path : path + "/", "tipo_lookup/");
  }

  const tipoUrl = resolverTipoUrl();

  function nombreTipo(t) {
    if (t === 1) return "sólido";
    if (t === 2) return "líquido";
    if (t === 3) return "medición";
    return "desconocido";
  }

  function tipoDeSelect(sel) {
    const opt = sel.options && sel.selectedIndex >= 0 ? sel.options[sel.selectedIndex] : null;
    const t = opt ? (opt.getAttribute("data-tipo") || (opt.dataset ? opt.dataset.tipo : null)) : null;
    const n = parseInt(String(t || ""), 10);
    return isNaN(n) ? null : n;
  }

  async function obtenerTipos(catId, uniId) {
    if (!tipoUrl) return null;

    const url = new URL(tipoUrl, window.location.origin);
    url.searchParams.set("categoria_id", String(catId));
    url.searchParams.set("unidad_id", String(uniId));

    const res = await fetch(url.toString(), {
      headers: { "X-Requested-With": "XMLHttpRequest" },
      credentials: "same-origin",
    });

    let data = null;
    try { data = await res.json(); } catch (e) {}

    if (!res.ok) {
      throw new Error(data && data.error ? data.error : "Error al consultar tipos");
    }
    return data;
  }

  let token = 0;

  async function validar(modo) {
    const myToken = ++token;

    const catVal = String(categoriaSel.value || "");
    const uniVal = String(unidadSel.value || "");

    if (!catVal || !uniVal) {
      mostrarMensaje(unidadSel, "", true);
      activarBotonEnFormulario(form);
      return true;
    }

    let tCat = null;
    let tUni = null;

    if (tipoUrl) {
      try {
        const data = await obtenerTipos(catVal, uniVal);
        if (myToken !== token) return false;

        if (data && data.categoria_tipo != null) tCat = parseInt(data.categoria_tipo, 10);
        if (data && data.unidad_tipo != null) tUni = parseInt(data.unidad_tipo, 10);
      } catch (e) {
        if (myToken !== token) return false;
        if (modo === "submit" || modo === "change") {
          mostrarMensaje(unidadSel, `No se pudo validar: ${String(e.message || e)}`, false);
          activarBotonEnFormulario(form);
        } else {
          mostrarMensaje(unidadSel, "", true);
          activarBotonEnFormulario(form);
        }
        return false;
      }
    }

    if (tCat == null) tCat = tipoDeSelect(categoriaSel);
    if (tUni == null) tUni = tipoDeSelect(unidadSel);

    if (tCat == null || tUni == null) {
      if (modo === "submit" || modo === "change") {
        mostrarMensaje(unidadSel, "No se pudo validar: no se encontraron tipos.", false);
      } else {
        mostrarMensaje(unidadSel, "", true);
      }
      activarBotonEnFormulario(form);
      return modo === "init";
    }

    if (tCat !== tUni) {
      mostrarMensaje(
        unidadSel,
        `Verifique que la categoría y la unidad sean del mismo estado, no se puede ${nombreTipo(tCat)} (categoría) con ${nombreTipo(tUni)} (unidad).`,
        false
      );
      activarBotonEnFormulario(form);
      return false;
    }

    mostrarMensaje(unidadSel, "Categoría y unidad compatibles ✔", true);
    activarBotonEnFormulario(form);
    return true;
  }

  categoriaSel.addEventListener("change", function () { validar("change"); });
  unidadSel.addEventListener("change", function () { validar("change"); });

  if (form) {
    form.addEventListener("submit", function (e) {
      if (form.dataset.tipoValidado === "1") {
        delete form.dataset.tipoValidado;
        return;
      }

      e.preventDefault();

      validar("submit").then((ok) => {
        if (!ok) {
          try { unidadSel.focus(); } catch (e2) {}
          return;
        }
        form.dataset.tipoValidado = "1";
        if (typeof form.requestSubmit === "function") form.requestSubmit();
        else form.submit();
      });
    });
  }

  validar("init");
}


document.addEventListener("DOMContentLoaded", initValidacionTipoCategoriaUnidadInsumo);
document.addEventListener("DOMContentLoaded", conectarValidacionesGenerales);
document.addEventListener("DOMContentLoaded", initValidacionDocumentoEmpleado);
document.addEventListener("DOMContentLoaded", initValidacionesOrdenEntrega);
document.addEventListener("DOMContentLoaded", initNumeroCAIAdmin);
document.addEventListener("DOMContentLoaded", validarRangosCAI);
document.addEventListener("DOMContentLoaded", validarFechasCAI);
document.addEventListener("DOMContentLoaded", validarSecuenciaCAI);
document.addEventListener("DOMContentLoaded", initRecetaValidaciones);
document.addEventListener("DOMContentLoaded", initValidacionesInsumo);
