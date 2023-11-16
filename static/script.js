window.onload = function() {
    const form = document.getElementById('studyInputForm');
    const websiteInputs = document.getElementById('websiteInputs');
    const taskInputs = document.getElementById('taskInputs');
    const participantInputs = document.getElementById('participantInputs');

    form.onchange = function(e) {
        const participants = document.getElementById('participants').value;
        const websites = document.getElementById('websites').value;
        const tasksPerWebsite = document.getElementById('tasksPerWebsite').value;

        // Clear existing inputs
        websiteInputs.innerHTML = '';
        taskInputs.innerHTML = '';
        participantInputs.innerHTML = '';

        // Create inputs for website names and screenshots
        for (let j = 1; j <= websites; j++) {
            websiteInputs.innerHTML += `<h3>Website ${j}</h3>`;
            websiteInputs.innerHTML += `<input type='text' name='websiteName_${j}' placeholder='Website Name' required>`;
            websiteInputs.innerHTML += `<input type='file' name='screenshot_${j}' accept='image/*'><br>`;
        }

        // Create inputs for task descriptions
        for (let k = 1; k <= tasksPerWebsite; k++) {
            taskInputs.innerHTML += `<h4>Task ${k}</h4>`;
            taskInputs.innerHTML += `<input type='text' name='taskDesc_${k}' placeholder='Task Description' required><br>`;
        }

        // Create inputs for each participant's files
        for (let i = 1; i <= participants; i++) {
            participantInputs.innerHTML += `<h2>Participant ${i}</h2>`;
            for (let j = 1; j <= websites; j++) {
                participantInputs.innerHTML += `<h3>Website ${j}</h3>`;
                for (let k = 1; k <= tasksPerWebsite; k++) {
                    participantInputs.innerHTML += `<h4>Task ${k}</h4>`;
                    participantInputs.innerHTML += `<input type='file' name='thinkAloud_${i}_${j}_${k}' accept='audio/*'>`;
                    participantInputs.innerHTML += `<input type='file' name='eyeClickData_${i}_${j}_${k}' accept='.tsv'>`;
                    participantInputs.innerHTML += `<input type='file' name='browserLog_${i}_${j}_${k}' accept='.txt'><br>`;
                }
            }
        }
    };
};
