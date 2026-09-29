<script setup>

import CompanyNavbar from '../../components/CompanyNavbar.vue'

import { ref, onMounted } from 'vue'

import { useRoute } from 'vue-router'

import api from '../../api'

const route = useRoute()

const token = localStorage.getItem('token')

const drives = ref([])

const applicants = ref([])

const selectedDrive = ref('')

const selectedApplication = ref(null)

const interview_date = ref('')

const interview_time = ref('')

const interview_location = ref('')

const exportReady = ref(false)

const fetchDrives = async () => {

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



const fetchApplicants = async () => {

    if (!selectedDrive.value) return

    const response = await api.get(

        `/company/applications/${selectedDrive.value}`,

        {

            headers: {

                Authorization: `Bearer ${token}`

            }

        }

    )

    applicants.value = response.data

}


const updateStatus = async (

    applicationId,

    status

) => {

    try {

        await api.put(

            `/company/application/${applicationId}/status`,

            {

                status: status

            },

            {

                headers: {

                    Authorization: `Bearer ${token}`

                }

            }

        )

        fetchApplicants()

    }

    catch (error) {

        alert(

            error.response.data.message

        )

    }

}


const openInterviewForm = (

    applicant

) => {

    selectedApplication.value = applicant

}

const scheduleInterview = async () => {

    try {

        await api.put(

            `/company/application/${selectedApplication.value.application_id}/interview`,

            {

                date: interview_date.value,

                time: interview_time.value,

                location: interview_location.value

            },

            {

                headers: {

                    Authorization: `Bearer ${token}`

                }

            }

        )

        selectedApplication.value = null

        interview_date.value = ''

        interview_time.value = ''

        interview_location.value = ''

        fetchApplicants()

    }

    catch (error) {

        alert(

            error.response.data.message

        )

    }

}

const markPlaced = async(applicationId)=>{

await api.put(

    `/company/application/${applicationId}/placed`,

    {},

    {

        headers:{

            Authorization:`Bearer ${token}`

        }

    }

)

fetchApplicants()

}


onMounted(async () => {

    await fetchDrives()

    if (route.query.drive) {

        selectedDrive.value = route.query.drive

        fetchApplicants()

    }

})

</script>

<template>

    <CompanyNavbar />
    
    <div class="container mt-4">
    

    
        <div class="d-flex justify-content-between align-items-center mb-4">
    
            <div>
    
                <h2>Applicants</h2>
    
                <p class="text-muted">
                    Manage applications for your placement drives.
                </p>
    
            </div>
    
        </div>
    

    
        <div class="card shadow-sm mb-4">
    
            <div class="card-body">
    
                <label class="form-label">
    
                    Select Placement Drive
    
                </label>
    
                <select
    
                    class="form-select"
    
                    v-model="selectedDrive"
    
                    @change="fetchApplicants"
    
                >
    
                    <option value="">
    
                        Choose Drive
    
                    </option>
    
                    <option
    
                        v-for="drive in drives"
    
                        :key="drive.id"
    
                        :value="drive.id"
    
                    >
    
                        {{ drive.job_title }}
    
                        ({{ drive.applicant_count }} Applicants)
    
                    </option>
    
                </select>
    
            </div>
    
        </div>
        <div class="mb-4">

            
</div>

    
        <div
    
            v-if="selectedDrive && applicants.length===0"
    
            class="alert alert-info"
    
        >
    
            No applicants found for this placement drive.
    
        </div>
    

    
        <div
    
            v-for="applicant in applicants"
    
            :key="applicant.application_id"
    
            class="card shadow-sm mb-4"
    
        >
    
            <div class="card-body">
    
                <div class="d-flex justify-content-between">
    
                    <div>
    
                        <h4>
    
                            {{ applicant.student_name }}
    
                        </h4>
    
                        <p class="mb-1">
    
                            <strong>Branch:</strong>
    
                            {{ applicant.branch }}
    
                        </p>
    
                        <p class="mb-1">
    
                            <strong>CGPA:</strong>
    
                            {{ applicant.cgpa }}
    
                        </p>
    
                    </div>
    
                    <div>
    
                        <span
    
                            class="badge bg-primary"
    
                        >
    
                            {{ applicant.status }}
    
                        </span>
    
                    </div>
    
                </div>
                <button

                class="btn btn-outline-primary me-2"

                @click="$router.push(`/company/student/${applicant.student_id}`)"

                >

                View Profile

                </button>
                <hr>
    

    
                <div
    
                    v-if="applicant.status==='applied'"
    
                >
    
                    <button
    
                        class="btn btn-success me-2"
    
                        @click="updateStatus(applicant.application_id,'shortlisted')"
    
                    >
    
                        Shortlist
    
                    </button>
    
                    <button
    
                        class="btn btn-danger"
    
                        @click="updateStatus(applicant.application_id,'rejected')"
    
                    >
    
                        Reject
    
                    </button>
    
                </div>
    

    
                <div
    
                    v-if="applicant.status==='shortlisted'"
    
                >
    
                    <div class="alert alert-success">
    
                        Candidate Shortlisted
    
                    </div>
    
                    <button
    
                        class="btn btn-warning"
    
                        @click="openInterviewForm(applicant)"
    
                    >
    
                        Schedule Interview
    
                    </button>
    
                </div>
    

    
                <div
    
                    v-if="applicant.status==='interview_scheduled'"
    
                >
    
                    <div class="alert alert-warning">
    
                        Interview Scheduled
    
                    </div>
    
                    <p>
    
                        <strong>Date:</strong>
    
                        {{ applicant.interview_date }}
    
                    </p>
    
                    <p>
    
                        <strong>Time:</strong>
    
                        {{ applicant.interview_time }}
    
                    </p>
    
                    <p>
    
                        <strong>Location:</strong>
    
                        {{ applicant.interview_location }}
    
                    </p>
    
                    <button
    
                        class="btn btn-success me-2"
    
                        @click="updateStatus(applicant.application_id,'offer')"
    
                    >
    
                        Offer Candidate
    
                    </button>
    
                    <button
    
                        class="btn btn-danger"
    
                        @click="updateStatus(applicant.application_id,'rejected')"
    
                    >
    
                        Reject
    
                    </button>
    
                </div>
    

    
                <div
    
                    v-if="applicant.status==='offer'"
    
                >
    
                    <div class="alert alert-success">
    
                        Offer Released to Candidate
    
                    </div>
                    <button

                    class="btn btn-dark ms-2"

                    @click="markPlaced(applicant.application_id)"

                    v-if="applicant.status==='offer'"

                    >

                    Mark as Placed

                    </button>
                </div>
    

    
                <div
    
                    v-if="applicant.status==='rejected'"
    
                >
    
                    <div class="alert alert-danger">
    
                        Candidate Rejected
    
                    </div>
    
                </div>
    
            </div>
    
        </div>
    

    
        <div
    
            v-if="selectedApplication"
    
            class="modal d-block"
    
            style="background:rgba(0,0,0,.5)"
    
        >
    
            <div class="modal-dialog">
    
                <div class="modal-content">
    
                    <div class="modal-header">
    
                        <h4>
    
                            Schedule Interview
    
                        </h4>
    
                        <button
    
                            class="btn-close"
    
                            @click="selectedApplication=null"
    
                        >
    
                        </button>
    
                    </div>
    
                    <div class="modal-body">
    
                        <label>
    
                            Interview Date
    
                        </label>
    
                        <input
    
                            type="date"
    
                            class="form-control mb-3"
    
                            v-model="interview_date"
    
                        >
    
                        <label>
    
                            Interview Time
    
                        </label>
    
                        <input
    
                            type="time"
    
                            class="form-control mb-3"
    
                            v-model="interview_time"
    
                        >
    
                        <label>
    
                            Interview Location / Google Meet Link
    
                        </label>
    
                        <input
    
                            class="form-control"
    
                            v-model="interview_location"
    
                        >
    
                    </div>
    
                    <div class="modal-footer">
    
                        <button
    
                            class="btn btn-success"
    
                            @click="scheduleInterview"
    
                        >
    
                            Confirm Interview
    
                        </button>
    
                    </div>
    
                </div>
    
            </div>
    
        </div>
    
    </div>
    
    </template>