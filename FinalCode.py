import streamlit as st
import pandas as pd
import numpy as np
import time
import csv
from datetime import date
import os
import plotly.graph_objects as go
from datetime import date, timedelta


#Page settings
st.set_page_config(page_title="KHWEZI MINING", page_icon=":pick:", layout="wide")

st.title("KHWEZI MINING")
st.subheader("Health, Safety and Equipment Monitoring")

#initializing the state session before logging in.
if "logged_in" not in st.session_state:  #log in screen
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state["role"] = ""
    
if "workers" not in st.session_state:
    st.session_state["workers"] = []     #store workers records

if "incidents" not in st.session_state:
    st.session_state["incidents"] = []


# Read users from the CSV file
users = {} #{"Lesiba": ["123","admin"]}

with open("users.csv", mode="r", newline="") as file:   # open the users.csv file in read mode, with newline="" to handle line endings correctly across different operating systems.
    reader = csv.DictReader(file)      #values of the csv must be read as a dictinary {username: Lesiba , password: 123, role: admin}]}

    for row in reader:    #reading the user names from the csv and adding them in the dictionary
        file_username = row["username"].strip()
        file_password = row["password"].strip()
        file_role = row["role"].strip()


        if file_username != "":
            users[file_username] = {"password":file_password, "role":file_role}  #converts the csv into a dictionary





#Login page

if not st.session_state["logged_in"]:
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

####Check the code again

    if st.button("Login"):
        if username in users and password == users[username]["password"]:   #this checks if the user name and the password are correct
            user_role = users[username]["role"]   #this gets the role that belongs to the username on the csv
        else:
            st.error("Incorrect username or password. Enter the correct credentials or contact the system administrator.")
            st.stop()

        st.session_state["logged_in"] = True
        st.session_state["role"] = user_role #####if the username and the password are on the same row in the csv
                                             ##### the login will take me to the page of the user's role as shown on the file

        with st.spinner("Logging in..."):
            time.sleep(2)

        st.success("Login successfull!")
        time.sleep(1)
        st.rerun()     # Restarts the script with the new session state(logged_in=True and role assigned), 
                        # allowing access to the application after login,
                        # Meaning everything under the first if statements won't happen because the opposite is true)

   


##After login, display the appropriate page based on the user's role

else:

    role= st.session_state["role"]
    st.sidebar.title("Khwezi Mining")
    st.sidebar.write("Logged in as:", role)



## navigator for each role

    if role == "Administrator":
        page = ["<CHOOSE>", "Dashboard", "Worker Safety Data", "Equipment Data", "Maintenance Data", "Manage Users", "Safety incidents", "Risk Assessment", "General Reports"]

    elif role == "Safety Officer":
        page = ["<CHOOSE>", "Dashboard", "Worker Safety Data", "Safety Incidents", "Risk Assessment", "General Reports"]

    elif role == "Mine Engineer":
        page = ["<CHOOSE>", "Dashboard", "Worker Safety Data", "Equipment Data", "Maintenance Data", "Safety Incidents", "Risk Assessment", "General Reports"]

    elif role == "Maintenance Manager": ##########Rename this role to Maintenance Engineer
        page = ["<CHOOSE>", "Dashboard", "Equipment Data", "Maintenance Data", "General Reports"] 

    else:
        page = ["<CHOOSE>", "Dashboard", "Worker Safety Data", "Equipment Data", "Maintenance Data", "Safety Incidents", "Risk Assessment", "General Reports"]

    selected_page = st.sidebar.selectbox("Select a section", page)  #might be bad!!!!!!!!!!!

    st.write(" Hello!, ", role, "! Welcome to the Khwezi Mining Health, Safety and Equipment Monitoring System.")

