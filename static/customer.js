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
                <td>${c.id}</td>
                <td>${c.c_name}</td>
                <td>${c.c_type}</td>
                <td>${c.c_name}</td>
                <td>${c.c_mail}</td>
                <td>${c.c_phone}</td>
                <td class="action-col">
                    <button class="btn-edit" data-id="${c.id}">Edit</button>
                    <button class="btn-delete" data-id="${c.id}">Delete</button>
                </td>
            </tr>
        `;
    });
}
})
}

