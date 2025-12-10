function allowDrop(ev) { ev.preventDefault(); }
function drag(ev) { ev.dataTransfer.setData("text", ev.target.id); }
function drop(ev, newStatus) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var taskId = data.split('-')[1];
    document.getElementById('dd_task_id').value = taskId;
    document.getElementById('dd_status').value = newStatus;
    document.getElementById('updateStatusForm').submit();
}

function openManageTeamModal(teamId) {
    document.getElementById('add_member_team_id').value = teamId;
    const tbody = document.getElementById('team_members_table_body');
    tbody.innerHTML = '<tr><td colspan="3" class="text-center">Завантаження...</td></tr>';

    new bootstrap.Modal(document.getElementById('manageTeamModal')).show();

    fetch(`/team/members/${teamId}/`)
        .then(r => r.json())
        .then(data => {
            tbody.innerHTML = '';
            if (data.members.length === 0) {
                tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">Немає учасників</td></tr>';
            }
            data.members.forEach(m => {
                tbody.innerHTML += `
                    <tr>
                        <td>${m.name} ${m.surname}</td>
                        <td>${m.role}</td>
                        <td class="text-center">
                            <form action="/team/remove_member/" method="POST" style="display:inline;">
                                <input type="hidden" name="csrfmiddlewaretoken" value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">
                                <input type="hidden" name="team_id" value="${teamId}">
                                <input type="hidden" name="client_id" value="${m.id}">
                                <button class="btn btn-sm btn-outline-danger py-0 px-1"><i class="bi bi-x"></i></button>
                            </form>
                        </td>
                    </tr>
                `;
            });
        });
}


function openManageProjectModal(projectId) {
    document.getElementById('add_team_project_id').value = projectId;
    const tbody = document.getElementById('project_teams_table_body');
    const titleEl = document.getElementById('manageProjectTitle');
    tbody.innerHTML = '<tr><td colspan="2" class="text-center">Завантаження...</td></tr>';

    new bootstrap.Modal(document.getElementById('manageProjectModal')).show();

    fetch(`/project/details/${projectId}/`)
        .then(r => r.json())
        .then(data => {
            titleEl.innerText = `Управління проектом: ${data.title}`;
            tbody.innerHTML = '';
            if (data.teams.length === 0) {
                tbody.innerHTML = '<tr><td colspan="2" class="text-center text-muted">Немає прикріплених команд</td></tr>';
            }
            data.teams.forEach(t => {
                tbody.innerHTML += `
                    <tr>
                        <td>${t.title}</td>
                        <td class="text-center">
                            <form action="/project/remove_team/" method="POST" style="display:inline;">
                                <input type="hidden" name="csrfmiddlewaretoken" value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">
                                <input type="hidden" name="project_id" value="${projectId}">
                                <input type="hidden" name="team_id" value="${t.id}">
                                <button class="btn btn-sm btn-outline-danger py-0 px-1"><i class="bi bi-x"></i></button>
                            </form>
                        </td>
                    </tr>
                `;
            });
        });
}

function confirmDeleteProject(projectId) {
    fetch(`/project/details/${projectId}/`)
        .then(r => r.json())
        .then(data => {
            let msg = `Видалити проект "${data.title}"?`;
            if (data.task_count > 0) {
                msg += `\n\nУВАГА: Цей проект містить ${data.task_count} завдань! Всі вони будуть видалені.`;
            }
            if (confirm(msg)) {
                document.getElementById('delete_proj_id').value = projectId;
                document.getElementById('deleteProjectForm').submit();
            }
        });
}

function openEditModal(id, title, desc, prio, date) {
    const modal = document.getElementById('editTaskModal');
    if (!modal) return;
    document.getElementById('edit_task_id').value = id;
    document.getElementById('edit_title').value = title;
    document.getElementById('edit_description').value = desc;
    document.getElementById('edit_priority').value = prio;
    document.getElementById('edit_deadline').value = date;
    new bootstrap.Modal(modal).show();
}

function openEditEventModal(id, theme, desc, priority, date, duration, link) {
    const modal = document.getElementById('editEventModal');
    if (!modal) return;
    document.getElementById('edit_event_id').value = id;
    document.getElementById('edit_event_theme').value = theme;
    document.getElementById('edit_event_description').value = desc;
    document.getElementById('edit_event_priority').value = priority;
    document.getElementById('edit_event_date').value = date;
    document.getElementById('edit_event_duration').value = duration;
    document.getElementById('edit_event_link').value = link;
    new bootstrap.Modal(modal).show();
}

function openEventParticipantsModal(eventId) {
    const modal = document.getElementById('eventParticipantsModal');
    if (!modal) return;
    document.getElementById('current_event_id').value = eventId;
    const addInput = document.getElementById('add_part_event_id');
    if(addInput) addInput.value = eventId;

    fetch(`/event/participants/${eventId}/`)
        .then(r => r.json())
        .then(data => {
            const list = document.getElementById('participants_list');
            list.innerHTML = '';
            if (data.participants.length === 0) {
                list.innerHTML = '<small class="text-muted">Немає учасників</small>';
            } else {
                data.participants.forEach(p => {
                    list.innerHTML += `
                        <div class="d-flex justify-content-between align-items-center mb-2 p-2 border rounded bg-light">
                            <span>${p.name} ${p.surname}</span>
                            <form action="/event/remove_participant/" method="POST" style="display:inline;">
                                <input type="hidden" name="csrfmiddlewaretoken" value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">
                                <input type="hidden" name="event_id" value="${eventId}">
                                <input type="hidden" name="client_id" value="${p.id}">
                                <button class="btn btn-sm btn-outline-danger" title="Видалити"><i class="bi bi-x"></i></button>
                            </form>
                        </div>
                    `;
                });
            }
        });
    new bootstrap.Modal(modal).show();
}

function openSubmitModal(id) {
    document.getElementById('submit_task_id').value = id;
    new bootstrap.Modal(document.getElementById('submitResultModal')).show();
}
function openSubmitUTModal(id) {
    document.getElementById('submit_ut_id').value = id;
    new bootstrap.Modal(document.getElementById('submitUTModal')).show();
}
function openAddExecModal(id) {
    document.getElementById('exec_task_id').value = id;
    new bootstrap.Modal(document.getElementById('addExecutorModal')).show();
}
function openUnderTaskModal(id) {
    document.getElementById('ut_parent_id').value = id;
    new bootstrap.Modal(document.getElementById('createUnderTaskModal')).show();
}
function openChangeRoleModal(userId, currentRole) {
    document.getElementById('change_role_user_id').value = userId;
    document.getElementById('change_role_select').value = currentRole;
    new bootstrap.Modal(document.getElementById('changeRoleModal')).show();
}
function toggleTaskDetails(taskId) {
    const details = document.getElementById('task-details-' + taskId);
    if (details) details.classList.toggle('d-none');
}
function applyFilters() {
    const project = document.getElementById('filter_project').value;
    const priority = document.getElementById('filter_priority').value;
    const deadline = document.getElementById('filter_deadline').value;
    const status = document.getElementById('filter_status').value;
    const url = new URL(window.location.href);
    if (project) url.searchParams.set('project', project); else url.searchParams.delete('project');
    if (priority) url.searchParams.set('priority', priority); else url.searchParams.delete('priority');
    if (deadline) url.searchParams.set('deadline', deadline); else url.searchParams.delete('deadline');
    if (status) url.searchParams.set('status', status); else url.searchParams.delete('status');
    window.location.href = url.toString();
}
function clearFilters() {
    window.location.href = window.location.pathname;
}