const form = document.querySelector("#employee-form");
const list = document.querySelector("#employee-list");
const message = document.querySelector("#message");
const count = document.querySelector("#count");
const emptyState = document.querySelector("#empty-state");
const formTitle = document.querySelector("#form-title");
const submitBtn = document.querySelector("#submit-btn");
const cancelBtn = document.querySelector("#cancel-btn");

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options
  });
  if (!response.ok) {
    let detail = "Une erreur est survenue.";
    try { detail = (await response.json()).detail || detail; } catch (_) {}
    throw new Error(detail);
  }
  if (response.status === 204) return null;
  return response.json();
}

function showMessage(text, isError = false) {
  message.textContent = text;
  message.classList.toggle("error", isError);
}

function resetForm() {
  form.reset();
  document.querySelector("#employee-id").value = "";
  formTitle.textContent = "Ajouter un employé";
  submitBtn.textContent = "Enregistrer";
  cancelBtn.classList.add("hidden");
}

function addCell(row, text) {
  const cell = document.createElement("td");
  cell.textContent = text ?? "";
  row.appendChild(cell);
  return cell;
}

function renderEmployees(employees) {
  list.replaceChildren();
  count.textContent = employees.length;
  emptyState.classList.toggle("hidden", employees.length > 0);

  for (const employee of employees) {
    const row = document.createElement("tr");
    const identity = document.createElement("td");
    const name = document.createElement("strong");
    name.textContent = employee.full_name;
    const email = document.createElement("span");
    email.className = "email";
    email.textContent = employee.email;
    identity.append(name, email);
    row.appendChild(identity);
    addCell(row, employee.department);
    addCell(row, employee.job_title);

    const actions = document.createElement("td");
    const edit = document.createElement("button");
    edit.className = "edit";
    edit.textContent = "Modifier";
    edit.addEventListener("click", () => startEdit(employee));
    const remove = document.createElement("button");
    remove.className = "danger";
    remove.textContent = "Supprimer";
    remove.addEventListener("click", () => removeEmployee(employee));
    actions.append(edit, remove);
    row.appendChild(actions);
    list.appendChild(row);
  }
}

async function loadEmployees() {
  try {
    renderEmployees(await api("/api/employees"));
  } catch (error) {
    showMessage(error.message, true);
  }
}

function startEdit(employee) {
  document.querySelector("#employee-id").value = employee.id;
  for (const field of ["full_name", "email", "department", "job_title"]) {
    document.querySelector(`#${field}`).value = employee[field];
  }
  formTitle.textContent = "Modifier un employé";
  submitBtn.textContent = "Enregistrer les modifications";
  cancelBtn.classList.remove("hidden");
  showMessage("");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

async function removeEmployee(employee) {
  if (!window.confirm(`Supprimer l'employé « ${employee.full_name} » ?`)) return;
  try {
    await api(`/api/employees/${employee.id}`, { method: "DELETE" });
    showMessage("Employé supprimé.");
    await loadEmployees();
  } catch (error) {
    showMessage(error.message, true);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const id = document.querySelector("#employee-id").value;
  const data = Object.fromEntries(new FormData(form).entries());
  delete data[""];
  try {
    await api(id ? `/api/employees/${id}` : "/api/employees", {
      method: id ? "PUT" : "POST",
      body: JSON.stringify(data)
    });
    showMessage(id ? "Employé modifié avec succès." : "Employé ajouté avec succès.");
    resetForm();
    await loadEmployees();
  } catch (error) {
    showMessage(error.message, true);
  }
});

cancelBtn.addEventListener("click", resetForm);
document.querySelector("#refresh-btn").addEventListener("click", loadEmployees);
loadEmployees();