### THE DASHBOARD

    if selected_page == "Dashboard":
        st.header("Dashboard")
        st.write("Welcome,", role, "!")
        st.metric("Workers recorded", len(st.session_state["workers"]))
        st.metric("Safety Incidents Recorded", len(st.session_state["incidents"]))
        high_incidents = 0
        for incident in st.session_state["incidents"]:
            if incident["Severity"] == "High": ####CHECK THIS LINE AGAIN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                high_incidents += 1
        st.metric("High Severity Incidents", high_incidents) ########CHECK THIS LINE AGAIN!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    ###Worker Safety Data

    elif selected_page == "Worker Safety Data":
        st.header("Worker Health and Safety Monitoring")
        st.write("Record the worker's safety data and look for potential health and safety risks.")
        st.subheader("Record Worker Information")
        worker_id = st.text_input("Worker's ID")
        department = st.selectbox("Select Department", ["", "Community Relations", "Electrical Engineering", "Emergency Response", "Environmental Management", "Finance & Commercial", "Fixed Plant Maintenance", "Geology & Exploration", "Geotechnical Engineering", "Grade Control", "Human Resources & Payroll", "Mine Engineering", "Mine Surveying", "Mining Operations (Production)", "Mobile Equipment Maintenance", "Occupational Health & Safety", "Processing / Metallurgy", "Security", "Supply Chain & Logistics"])
        job_role = st.text_input("Job Role")
        shift = st.selectbox("Select Shift", ["Day Shift", "Night Shift"])
        ppe = st.selectbox("Is the worker wearing full PPE?", ["", "Yes", "No"])
        training = st.selectbox("Has the worker recieved and completed safety training?", ["", "Yes", "No"])
        fatigue = st.number_input("Worker's Fatigue Level (1-10)", min_value=1, max_value=10)  ########Check this line again!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        observation = st.text_area("Safety Observation(s)", placeholder="Enter any safety observations or concerns regarding the worker's health and safety.")
        near_misses = st.number_input("Number of near misses reported by the worker", min_value=0, step=1)
        previous_incidents = st.number_input("Number of previous incidents involving the worker", min_value=0, step=1)

        if st.button("Record Worker Data"):
            if worker_id.strip() == "":    #if worker_id is empty or only contains whitespace, show error message
                st.error("Please enter the Worker's ID.")
            elif job_role.strip() == "":     #if job role is empty or only contains whitespace, show error message
                st.error("Please enter the Worker's Job Role.")
            elif department.strip() == "":     #if department is empty or only contains whitespace, show error message
                st.error("Please select the Worker's Department.")
            elif observation.strip() == "":   #if worker's observations is empty or only contains whitespace, show error message
                st.error("Please enter any safety observations or concerns regarding the worker's health and safety. If there are none, please enter 'None'.")
            else:
            # Worker's risk level

                if (ppe == "No" or training == "No" or fatigue >= 8 or near_misses >= 3 or previous_incidents >= 2):
                    risk_level = "High"
                elif fatigue >= 5:
                    risk_level = "Medium"
                else:
                    risk_level = "Low"

#Save worker's information
                worker_data = {"Worker's ID": worker_id, "Department": department, "Job Role": job_role, "Shift": shift, "PPE": ppe, "Training": training, "Fatigue Level": fatigue, "Safety Observation(s)": observation, "Near Misses": near_misses, "Previous Incidents": previous_incidents, "Risk Level": risk_level}

                st.session_state["workers"].append(worker_data)
                st.success("Worker safety data submitted successfully!")

                if risk_level == "High":
                    st.warning("The worker's risk level is HIGH. Please investigate immediately and take action to address the safety concerns.")
        st.subheader("Recorded Worker's Data")

        if len(st.session_state["workers"]) > 0:
            st.dataframe(st.session_state["workers"], use_container_width=True)   #if the length of the workers list is greater than 0, 
                                                    #then the data should be displayed in a table format using the st.dataframe() function. 
                                                    #The dataframe will show all the recorded worker information stored in the session state.
            st.write("Total workers recorded:", len(st.session_state["workers"]))
        else:
            st.info("workers' data has not yet been recorded!")

    #part C

    elif selected_page == "Safety Incidents":
        st.header("Safety Incidents Database")
        st.write("Record and monitor safety incidents that occur at the mine")
        st.subheader("Record a New Safety Incident")
        incident_id = st.text_input("Incident ID")
        incident_worker_id = st.text_input("Worker ID")
        incident_date = st.date_input("Date of incident", value=date.today())
        location = st.text_area("Location of the incident", placeholder= "Where did the incident happen...")
        incident_type = st.text_area("Type of incident", placeholder = "What type...")
        severity = st.selectbox("Incident Severity", ["<CHOOSE>", "Low", "Medium", "High", "Critical"])
        injury = st.selectbox(" Did the incident cause injury?", ["<CHOOSE>", "No", "Yes"])
        description = st.text_area("Description of Incident", placeholder= "Describe what happened...")
        corrective_action = st.text_area("Corrective Measures Taken", placeholder = "Describe actions taken...")

        if st.button("Record Incident"):
            if incident_id.strip() == "":
                st.error("Please enter incident ID.")
            
            elif worker_id.strip()=="":
                st.error("Please input the Worker's ID.")
            
            else:

                duplicate = False
                for incident in st.session_state["indidents"]:
                    if incident["Incident ID"] == incident_id.strip():
                        duplicate = True
                        break

                if duplicate: 
                    st.error("This Incident already exists. Please enter another ID.")
                else:
                    incident = {"Incident ID": incident_id.strip(), "Worker ID": incident_worker_id, "Date": str(incident_date), "Location": location, "Incident Type": incident_type, "Severity": severity, "Injury": injury, "Description": description.strip(), "Corrective Action": corrective_action.strip()}

                    st.session_state["incidents"].append(incident)
                    st.success("Safety incident recorded successfully!") 

                    if severity in ["High", "Critical"]:
                        st.warning("Extreme risk incident recorded. Attend immediately")
                    
                    if injury == "Yes":
                        st.warning("An injury was reported. Attend respond immediately")

        st.subheader("Recorded Safety Incidents")

        if len(st.session_state["incidents"]) > 0:
            st.dataframe(st.session_state["incidents"], use_container_width = True)
            st.write("Total incidents recorded:", len(st.session_state["incidents"]))
        else:
            st.info("No safety incidents have been recorded yet.")


