/*To call load automatically when page loaded */
document.addEventListener("DOMContentLoaded",() => {
  load();
}

/* Load function to add data to the table */
function load(){
fetch("/api/customer")
  .then(r => r.json())
  .then(data => {
    const tbody = document.getElementById("customerTableBody");
    body.innerHTML = "";

tbody.innerHTML = "";

if (data.length === 0) {
    // show NOTHING when empty (as requested)
} else {
    data.forEach(c => {
        tbody.innerHTML += `
            <tr>
                <td>${c.company_id}</td>
                <td>${c.company_name}</td>
                <td>${c.company_type}</td>
                <td>${c.conatct_name}</td>
                <td>${c.cantact_mail}</td>
                <td>${c.contact_phone}</td>
                <td class="action-col">
                    <button class="btn-edit" data-id="${c.company_id}">Edit</button>
                    <button class="btn-delete" data-id="${c.company_id}">Delete</button>
                </td>
            </tr>
        `;
    });
}
})
}

