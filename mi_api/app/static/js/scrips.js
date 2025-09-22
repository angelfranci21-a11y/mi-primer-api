document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/estudiantes")
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById("estudiantes-list");
            lista.innerHTML = "";

            if (data.length === 0) {
                lista.innerHTML = "<li>No hay estudiantes.</li>";
                return;
            }

            data.forEach(est => {
                const item = document.createElement("li");
                item.textContent = `${est.carnet} - ${est.nombre} (${est.grado}) - Edad: ${est.edad}`;
                lista.appendChild(item);
            });
        })
        .catch(error => {
            console.error("Error al obtener estudiantes:", error);
        });
});