#####PLACEHOLDERS FOR OTHER SECTIONS
                        
    elif selected_page == "Equipment Data":
        st.info("The equipment monitoring session still needs to be added")
        st.header("Equipment Database and Condition Monitoring")
        equipment_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "equipment.csv")
        equipment_types = ["Haul Truck", "Loader", "Excavator", "Drilling Machine",
                           "Bulldozer", "Scraper Winch", "Crusher", "Conveyor"]
        part_statuses = ["Good", "Worn", "Faulty"]
        maintenance_statuses = ["Operational", "Due for Maintenance", "Overdue", "Under Maintenance"]
        columns = ["Equipment ID", "Equipment Type", "Manufacturer", "Operating Hours",
                   "Temperature (C)", "Vibration (mm/s)", "Fuel Consumption (L/h)",
                   "Brake Status", "Tyre Status", "Engine Status", "Maintenance Status",
                   "Downtime (hours)", "Last Maintenance", "Next Maintenance Due", "Alert Count"]
        numeric = ["Operating Hours", "Temperature (C)", "Vibration (mm/s)",
                   "Fuel Consumption (L/h)", "Downtime (hours)", "Alert Count"]

        # Accept the column names used in your earlier equipment CSV.
        aliases = {"ID": "Equipment ID", "Type": "Equipment Type",
                   "Operating time": "Operating Hours", "Temperature": "Temperature (C)",
                   "Vibration": "Vibration (mm/s)", "Fuel": "Fuel Consumption (L/h)",
                   "Brakes": "Brake Status", "Tyres": "Tyre Status", "Engine": "Engine Status",
                   "Maintenance": "Maintenance Status", "Downtime": "Downtime (hours)",
                   "Alerts": "Alert Count"}

        # Load saved records once per session.
        if "equipment" not in st.session_state:
            try:
                saved = pd.read_csv(equipment_file, keep_default_na=False, dtype=str)
                st.session_state["equipment"] = saved.to_dict("records")
            except (FileNotFoundError, pd.errors.EmptyDataError):
                st.session_state["equipment"] = []

        data = pd.DataFrame(st.session_state["equipment"])
        for old, new in aliases.items():
            if old in data.columns and new not in data.columns:
                data[new] = data[old]
        if "Operating Hours" not in data.columns and "Hours" in data.columns:
            data["Operating Hours"] = data["Hours"]
        for column in columns:
            if column not in data.columns:
                data[column] = 0 if column in numeric else ""
        data[numeric] = data[numeric].apply(pd.to_numeric, errors="coerce").fillna(0)
        data["Maintenance Status"] = data["Maintenance Status"].replace(
            {"Normal": "Operational", "Due": "Due for Maintenance"})
        st.session_state["equipment"] = data.to_dict("records")

        def save_equipment():
            saved = pd.DataFrame(st.session_state["equipment"])
            for old, new in aliases.items():
                if old in saved.columns:
                    saved[old] = saved[new]
            saved.to_csv(equipment_file, index=False)

        # Example limits: temperature 80/100 C; vibration 5/8 mm/s.
        def reading_status(value, warning, critical):
            if value > critical:
                return "Critical"
            elif value >= warning:
                return "Warning"
            else:
                return "Normal"

        def machine_condition(temp, vibration):
            states = [reading_status(temp, 80, 100), reading_status(vibration, 5, 8)]
            if "Critical" in states:
                return "Critical"
            elif "Warning" in states:
                return "Warning"
            else:
                return "Normal"

        if "equipment_message" in st.session_state:
            st.success(st.session_state.pop("equipment_message"))

        register, records, monitoring, charts = st.tabs(
            ["D: Register", "D: Equipment Records", "E: Monitoring", "E: Charts"])

        # D: Register a machine and save its details.
        with register:
            with st.form("equipment_form", clear_on_submit=True):
                left, right = st.columns(2)
                eq_id = left.text_input("Equipment ID")
                eq_type = left.selectbox("Equipment Type", equipment_types)
                maker = left.text_input("Manufacturer")
                hours = left.number_input("Operating Hours", min_value=0.0)
                downtime = left.number_input("Downtime (hours)", min_value=0.0)
                fuel = left.number_input("Fuel consumption (L/h)", min_value=0.0)
                temp = left.number_input("Temperature (C)", value=60.0)
                vibration = left.number_input("Vibration (mm/s)", min_value=0.0, value=2.0)
                brakes = right.selectbox("Brake Status", part_statuses)
                tyres = right.selectbox("Tyre Status", part_statuses)
                engine = right.selectbox("Engine Status", part_statuses)
                maintenance = right.selectbox("Maintenance Status", maintenance_statuses)
                last = right.date_input("Last Maintenance", value=date.today())
                due = right.date_input("Next Maintenance Due", value=date.today() + timedelta(days=90))
                submitted = st.form_submit_button("Register Equipment")

            if submitted:
                existing_ids = [r["Equipment ID"] for r in st.session_state["equipment"]]
                if not eq_id.strip() or not maker.strip():
                    st.error("Equipment ID and manufacturer are required.")
                elif eq_id.strip() in existing_ids:
                    st.error("This equipment ID already exists.")
                elif due < last:
                    st.error("Next maintenance due cannot be before last maintenance.")
                else:
                    st.session_state["equipment"].append({
                        "Equipment ID": eq_id.strip(), "Equipment Type": eq_type,
                        "Manufacturer": maker.strip(), "Operating Hours": hours,
                        "Temperature (C)": temp, "Vibration (mm/s)": vibration,
                        "Fuel Consumption (L/h)": fuel, "Brake Status": brakes,
                        "Tyre Status": tyres, "Engine Status": engine,
                        "Maintenance Status": maintenance, "Downtime (hours)": downtime,
                        "Last Maintenance": str(last), "Next Maintenance Due": str(due),
                        "Alert Count": int(temp >= 80) + int(vibration >= 5)
                    })
                    save_equipment()
                    st.session_state["equipment_message"] = "Equipment registered successfully."
                    st.rerun()

        data = pd.DataFrame(st.session_state["equipment"], columns=columns)
        if not data.empty:
            data["Condition"] = [machine_condition(t, v)
                                 for t, v in zip(data["Temperature (C)"], data["Vibration (mm/s)"])]

        # D: Search, filter and display saved equipment.
        with records:
            if data.empty:
                st.info("No equipment recorded yet.")
            else:
                search = st.text_input("Search Equipment ID / Manufacturer")
                kind = st.selectbox("Filter Equipment Type", ["All"] + equipment_types)
                view = data.copy()
                if kind != "All":
                    view = view[view["Equipment Type"] == kind]
                if search:
                    mask = (view["Equipment ID"].astype(str).str.contains(search, case=False, regex=False)
                            | view["Manufacturer"].astype(str).str.contains(search, case=False, regex=False))
                    view = view[mask]
                st.dataframe(view, use_container_width=True)

        # E: Check and update the selected machine's readings.
        with monitoring:
            st.caption("These monitoring limits are educational example values.")
            if data.empty:
                st.info("Register equipment before checking readings.")
            else:
                st.table(pd.DataFrame({
                    "Parameter": ["Temperature", "Vibration"],
                    "Normal": ["Below 80 C", "Below 5 mm/s"],
                    "Warning": ["80 to 100 C", "5 to 8 mm/s"],
                    "Critical": ["Above 100 C", "Above 8 mm/s"]
                }))
                selected_id = st.selectbox("Select Equipment", data["Equipment ID"].tolist())
                machine = next(r for r in st.session_state["equipment"] if r["Equipment ID"] == selected_id)

                with st.form("reading_form_" + selected_id):
                    new_temp = st.number_input("New Temperature (C)", value=float(machine["Temperature (C)"]))
                    new_vibration = st.number_input("New Vibration (mm/s)", min_value=0.0,
                                                    value=float(machine["Vibration (mm/s)"]))
                    update = st.form_submit_button("Update Readings")

                if update:
                    machine["Temperature (C)"] = new_temp
                    machine["Vibration (mm/s)"] = new_vibration
                    machine["Alert Count"] += int(new_temp >= 80) + int(new_vibration >= 5)
                    save_equipment()
                    st.session_state["equipment_message"] = "Readings updated successfully."
                    st.rerun()

                for name, value, warning, critical, unit in [
                    ("Temperature", machine["Temperature (C)"], 80, 100, "C"),
                    ("Vibration", machine["Vibration (mm/s)"], 5, 8, "mm/s")
                ]:
                    status = reading_status(value, warning, critical)
                    message = f"{selected_id}: {name} = {value:g} {unit} ({status})"
                    if status == "Critical":
                        st.error(message + ". Inspection required.")
                    elif status == "Warning":
                        st.warning(message + ". Monitor closely and arrange an inspection.")
                    else:
                        st.success(message)

                st.dataframe(data[["Equipment ID", "Temperature (C)", "Vibration (mm/s)",
                                   "Condition", "Alert Count"]], use_container_width=True)

        # E: Compare readings with the warning and critical limits.
        with charts:
            if data.empty:
                st.info("Register equipment to display charts.")
            else:
                for column, warning, critical in [("Temperature (C)", 80, 100),
                                                   ("Vibration (mm/s)", 5, 8)]:
                    figure = go.Figure(go.Bar(x=data["Equipment ID"], y=data[column]))
                    figure.update_layout(title=column, xaxis_title="Equipment ID", yaxis_title=column)
                    figure.add_hline(y=warning, line_dash="dash", line_color="orange", annotation_text="Warning")
                    figure.add_hline(y=critical, line_dash="dash", line_color="red", annotation_text="Critical")
                    st.plotly_chart(figure, use_container_width=True)
                st.bar_chart(data["Condition"].value_counts())

    elif selected_page == "Maintenance Data":
        st.header("Maintenance Data")
        st.info("The maintenance section session still needs to be added")  #add a code here

    elif selected_page == "Risk Assessment":
        st.header("Risk Assessment")
        st.info("The Risk Assessment session still needs to be added")   #add a code here
            
    elif selected_page == "General Reports":
        st.header("General Reports")
        st.write("Worker records:", len(st.session_state["workers"]))
        st.write("Incident records:", len(st.session_state["incidents"]))

        if st.button("Show Worker Records"):
            if st.session_state["workers"]:
                st.dataframe(st.session_state["workers"])
            else:
                st.info("No worker records are available.")

        if st.button("Show Incident Records"):
            if st.session_state["incidents"]:
                st.dataframe(st.session_state["incidents"])
            else:
                st.info("No incident records are available.")
        
    elif selected_page == "Manage Users":
        st.header("Manage Users")
        st.write("Users loaded from users.csv:")
        user_list=[]

        for username_from_file in users:
            user_list.append({"Username": username_from_file, "Role": users[username_from_file]["role"]})
        
        st.dataframe(user_list, use_container_width=True)



    ####Logout

    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["role"] = ""

        st.rerun()
         
