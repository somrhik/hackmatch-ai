async function addUser() {
    const name = document.getElementById("name").value;
    const skills = document.getElementById("skills").value.split(",");
    const experience = document.getElementById("experience").value;
    const role = document.getElementById("role").value;

    const response = await fetch("/add-user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name: name,
            skills: skills,
            experience_level: experience,
            preferred_role: role
        })
    });

    const result = await response.json();
    document.getElementById("statusMessage").innerText = result.message;
}

async function formTeams() {
    const response = await fetch("/form-teams");
    const data = await response.json();

    const container = document.getElementById("teamResult");
    container.innerHTML = "";

    if (data.message) {
        container.innerHTML = `<p>${data.message}</p>`;
        return;
    }

    Object.keys(data).forEach(team => {
        const teamDiv = document.createElement("div");
        teamDiv.className = "team-card";

        teamDiv.innerHTML = `
            <h3>${team}</h3>
            <div class="team-members">${data[team].join(", ")}</div>
        `;

        container.appendChild(teamDiv);
    });
}