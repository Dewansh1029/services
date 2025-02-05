let currentStep = 1;
const totalSteps = 3;

function showStep(step) {
    // Hide all steps
    const steps = document.querySelectorAll(".step");
    steps.forEach(stepElement => stepElement.style.display = "none");

    // Show the current step
    const currentStepElement = document.getElementById(`step${step}`);
    currentStepElement.style.display = "block";

    // Update navigation buttons
    document.getElementById("prevStep").disabled = step === 1;
    document.getElementById("nextStep").disabled = step === totalSteps;
}

function nextStep() {
    if (currentStep < totalSteps) {
        currentStep++;
        showStep(currentStep);
    }
}

function prevStep() {
    if (currentStep > 1) {
        currentStep--;
        showStep(currentStep);
    }
}

function getLeadDetail() {
    const leadId = document.getElementById("getLeadId").value;

    if (!leadId) {
        alert("Please enter a Lead ID.");
        return;
    }

    fetch(`/getlead/${leadId}`)
        .then(response => response.json())
        .then(data => {
            if (data.contacts && data.contacts[0]) {
                const lead = data.contacts[0];
                document.getElementById("leadStatus").innerText = lead.status;
                document.getElementById("leadName").innerText = lead.name;
                document.getElementById("leadEmail").innerText = lead.email;
                document.getElementById("leadPhone").innerText = lead.phone;
                document.getElementById("leadRequirements").innerText = lead.requirement;
                document.getElementById("leadLastCall").innerText = lead["last Call"];

                document.getElementById("leadDetailResult").style.display = "block";
            } else {
                alert("Lead not found.");
            }
        })
        .catch(error => {
            alert("Error fetching lead details: " + error);
        });
}

// Function to submit the Add Lead form and get the Lead ID
function submitLeadForm() {
    const leadName = document.getElementById("lead_name").value;
    const leadEmail = document.getElementById("lead_email").value;
    const leadPhone = document.getElementById("lead_phone").value;
    const leadStatus = document.getElementById("lead_status").value;
    const leadRequirements = document.getElementById("lead_requirements").value;
    const leadCallFrequency = document.getElementById("lead_call_frequency").value;
    const leadLastCalled = document.getElementById("lead_last_called").value;

    if (!leadName || !leadEmail || !leadPhone || !leadStatus || !leadRequirements || !leadCallFrequency || !leadLastCalled) {
        alert("Please fill out all fields.");
        return;
    }

    // Prepare the form data
    const leadData = {
        name: leadName,
        email: leadEmail,
        phone: leadPhone,
        status: leadStatus,
        requirements: leadRequirements,
        call_frequency: leadCallFrequency,
        last_called: leadLastCalled
    };

    // Make the API request to add a new lead
    fetch('/leads/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(leadData)
    })
    .then(response => response.json())
    .then(data => {
        if (data && data.lead_id) {
            // Show the generated lead_id in the popup
            document.getElementById("generatedLeadId").innerText = data.lead_id;
            document.getElementById("leadIdPopup").style.display = "block";
        } else {
            alert("Error: Could not generate Lead ID.");
        }
    })
    .catch(error => {
        alert("Error submitting lead data: " + error);
    });
}

// Close the Lead ID Popup
function closeLeadIdPopup() {
    document.getElementById("leadIdPopup").style.display = "none";
}

// Initialize the stepper
document.addEventListener("DOMContentLoaded", () => {
    showStep(currentStep);
});
