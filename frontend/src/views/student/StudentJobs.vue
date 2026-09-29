<script setup>

import StudentNavbar from '../../components/StudentNavbar.vue'
import { ref, computed, onMounted } from 'vue'
import api from '../../api'


const token = localStorage.getItem('token')

const jobs = ref([])

const search = ref('')

const degreeFilter = ref('All')


const loading = ref(false)

const successMessage = ref('')

const errorMessage = ref('')

const student = ref({})


/* -----------------------------
   Fetch Jobs
------------------------------ */

const fetchJobs = async () => {

    loading.value = true

    try {

        const response = await api.get(

            '/student/drives',

            {

                headers: {

                    Authorization: `Bearer ${token}`

                }

            }

        )

        jobs.value = response.data

    }

    catch (error) {

        console.log(error)

        errorMessage.value = "Unable to load jobs."

    }

    finally {

        loading.value = false

    }

}



const apply = async (driveId) => {

    try {

        await api.post(

            `/student/apply/${driveId}`,

            {},

            {

                headers: {

                    Authorization: `Bearer ${token}`

                }

            }

        )

        successMessage.value =

            "Application submitted successfully."

        errorMessage.value = ""

        fetchJobs()

    }

    catch (error) {

        successMessage.value = ""

        errorMessage.value =

            error.response.data.message

    }

}



const degrees = computed(() => {

    if (!student.value.degree) {

        return ["All"]

    }

    return [

        student.value.degree,

        "All"

    ]

})



const filteredJobs = computed(() => {

    return jobs.value.filter(job => {

        const searchMatch =

            job.job_title
                .toLowerCase()
                .includes(search.value.toLowerCase())

            ||

            job.company
                .toLowerCase()
                .includes(search.value.toLowerCase())

        const degreeMatch =

            degreeFilter.value === "All"

            ||

            job.eligible_degree === "Any"

            ||

            job.eligible_degree === degreeFilter.value

        return searchMatch && degreeMatch

    })

})

const fetchStudentProfile = async () => {

const response = await api.get(

    "/student/profile",

    {
        headers:{
            Authorization:`Bearer ${token}`
        }
    }

)

student.value = response.data

degreeFilter.value = student.value.degree || "All"

}

onMounted(async () => {

    await fetchJobs()

    await fetchStudentProfile()

})

</script>

<template>

    <StudentNavbar />
    
    <div class="container mt-4">
    

    
        <div class="d-flex justify-content-between align-items-center mb-4">
    
            <div>
    
                <h2>Available Placement Drives</h2>
    
                <p class="text-muted">
                    Browse and apply for available placement opportunities.
                </p>
    
            </div>
    
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
    

    
        <div class="card shadow-sm mb-4">
    
            <div class="card-body">
    
                <div class="row">
    
                    <div class="col-md-6">
    
                        <label class="form-label">
    
                            Search
    
                        </label>
    
                        <input
    
                            class="form-control"
    
                            placeholder="Search by company or job title"
    
                            v-model="search"
    
                        >
    
                    </div>
    
                    <div class="col-md-3">
    
                        <label class="form-label">
    
                            Degree
    
                        </label>
    
                        <select
    
                            class="form-select"
    
                            v-model="degreeFilter"
    
                        >
    
                            <option
    
                                v-for="degree in degrees"
    
                                :key="degree"
    
                            >
    
                                {{ degree }}
    
                            </option>
    
                        </select>
    
                    </div>
    
                </div>
    
            </div>
    
        </div>
    

    
        <div
            v-if="loading"
            class="text-center mt-5"
        >
    
            <div
                class="spinner-border"
            ></div>
    
        </div>
    

    
        <div
    
            v-else-if="filteredJobs.length===0"
    
            class="alert alert-info"
    
        >
    
            No placement drives found.
    
        </div>
    

    
        <div
    
            v-for="job in filteredJobs"
    
            :key="job.id"
    
            class="card shadow-sm mb-4"
    
        >
    
            <div class="card-body">
    
                <div class="d-flex justify-content-between">
    
                    <div>
    
                        <h4>
    
                            {{ job.job_title }}
    
                        </h4>
    
                        <h6 class="text-muted">
    
                            {{ job.company }}
    
                        </h6>
    
                    </div>
    
                    <div>
    
                        <span
    
                            class="badge bg-primary"
    
                        >
    
                            {{ job.location }}
    
                        </span>
    
                    </div>
    
                </div>
    
                <hr>
    
                <p>
    
                    {{ job.job_description }}
    
                </p>
    
                <div class="row mt-3">
    
                    <div class="col-md-4">
    
                        <strong>
    
                            Degree
    
                        </strong>
    
                        <p>
    
                            {{ job.eligible_degree }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4">
    
                        <strong>
    
                            Branch/Specialization
    
                        </strong>
    
                        <p>
    
                            {{ job.eligible_branch }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4">
    
                        <strong>
    
                            Minimum CGPA
    
                        </strong>
    
                        <p>
    
                            {{ job.cgpa_required }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4">
    
                        <strong>
    
                            Experience
    
                        </strong>
    
                        <p>
    
                            {{ job.experience_required || "Not Specified" }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4">
    
                        <strong>
    
                            Salary
    
                        </strong>
    
                        <p>
    
                            {{ job.salary || "Not Disclosed" }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4">
    
                        <strong>
    
                            Openings
    
                        </strong>
    
                        <p>
    
                            {{ job.number_of_openings || 1 }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-6">
    
                        <strong>
    
                            Skills Required
    
                        </strong>
    
                        <p>
    
                            {{ job.skills_required || "Not Specified" }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-6">
    
                        <strong>
    
                            Application Deadline
    
                        </strong>
    
                        <p>
    
                            {{ job.application_deadline }}
    
                        </p>
    
                    </div>
    
                </div>
    
                <div class="mt-3">
    
                    <button
    
                        v-if="!job.already_applied"
    
                        class="btn btn-primary"
    
                        @click="apply(job.id)"
    
                    >
    
                        Apply
    
                    </button>
    
                    <button
    
                        v-else
    
                        class="btn btn-success"
    
                        disabled
    
                    >
    
                        Already Applied
    
                    </button>
    
                </div>
    
            </div>
    
        </div>
    
    </div>
    
    </template>