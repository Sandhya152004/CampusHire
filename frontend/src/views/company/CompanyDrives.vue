<script setup>

import CompanyNavbar from '../../components/CompanyNavbar.vue'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useRoute } from "vue-router"

const route = useRoute()
import api from '../../api'

const router = useRouter()

const token = localStorage.getItem('token')

const drives = ref([])

const successMessage = ref('')
const errorMessage = ref('')

const showCreateModal = ref(false)
const showEditModal = ref(false)

const editingDrive = ref(null)

const job_title = ref('')
const job_description = ref('')
const cgpa_required = ref('')

const eligible_degree = ref('Any')
const eligible_branch = ref('Any')

const application_deadline = ref('')

const edit_job_title = ref('')
const edit_job_description = ref('')
const edit_cgpa_required = ref('')

const edit_degree = ref('')
const edit_branch = ref('')

const edit_deadline = ref('')

const fetchDrives = async () => {

  try {

    const response = await api.get(

      '/company/drives',

      {

        headers: {

          Authorization: `Bearer ${token}`

        }

      }

    )

    drives.value = response.data

  }

  catch (error) {

    console.log(error)

  }

}

const driveId = route.query.edit

if (driveId) {

    const drive = drives.value.find(

        d => d.id == driveId

    )

    if (drive) {

        openEditDrive(drive)

    }

}
const createDrive = async () => {

  try {

    await api.post(

      '/company/drive',

      {

        job_title: job_title.value,

        job_description: job_description.value,

        cgpa_required: parseFloat(
          cgpa_required.value
        ),

        eligible_degree:
        eligible_degree.value,

        eligible_branch:
        eligible_branch.value,

        application_deadline:
        application_deadline.value

      },

      {

        headers: {

          Authorization:
          `Bearer ${token}`

        }

      }

    )

    successMessage.value =
    "Placement Drive Created Successfully"

    errorMessage.value = ""

    job_title.value = ""
    job_description.value = ""
    cgpa_required.value = ""

    eligible_degree.value = "Any"
    eligible_branch.value = "Any"

    application_deadline.value = ""

    showCreateModal.value = false

    fetchDrives()

  }

  catch (error) {

    console.log(error)

    errorMessage.value =
    "Failed to create drive."

    successMessage.value = ""

  }

}


const openEditDrive = (drive) => {

  editingDrive.value = drive

  edit_job_title.value =
  drive.job_title

  edit_job_description.value =
  drive.job_description

  edit_cgpa_required.value =
  drive.cgpa_required

  edit_degree.value =
  drive.eligible_degree

  edit_branch.value =
  drive.eligible_branch

  edit_deadline.value =
  drive.application_deadline

  showEditModal.value = true

}

const updateDrive = async () => {

  try {

    await api.put(

      `/company/drive/${editingDrive.value.id}`,

      {

        job_title:
        edit_job_title.value,

        job_description:
        edit_job_description.value,

        cgpa_required:
        edit_cgpa_required.value,

        eligible_degree:
        edit_degree.value,

        eligible_branch:
        edit_branch.value,

        application_deadline:
        edit_deadline.value

      },

      {

        headers: {

          Authorization:
          `Bearer ${token}`

        }

      }

    )

    showEditModal.value = false

    editingDrive.value = null

    fetchDrives()

  }

  catch(error){

    console.log(error)

  }

}


const closeDrive = async (driveId) => {

  if(

    !confirm(
      "Are you sure you want to close this drive?"
    )

  )

  return

  try{

    await api.put(

      `/company/drive/${driveId}/close`,

      {},

      {

        headers:{

          Authorization:
          `Bearer ${token}`

        }

      }

    )

    fetchDrives()

  }

  catch(error){

    console.log(error)

  }

}


const viewApplicants = (driveId)=>{

  router.push(

    `/company/applicants?drive=${driveId}`

  )

}

const exportApplications = async () => {

try{

    await api.post(

        "/company/export-applications",

        {},

        {

            headers:{

                Authorization:`Bearer ${token}`

            }

        }

    )

    exportReady.value = true

    alert("Export completed successfully.")

}

catch(error){

    alert("Export failed.")

}

}

