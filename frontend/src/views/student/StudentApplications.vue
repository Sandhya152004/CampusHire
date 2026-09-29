<script setup>

import StudentNavbar from '../../components/StudentNavbar.vue'

import { ref, onMounted } from 'vue'

import api from '../../api'

const token = localStorage.getItem('token')

const applications = ref([])

const loading = ref(false)

const exportReady = ref(false)

const fetchApplications = async () => {

    loading.value = true

    try {

        const response = await api.get(

            '/student/applications',

            {

                headers: {

                    Authorization: `Bearer ${token}`

                }

            }

        )

        applications.value = response.data

    }

    catch (error) {

        console.log(error)

    }

    finally {

        loading.value = false

    }

}
const exportApplications = async () => {

    try {

        const response = await api.post(

            "/student/export-applications",

            {},

            {

                headers: {

                    Authorization: `Bearer ${token}`

                }

            }

        )

        exportReady.value = true

        alert(
            "Export completed successfully.\n\nClick 'Download CSV' to save your file."
        )

    }

    catch (error) {

        alert(error.response?.data?.message || "Export failed.")

    }

}

const downloadCSV = async () => {

    try {

        const response = await api.get(

            "/student/export/download",

            {

                responseType: "blob",

                headers: {

                    Authorization: `Bearer ${token}`

                }

            }

        )

        const url = window.URL.createObjectURL(

            new Blob([response.data])

        )

        const link = document.createElement("a")

        link.href = url

        link.download = "Applications.csv"

        document.body.appendChild(link)

        link.click()

        document.body.removeChild(link)

        window.URL.revokeObjectURL(url)

    }

    catch (error) {

        alert("Unable to download CSV.")

    }

}

const downloadOfferLetter = async (applicationId) => {

try {

    const response = await api.get(

        `/student/offer-letter/${applicationId}`,

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

    link.download = "OfferLetter.pdf"

    document.body.appendChild(link)

    link.click()

    document.body.removeChild(link)

    window.URL.revokeObjectURL(url)

}

catch(error){

    alert(

        error.response?.data?.message ||

        "Unable to download offer letter."

    )

}

}

onMounted(() => {

    fetchApplications()

})

</script>

<template>

    <StudentNavbar></StudentNavbar>

    <div class="container mt-4">



        <div class="d-flex justify-content-between align-items-center mb-4">

            <div>

                <h2>My Applications</h2>

                <p class="text-muted">
                    Track the status of all your placement applications.
                </p>

            </div>
           <button class="btn btn-success" @click="exportApplications"

>

                Export Applications (CSV)

            </button>
            <button

                v-if="exportReady"

                class="btn btn-primary ms-2"

                @click="downloadCSV"

            >

                Download CSV

            </button>
            </div>



        <div v-if="loading" class="text-center mt-5">

            <div class="spinner-border"></div>

        </div>



        <div v-else-if="applications.length === 0" class="alert alert-info">

            You have not applied to any placement drives yet.

        </div>





        <h4 class="mb-3">

            Current Applications

        </h4>

        <div v-for="application in applications.filter(

            a =>

                a.status !== 'placed' &&

                a.status !== 'rejected'

        )" :key="application.application_id" class="card shadow-sm mb-4">

            <div class="card-body">

                <div class="d-flex justify-content-between">

                    <div>

                        <h4>

                            {{ application.job_title }}

                        </h4>

                        <h6 class="text-muted">

                            {{ application.company }}

                        </h6>

                    </div>

                    <div>

                        <span class="badge" :class="{

                            'bg-secondary': application.status === 'applied',

                            'bg-primary': application.status === 'shortlisted',

                            'bg-warning text-dark': application.status === 'interview_scheduled',

                            'bg-success': application.status === 'offer' ||

                                application.status === 'placed',

                            'bg-danger': application.status === 'rejected'

                        }">

                            {{ application.status }}

                        </span>

                    </div>

                </div>

                <hr>

                <div class="row">

                    <div class="col-md-4">

                        <strong>

                            Applied On

                        </strong>

                        <p>

                            {{ application.applied_at }}

                        </p>

                    </div>

                </div>
                <div
                    v-if="application.status === 'offer' || application.status === 'placed'"
                    class="mt-3"
                >

                    <button

                        class="btn btn-success"

                        @click="downloadOfferLetter(application.application_id)"

                    >

                        Download Offer Letter (PDF)

                    </button>

                </div>


                <div v-if="application.status === 'interview_scheduled'" class="mt-3">

                    <div class="card bg-light">

                        <div class="card-body">

                            <h5>

                                Interview Details

                            </h5>

                            <div class="row">

                                <div class="col-md-4">

                                    <strong>Date</strong>

                                    <p>

                                        {{ application.interview_date }}

                                    </p>

                                </div>

                                <div class="col-md-4">

                                    <strong>Time</strong>

                                    <p>

                                        {{ application.interview_time }}

                                    </p>

                                </div>

                                <div class="col-md-4">

                                    <strong>Location</strong>

                                    <p>

                                        {{ application.interview_location }}

                                    </p>

                                </div>

                            </div>

                        </div>

                    </div>

                </div>

               <div v-if="application.status === 'offer' || application.status === 'placed'"
                    class="alert alert-success mt-3">



                  <span v-if="application.status === 'offer'">
                        Congratulations. You have received an offer for this position.
                    </span>



                  <span v-else>
                        Congratulations! You have been placed for this position.
                    </span>

                </div>


                <div v-if="application.status === 'rejected'" class="alert alert-danger mt-3">

                    Your application was not selected for this position.

                </div>

            </div>

        </div>
        <hr class="my-5">

        <h4 class="mb-3">

            Placement History

        </h4>

        <div v-for="application in applications.filter(

            a =>

                a.status === 'placed' ||

                a.status === 'rejected'

        )" :key="'history' + application.application_id" class="card shadow-sm mb-4">

            <div class="card-body">

                <div class="d-flex justify-content-between">

                    <div>

                        <h4>

                            {{ application.job_title }}

                        </h4>

                        <h6 class="text-muted">

                            {{ application.company }}

                        </h6>

                    </div>

                    <div>

                        <span class="badge" :class="{

                            'bg-success': application.status === 'placed',

                            'bg-danger': application.status === 'rejected'

                        }">

                            {{ application.status }}

                        </span>

                    </div>

                </div>

                <hr>

                <p>

                    <strong>Applied On:</strong>

                    {{ application.applied_at }}

                </p>

                <div v-if="application.status === 'placed'" class="alert alert-success mt-3">

                    Congratulations! You have been successfully placed.

                </div>
                <button

                    v-if="application.status === 'placed'"

                    class="btn btn-success"

                    @click="downloadOfferLetter(application.application_id)"

                >

                    Download Offer Letter (PDF)

                </button>
                <div v-if="application.status === 'rejected'" class="alert alert-danger mt-3">

                    Application Closed.

                </div>

            </div>

        </div>
    </div>

</template>