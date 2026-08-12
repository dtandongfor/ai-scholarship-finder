const API_BASE = window.INTELLIBLE_API_BASE || "http://127.0.0.1:8000";
const states = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"];
const form = document.querySelector("#profile-form");
const status = document.querySelector("#status");
const button = document.querySelector("#submit-button");
const resumeUpload = document.querySelector("#resume-upload");
const resumeButton = document.querySelector("#resume-prefill-button");
const resumeStatus = document.querySelector("#resume-status");
const deleteProfileButton = document.querySelector("#delete-profile-button");
const resetDemoButton = document.querySelector("#reset-demo-button");
const feedbackForm = document.querySelector("#feedback-form");
const feedbackStatus = document.querySelector("#feedback-status");
const stateSelect = form.elements.state;

states.forEach((state) => stateSelect.add(new Option(state, state)));

function profileFromForm() {
  const values = Object.fromEntries(new FormData(form));
  ["household_income", "sat_score", "act_score", "completed_credits", "volunteer_hours", "work_hours", "planned_term_credits"].forEach((key) => {
    values[key] = values[key] ? Number(values[key]) : null;
  });
  ["financial_aid_submitted", "pell_eligible", "disciplinary_good_standing", "demonstrated_financial_need", "accepts_service_commitment", "is_first_generation", "eligible_for_women_tech_scholarships", "can_seek_security_clearance"].forEach((key) => {
    values[key] = values[key] === "" ? null : values[key] === "true";
  });
  ["student_type", "enrollment_status"].forEach((key) => { if (!values[key]) values[key] = null; });
  if (!values.student_type && values.year.startsWith("College")) values.student_type = "current";
  if (!values.student_type && values.year === "High school senior") values.student_type = "first_year";
  return values;
}

function appendMatch(list, match, profile) {
  const template = document.querySelector("#match-template");
  const node = template.content.cloneNode(true);
  const scholarship = match.scholarship;
  node.querySelector(".provider").textContent = scholarship.provider;
  node.querySelector("h3").textContent = scholarship.name;
  node.querySelector(".score").textContent = `${match.match_status || match.match_level} · ${match.score}%`;
  node.querySelector(".amount").textContent = scholarship.amount || "Award amount varies";
  node.querySelector(".description").textContent = scholarship.description || scholarship.eligibility || "Review the official requirements before applying.";
  const reasons = node.querySelector(".reasons");
  const bullets = match.why_you_match?.length ? [...match.why_you_match] : [];
  (match.review_items || []).forEach((item) => bullets.push(`Confirm: ${item}`));
  const noSeparateApplication = scholarship.requirements?.application_required === false;
  const checklistLabel = noSeparateApplication ? "Required step" : "To apply";
  (match.application_checklist || []).forEach((item) => bullets.push(`${checklistLabel}: ${item}`));
  (match.selection_notes || []).forEach((item) => bullets.push(`Selection note: ${item}`));
  if (!bullets.length) bullets.push("Review the official requirements to confirm your fit.");
  const ul = document.createElement("ul");
  bullets.slice(0, 6).forEach((text) => { const li = document.createElement("li"); li.textContent = text; ul.append(li); });
  reasons.append(ul);
  const unassessed = node.querySelector(".unassessed-requirements");
  const officialDetails = match.unassessed_requirements || [];
  if (officialDetails.length) {
    unassessed.hidden = false;
    const label = document.createElement("strong");
    label.textContent = "Other official requirements to verify (not checked by your profile):";
    const details = document.createElement("p");
    details.textContent = officialDetails.join(" ");
    unassessed.append(label, details);
  }
  const link = node.querySelector(".apply-link");
  link.href = scholarship.application_url || scholarship.source_url;
  link.firstChild.textContent = scholarship.requirements?.application_link_label || "View official details and application steps ";
  const prepareButton = node.querySelector(".prepare-button");
  const prep = node.querySelector(".application-prep");
  if (noSeparateApplication) {
    prepareButton.hidden = true;
    const notice = node.querySelector(".no-application-note");
    notice.hidden = false;
    const heading = document.createElement("strong");
    heading.textContent = "No separate application needed";
    const details = document.createElement("p");
    details.textContent = scholarship.requirements?.no_application_message || "Review the official eligibility details and complete the listed required steps.";
    notice.append(heading, details);
  }
  prepareButton.addEventListener("click", () => {
    const profileDetails = [profile.name, profile.email, profile.university, profile.major, profile.gpa ? `GPA ${profile.gpa}` : ""]
      .filter(Boolean)
      .join(" · ");
    prep.replaceChildren();
    const heading = document.createElement("strong");
    heading.textContent = "Application prep";
    const details = document.createElement("p");
    details.textContent = `Review these details before opening the official application: ${profileDetails}. Complete the scholarship-specific items above. Intellible does not submit applications for you.`;
    prep.append(heading, details);
    prep.hidden = false;
    prepareButton.hidden = true;
  });
  list.append(node);
}