const downloadCSV = async () => {

const response = await api.get(

"/company/export/download",

{

    responseType:"blob",

    headers:{

        Authorization:`Bearer ${token}`

    }

}

)

const url = window.URL.createObjectURL(

new Blob([response.data])

)

const link = document.createElement("a")

link.href = url

link.download = "CompanyApplications.csv"

link.click()

}


onMounted(()=>{

  fetchDrives()

})

</script>

<template>

    <CompanyNavbar />
    
    <div class="container mt-4">
    

    
        <div class="d-flex justify-content-between align-items-center mb-4">
    
            <div>
    
                <h2>My Placement Drives</h2>
    
                <p class="text-muted">
                    Create and manage all your placement drives.
                </p>
    
            </div>
            
            <button

                class="btn btn-success"

                @click="exportApplications"

                >

                Export Applicants (CSV)

                </button>

                <button

                v-if="exportReady"

                class="btn btn-primary ms-2"

                @click="downloadCSV"

                >

                Download CSV

                </button>

            <button
                class="btn btn-primary"
                @click="showCreateModal = true"
            >
                + New Drive
            </button>
    
        </div>
    

    
        <div
            v-if="successMessage"
            class="alert alert-success"
        >
            {{ successMessage }}
        </div>
    
        <div
            v-if="errorMessage"
            class="alert alert-danger"
        >
            {{ errorMessage }}
        </div>
    

    
        <div
            v-if="drives.length===0"
            class="card shadow-sm p-5 text-center"
        >
    
            <h4>No Placement Drives Yet</h4>
    
            <p class="text-muted">
    
                Click "New Drive" to create your first placement drive.
    
            </p>
    
        </div>
    

    
        <div
            v-for="drive in drives"
            :key="drive.id"
            class="card shadow-sm mb-4"
        >
    
            <div class="card-body">
    
                <div
                    class="d-flex justify-content-between"
                >
    
                    <div>
    
                        <h4>
    
                            {{ drive.job_title }}
    
                        </h4>
    
                        <p class="text-muted">
    
                            {{ drive.job_description }}
    
                        </p>
    
                    </div>
    
                    <span
                        class="badge bg-success"
                        v-if="!drive.is_closed"
                    >
    
                        Active
    
                    </span>
    
                    <span
                        class="badge bg-secondary"
                        v-else
                    >
    
                        Closed
    
                    </span>
    
                </div>
    
                <hr>
    
                <div class="row">
    
                    <div class="col-md-4">
    
                        <p>
    
                            <strong>Degree</strong>
    
                            <br>
    
                            {{ drive.eligible_degree }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4">
    
                        <p>
    
                            <strong>Branch/Specialization</strong>
    
                            <br>
    
                            {{ drive.eligible_branch }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4">
    
                        <p>
    
                            <strong>CGPA</strong>
    
                            <br>
    
                            {{ drive.cgpa_required }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4">
    
                        <p>
    
                            <strong>Deadline</strong>
    
                            <br>
    
                            {{ drive.application_deadline }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4">
    
                        <p>
    
                            <strong>Applicants</strong>
    
                            <br>
    
                            {{ drive.applicant_count }}
    
                        </p>
    
                    </div>
    
                </div>
    
                <hr>
    
                <button
                    class="btn btn-primary me-2"
                    @click="viewApplicants(drive.id)"
                >
    
                    View Applicants
    
                </button>
    
                <button
                    class="btn btn-warning me-2"
                    @click="openEditDrive(drive)"
                >
    
                    Edit
    
                </button>
    
                <button
                    class="btn btn-danger"
                    @click="closeDrive(drive.id)"
                    v-if="!drive.is_closed"
                >
    
                    Close Drive
    
                </button>
    
            </div>
    
        </div>
    

    
        <div
            v-if="showCreateModal"
            class="modal d-block"
            style="background:rgba(0,0,0,.5)"
        >
    
            <div class="modal-dialog modal-lg">
    
                <div class="modal-content">
    
                    <div class="modal-header">
    
                        <h4>Create Placement Drive</h4>
    
                        <button
                            class="btn-close"
                            @click="showCreateModal=false"
                        ></button>
    
                    </div>
    
                    <div class="modal-body">
    
                        <label class="form-label">
    
                            Job Title
    
                        </label>
    
                        <input
                            class="form-control mb-3"
                            v-model="job_title"
                        >
    
                        <label class="form-label">
    
                            Job Description
    
                        </label>
    
                        <textarea
                            class="form-control mb-3"
                            rows="4"
                            v-model="job_description"
                        ></textarea>
    
                        <div class="row">
    
                            <div class="col-md-4">
    
                                <label>
    
                                    Minimum CGPA
    
                                </label>
    
                                <input
                                    type="number"
                                    class="form-control"
                                    v-model="cgpa_required"
                                >
    
                            </div>
    
                            <div class="col-md-4">
    
                                <label>Eligible Degree</label>

                                <select
                                    class="form-select"
                                    v-model="eligible_degree"
                                >
                                    <option value="Any">Any</option>
                                    <option value="B.Tech">B.Tech</option>
                                    <option value="B.Sc">B.Sc</option>
                                    <option value="BCA">BCA</option>
                                    <option value="B.Com">B.Com</option>
                                    <option value="B.A">B.A</option>
                                    <option value="M.Tech">M.Tech</option>
                                    <option value="M.Sc">M.Sc</option>
                                    <option value="MBA">MBA</option>
                                    <option value="Other">Other</option>
                                </select>
    
                            </div>
    
                            <div class="col-md-4">
    
                                <label>
    
                                    Eligible Branch/Specialization
    
                                </label>
    
                                <input
                                class="form-control"
                                placeholder="e.g. Computer Science, Chemistry, Data Science or Any"
                                v-model="eligible_branch"
                                />
    
                            </div>
    
                        </div>
    
                        <label class="mt-3">
    
                            Application Deadline
    
                        </label>
    
                        <input
                            type="date"
                            class="form-control"
                            v-model="application_deadline"
                        >
    
                    </div>
    
                    <div class="modal-footer">
    
                        <button
                            class="btn btn-success"
                            @click="createDrive"
                        >
    
                            Create Drive
    
                        </button>
    
                    </div>
    
                </div>
    
            </div>
    
        </div>
    

    
        <div
            v-if="showEditModal"
            class="modal d-block"
            style="background:rgba(0,0,0,.5)"
        >
    
            <div class="modal-dialog modal-lg">
    
                <div class="modal-content">
    
                    <div class="modal-header">
    
                        <h4>Edit Placement Drive</h4>
    
                        <button
                            class="btn-close"
                            @click="showEditModal=false"
                        ></button>
    
                    </div>
    
                    <div class="modal-body">
    
                        <label>
    
                            Job Title
    
                        </label>
    
                        <input
                            class="form-control mb-3"
                            v-model="edit_job_title"
                        >
    
                        <label>
    
                            Job Description
    
                        </label>
    
                        <textarea
                            class="form-control mb-3"
                            rows="4"
                            v-model="edit_job_description"
                        ></textarea>
    
                        <div class="row">
    
                            <div class="col-md-4">
    
                                <label>
    
                                    CGPA
    
                                </label>
    
                                <input
                                    class="form-control"
                                    v-model="edit_cgpa_required"
                                >
    
                            </div>
    
                            <div class="col-md-4">
    
                                <label>Eligible Degree</label>

                                <select
                                    class="form-select"
                                    v-model="edit_degree"
                                >
                                    <option value="Any">Any</option>
                                    <option value="B.Tech">B.Tech</option>
                                    <option value="B.Sc">B.Sc</option>
                                    <option value="BCA">BCA</option>
                                    <option value="B.Com">B.Com</option>
                                    <option value="B.A">B.A</option>
                                    <option value="M.Tech">M.Tech</option>
                                    <option value="M.Sc">M.Sc</option>
                                    <option value="MBA">MBA</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
    
                            <div class="col-md-4">
    
                                <label>
    
                                    Branch/Specialization
    
                                </label>
    
                                <input
                                    class="form-control"
                                    v-model="edit_branch"
                                >
    
                            </div>
    
                        </div>
    
                        <label class="mt-3">
    
                            Application Deadline
    
                        </label>
    
                        <input
                            type="date"
                            class="form-control"
                            v-model="edit_deadline"
                        >
    
                    </div>
    
                    <div class="modal-footer">
    
                        <button
                            class="btn btn-warning"
                            @click="updateDrive"
                        >
    
                            Save Changes
    
                        </button>
    
                    </div>
    
                </div>
    
            </div>
    
        </div>
    
    </div>
    
    </template>