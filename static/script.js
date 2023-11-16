window.onload = function() {
    const form = document.getElementById('studyInputForm');
    const participantsInput = document.getElementById('participants');
    const websitesInput = document.getElementById('websites');
    const tasksPerWebsiteInput = document.getElementById('tasksPerWebsite');
    const websiteAndTaskInputs = document.getElementById('websiteAndTaskInputs');
    const participantInputs = document.getElementById('participantInputs');

    function updateWebsiteAndTaskInputs() {
        const websites = websitesInput.value;
        const tasksPerWebsite = tasksPerWebsiteInput.value;

        websiteAndTaskInputs.innerHTML = '';

        for (let j = 1; j <= websites; j++) {
            websiteAndTaskInputs.innerHTML += `<h3>Website ${j}</h3>`;
            websiteAndTaskInputs.innerHTML += `<input type='text' name='websiteName_${j}' placeholder='Website Name' required>`;
            websiteAndTaskInputs.innerHTML += `<input type='file' name='screenshot_${j}' accept='image/*'><br>`;

            for (let k = 1; k <= tasksPerWebsite; k++) {
                websiteAndTaskInputs.innerHTML += `<h4>Task ${k}</h4>`;
                websiteAndTaskInputs.innerHTML += `<input type='text' name='taskDesc_${j}_${k}' placeholder='Task Description' required><br>`;
            }
        }
    }

    function updateParticipantInputs() {
        const participants = participantsInput.value;
        const websites = websitesInput.value;
        const tasksPerWebsite = tasksPerWebsiteInput.value;

        participantInputs.innerHTML = '';

        for (let i = 1; i <= participants; i++) {
            participantInputs.innerHTML += `<h3>Participant ${i}</h3>`;
            for (let j = 1; j <= websites; j++) {
                for (let k = 1; k <= tasksPerWebsite; k++) {
                    participantInputs.innerHTML += `<input type='file' name='thinkAloud_${i}_${j}_${k}' accept='audio/*' placeholder='Think Aloud for Website ${j}, Task ${k}'>`;
                    participantInputs.innerHTML += `<input type='file' name='eyeClickData_${i}_${j}_${k}' accept='.tsv' placeholder='Eye+Click Data for Website ${j}, Task ${k}'>`;
                    participantInputs.innerHTML += `<input type='file' name='browserLog_${i}_${j}_${k}' accept='.txt' placeholder='Browser Log for Website ${j}, Task ${k}'><br>`;
                }
            }
        }
    }

    websitesInput.onchange = updateWebsiteAndTaskInputs;
    tasksPerWebsiteInput.onchange = updateWebsiteAndTaskInputs;
    participantsInput.onchange = updateParticipantInputs;
};
