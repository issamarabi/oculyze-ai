window.onload = function() {
    const form = document.getElementById('studyInputForm');
    
    form.onchange = function(e) {
        const participants = document.getElementById('participants').value;
        const websites = document.getElementById('websites').value;
        const tasksPerWebsite = document.getElementById('tasksPerWebsite').value;

        let dynamicInputs = document.getElementById('dynamicInputs');
        dynamicInputs.innerHTML = '';  // Clear any existing content

        let websiteInputs = document.getElementById('websiteInputs');
        websiteInputs.innerHTML = '';  // Clear any existing content

        let taskInputs = document.getElementById('taskInputs');
        taskInputs.innerHTML = '';  // Clear any existing content

        for (let i = 1; i <= websites; i++) {
            websiteInputs.innerHTML += `<h3>Website ${i}</h3>`;
            websiteInputs.innerHTML += `<input type='text' name='websiteName_${i}' placeholder='Website Name' required>`;
        }

        for (let i = 1; i <= tasksPerWebsite; i++) {
            taskInputs.innerHTML += `<h4> Task ${i}</h4>`;
            taskInputs.innerHTML += `<input type='text' name='taskDesc_${i}' placeholder='Task Description' required>`;
        }

        for (let i = 1; i <= participants; i++) {
            dynamicInputs.innerHTML += `<h2>Participant ${i}</h2>`;
            for (let j = 1; j <= websites; j++) {
                dynamicInputs.innerHTML += `<h3>Website ${j}</h3>`;
                dynamicInputs.innerHTML += `<label>Think Aloud for Website ${j}:</label>`;
                dynamicInputs.innerHTML += `<input type='file' name='thinkAloud_${i}_${j}' accept='audio/*'><br>`;

                for (let k = 1; k <= tasksPerWebsite; k++) {
                    dynamicInputs.innerHTML += `<h4>Task ${k}</h4>`;
                    dynamicInputs.innerHTML += `<label>Eye + Click Tracking Data for Task ${k}:</label>`;
                    dynamicInputs.innerHTML += `<input type='file' name='eyeClickData_${i}_${j}_${k}' accept='.tsv'><br>`;
                    dynamicInputs.innerHTML += `<label>Browser Log for Task ${k}:</label>`;
                    dynamicInputs.innerHTML += `<input type='file' name='browserLog_${i}_${j}_${k}' accept='.txt'><br>`;
                }
            }
        }
    };
};