function renderMatches(matches, profile) {
  const lists = {
    inState: document.querySelector("#in-state-list"),
    transfer: document.querySelector("#transfer-list"),
    other: document.querySelector("#other-list"),
  };
  Object.values(lists).forEach((list) => list.replaceChildren());

  const groups = { inState: [], transfer: [], other: [] };
  matches.forEach((match) => {
    const scholarship = match.scholarship;
    const isInState = scholarship.state && scholarship.state.toLowerCase() === profile.state.toLowerCase();
    const isTransfer = scholarship.eligible_student_types
      ?.split(",")
      .map((type) => type.trim().toLowerCase())
      .includes("transfer");
    if (isInState) groups.inState.push(match);
    else if (isTransfer) groups.transfer.push(match);
    else groups.other.push(match);
  });

  Object.entries(groups).forEach(([name, group]) => {
    const section = document.querySelector(`#${name === "inState" ? "in-state" : name}-group`);
    section.hidden = group.length === 0;
    group.forEach((match) => appendMatch(lists[name], match, profile));
  });
  document.querySelector("#empty-results").hidden = matches.length !== 0;
  document.querySelector("#results").hidden = false;
  document.querySelector("#result-count").textContent = `${matches.length} eligible opportunities found`;
}

const exampleProfiles = {
  "first-year": { name: "Avery Demo", major: "Computer Science", gpa: "3.6", year: "High school senior", university: "Future university", state: "TX", citizenship: "US", interests: "robotics, volunteering, coding", student_type: "first_year", household_income: "62000", financial_aid_submitted: "true", pell_eligible: "true", enrollment_status: "full_time", demonstrated_financial_need: "true", is_first_generation: "true", skills: "Python, web development", leadership: "Robotics team captain" },
  transfer: { name: "Jordan Demo", major: "Psychology", gpa: "3.7", year: "College sophomore", university: "Santa Monica College", state: "CA", citizenship: "U.S. citizen", interests: "student leadership, tutoring", student_type: "transfer", completed_credits: "62", enrollment_status: "full_time", skills: "research, communication", leadership: "student council president" },
  tech: { name: "Riley Demo", major: "Computer Science", gpa: "3.4", year: "College sophomore", university: "Dallas College", state: "TX", citizenship: "U.S. citizen", interests: "coding, cybersecurity, tutoring", student_type: "current", enrollment_status: "full_time", financial_aid_submitted: "true", demonstrated_financial_need: "true", planned_term_credits: "12", completed_credits: "30", skills: "Python, web development", volunteer: "peer technology tutor" },
};

function loadExampleProfile(name) {
  const example = { ...exampleProfiles[name] };
  example.email = `demo-${name}-${Date.now()}@example.invalid`;
  form.reset();
  Object.entries(example).forEach(([field, value]) => {
    const input = form.elements[field];
    if (input) input.value = value;
  });
  localStorage.removeItem("scholarMatchStudentId");
  deleteProfileButton.hidden = true;
  status.textContent = "Example loaded. Finding matches...";
  form.requestSubmit();
}

document.querySelectorAll("[data-example]").forEach((button) => {
  button.addEventListener("click", () => loadExampleProfile(button.dataset.example));
});

