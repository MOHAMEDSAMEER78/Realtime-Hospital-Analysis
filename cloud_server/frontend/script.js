document.addEventListener('DOMContentLoaded', function() {
    // Close detail view handler
    document.getElementById('closeDetail').addEventListener('click', function() {
        document.getElementById('patientDetail').style.display = 'none';
    });
    // Care API interaction
    document.getElementById('fetchCareData').addEventListener('click', function() {
        fetch('/care/receive_fog_data/')
            .then(response => response.json())
            .then(data => {
                let html = '<table><tr><th>Timestamp</th><th>Temperature</th><th>Heart Rate</th><th>Oxygen Saturation</th></tr>';
                if (Array.isArray(data)) {
                    data.forEach(item => {
                        html += `<tr><td>${item.timestamp}</td><td>${item.temperature}</td><td>${item.heart_rate}</td><td>${item.oxygen_saturation}</td></tr>`;
                    });
                } else {
                    html += '<tr><td colspan="4">No data available</td></tr>';
                }
                html += '</table>';
                document.getElementById('careData').innerHTML = html;
            })
            .catch(error => {
                document.getElementById('careData').innerHTML =
                    `Error fetching care data: ${error.message}`;
            });
    });

    // Patient lists interaction
    document.getElementById('fetchAdmittedPatients').addEventListener('click', fetchAdmittedPatients);
    document.getElementById('fetchDischargedPatients').addEventListener('click', fetchDischargedPatients);

    // Load initial data
    fetchAdmittedPatients();
    fetchDischargedPatients();
});

function fetchAdmittedPatients() {
    fetch('/patients/in/')
        .then(response => response.json())
        .then(patients => {
            const html = patients.length > 0
                ? `<table>
                    <tr>
                        <th>Name</th>
                        <th>Admission Date</th>
                        <th>Room</th>
                    </tr>
                    ${patients.map(patient => `
                        <tr>
                            <td class="patient-name" data-patient-id="${patient.id}">${patient.name}</td>
                            <td>${new Date(patient.admission_date).toLocaleString()}</td>
                            <td>${patient.room_number || 'N/A'}</td>
                        </tr>
                    `).join('')}
                </table>`
                : '<p>No currently admitted patients</p>';
            document.getElementById('admittedPatients').innerHTML = html;
        })
        .catch(error => {
            document.getElementById('admittedPatients').innerHTML =
                `Error fetching admitted patients: ${error.message}`;
        });
}

// Handle patient name clicks
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('patient-name')) {
        const patientId = e.target.getAttribute('data-patient-id');
        fetchPatientDetails(patientId);
    }
});

function fetchPatientDetails(patientId) {
    fetch(`/patients/${patientId}/`)
        .then(response => response.json())
        .then(patient => {
            const detailContent = `
                <p><strong>Name:</strong> ${patient.name}</p>
                <p><strong>RFID Tag:</strong> ${patient.rfid_tag}</p>
                <p><strong>Date of Birth:</strong> ${new Date(patient.date_of_birth).toLocaleDateString()}</p>
                <p><strong>Admission Date:</strong> ${new Date(patient.admission_date).toLocaleString()}</p>
                ${patient.discharge_date ?
                    `<p><strong>Discharge Date:</strong> ${new Date(patient.discharge_date).toLocaleString()}</p>` : ''}
                <p><strong>Room Number:</strong> ${patient.room_number || 'N/A'}</p>
                ${patient.medical_history ?
                    `<p><strong>Medical History:</strong><br>${patient.medical_history}</p>` : ''}
            `;
            document.getElementById('detailContent').innerHTML = detailContent;
            document.getElementById('patientDetail').style.display = 'block';
        })
        .catch(error => {
            document.getElementById('detailContent').innerHTML =
                `Error fetching patient details: ${error.message}`;
            document.getElementById('patientDetail').style.display = 'block';
        });
}

function fetchDischargedPatients() {
    fetch('/patients/out/')
        .then(response => response.json())
        .then(patients => {
            const html = patients.length > 0
                ? `<table>
                    <tr>
                        <th>Name</th>
                        <th>Admission Date</th>
                        <th>Discharge Date</th>
                    </tr>
                    ${patients.map(patient => `
                        <tr>
                            <td>${patient.name}</td>
                            <td>${new Date(patient.admission_date).toLocaleDateString()}</td>
                            <td>${new Date(patient.discharge_date).toLocaleString()}</td>
                        </tr>
                    `).join('')}
                </table>`
                : '<p>No recently discharged patients</p>';
            document.getElementById('dischargedPatients').innerHTML = html;
        })
        .catch(error => {
            document.getElementById('dischargedPatients').innerHTML =
                `Error fetching discharged patients: ${error.message}`;
        });
}