resetDemoButton.addEventListener("click", async () => {
  const studentId = localStorage.getItem("scholarMatchStudentId");
  const email = form.elements.email.value;
  form.reset();
  localStorage.removeItem("scholarMatchStudentId");
  deleteProfileButton.hidden = true;
  document.querySelector("#results").hidden = true;
  if (studentId && email.endsWith("@example.invalid")) {
    try {
      await fetch(`${API_BASE}/students/${studentId}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email }),
      });
      status.textContent = "The fictional demo profile has been cleared.";
    } catch {
      status.textContent = "This browser's demo profile has been cleared.";
    }
    return;
  }
  status.textContent = "This browser's demo profile has been cleared.";
});

async function saveProfile(profile) {
  const existingId = localStorage.getItem("scholarMatchStudentId");
  const url = existingId ? `${API_BASE}/students/${existingId}` : `${API_BASE}/students/`;
  const response = await fetch(url, { method: existingId ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(profile) });
  if (!response.ok) throw new Error((await response.json()).detail || "We could not save your profile.");
  const student = await response.json();
  localStorage.setItem("scholarMatchStudentId", student.id);
  deleteProfileButton.hidden = false;
  return student;
}

if (localStorage.getItem("scholarMatchStudentId")) deleteProfileButton.hidden = false;

deleteProfileButton.addEventListener("click", async () => {
  const studentId = localStorage.getItem("scholarMatchStudentId");
  const email = window.prompt("To delete your saved profile, enter its email address.");
  if (!email || !studentId) return;
  try {
    const response = await fetch(`${API_BASE}/students/${studentId}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "We couldn't delete your profile.");
    localStorage.removeItem("scholarMatchStudentId");
    deleteProfileButton.hidden = true;
    document.querySelector("#results").hidden = true;
    status.textContent = "Your saved profile has been deleted.";
  } catch (error) {
    status.textContent = error.message.includes("fetch") ? "Start the local scholarship API, then try again." : error.message;
  }
});

resumeButton.addEventListener("click", async () => {
  const resume = resumeUpload.files[0];
  if (!resume) {
    resumeStatus.textContent = "Choose a PDF, Word document, or text resume first.";
    return;
  }
  resumeButton.disabled = true;
  resumeStatus.textContent = "Reading your resume...";
  try {
    const upload = new FormData();
    upload.append("resume", resume);
    const response = await fetch(`${API_BASE}/students/resume-preview`, { method: "POST", body: upload });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "We couldn't read that resume.");
    let filled = 0;
    Object.entries(data.suggestions || {}).forEach(([field, value]) => {
      const input = form.elements[field];
      if (input && !input.value && value) {
        input.value = value;
        filled += 1;
      }
    });
    resumeStatus.textContent = `${filled ? `Added ${filled} suggestion${filled === 1 ? "" : "s"}` : "No blank fields were changed"}. Review every field before finding matches. ${data.review_notes?.[1] || ""}`;
  } catch (error) {
    resumeStatus.textContent = error.message.includes("fetch") ? "Start the local scholarship API, then try again." : error.message;
  } finally {
    resumeButton.disabled = false;
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  button.disabled = true;
  status.textContent = "Finding your matches...";
  try {
    const student = await saveProfile(profileFromForm());
    const response = await fetch(`${API_BASE}/recommendations/${student.id}`);
    if (!response.ok) throw new Error("We could not load your recommendations.");
    const data = await response.json();
    renderMatches(data.matches, profileFromForm());
    status.textContent = "Your profile is saved. Review each official source before applying.";
  } catch (error) {
    status.textContent = error.message.includes("fetch") ? "Start the local scholarship API, then try again." : error.message;
  } finally { button.disabled = false; }
});

feedbackForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  feedbackStatus.textContent = "Sending feedback...";
  const values = Object.fromEntries(new FormData(feedbackForm));
  values.rating = Number(values.rating);
  try {
    const response = await fetch(`${API_BASE}/feedback/`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(values) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "We couldn't save your feedback.");
    feedbackForm.reset();
    feedbackStatus.textContent = data.message;
  } catch (error) {
    feedbackStatus.textContent = error.message.includes("fetch") ? "Start the local scholarship API, then try again." : error.message;
  }
});
