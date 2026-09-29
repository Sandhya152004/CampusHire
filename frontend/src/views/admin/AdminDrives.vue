<script setup>

import AdminNavbar from '../../components/AdminNavbar.vue'

import { ref,onMounted } from 'vue'
import api from '../../api'

const token = localStorage.getItem('token')

const drives = ref([])

const fetchDrives = async()=>{

    const response = await api.get(

        "/admin/drives",

        {

            headers:{

                Authorization:`Bearer ${token}`

            }

        }

    )

    drives.value = response.data

}

const approveDrive = async(id)=>{

    await api.put(

        `/admin/drive/${id}/approve`,

        {},

        {

            headers:{

                Authorization:`Bearer ${token}`

            }

        }

    )

    fetchDrives()

}

const rejectDrive = async(id)=>{

    const reason = prompt(

        "Enter rejection reason"

    )

    if(!reason) return

    await api.put(

        `/admin/drive/${id}/reject`,

        {

            reason

        },

        {

            headers:{

                Authorization:`Bearer ${token}`

            }

        }

    )

    fetchDrives()

}

onMounted(()=>{

    fetchDrives()

})

</script>


<template>

    <AdminNavbar />
    
    <div class="container mt-4">
    
        <div class="d-flex justify-content-between align-items-center mb-4">
    
            <div>
    
                <h2>Placement Drives</h2>
    
                <p class="text-muted">
    
                    Review and manage placement drives submitted by companies.
    
                </p>
    
            </div>
    
        </div>
    
        <div
            v-if="drives.length === 0"
            class="alert alert-info"
        >
            No placement drives available.
        </div>
    
        <div
    
            v-for="drive in drives"
    
            :key="drive.id"
    
            class="card shadow-sm mb-4"
    
        >
    
            <div class="card-body">
    
                <div class="d-flex justify-content-between align-items-start">
    
                    <div>
    
                        <h4>
    
                            {{ drive.job_title }}
    
                        </h4>
    
                        <p class="text-muted">
    
                            {{ drive.company_name }}
    
                        </p>
    
                    </div>
    
                    <div>
    
                        <span
    
                            v-if="drive.status==='approved'"
    
                            class="badge bg-success"
    
                        >
    
                            Approved
    
                        </span>
    
                        <span
    
                            v-else-if="drive.status==='pending'"
    
                            class="badge bg-warning text-dark"
    
                        >
    
                            Pending
    
                        </span>
    
                        <span
    
                            v-else
    
                            class="badge bg-danger"
    
                        >
    
                            Rejected
    
                        </span>
    
                    </div>
    
                </div>
    
                <hr>
    
                <p>
    
                    {{ drive.job_description }}
    
                </p>
    
                <div class="row">
    
                    <div class="col-md-4 mb-2">
    
                        <strong>Location</strong>
    
                        <p>{{ drive.location }}</p>
    
                    </div>
    
                    <div class="col-md-4 mb-2">
    
                        <strong>Salary</strong>
    
                        <p>{{ drive.salary }}</p>
    
                    </div>
    
                    <div class="col-md-4 mb-2">
    
                        <strong>Applicants</strong>
    
                        <p>{{ drive.applicant_count }}</p>
    
                    </div>
    
                    <div class="col-md-4 mb-2">
    
                        <strong>Minimum CGPA</strong>
    
                        <p>{{ drive.cgpa_required }}</p>
    
                    </div>
    
                    <div class="col-md-4 mb-2">
    
                        <strong>Eligible Degree</strong>
    
                        <p>{{ drive.eligible_degree }}</p>
    
                    </div>
    
                    <div class="col-md-4 mb-2">
    
                        <strong>Eligible Branch/Specialization</strong>
    
                        <p>{{ drive.eligible_branch }}</p>
    
                    </div>
    
                    <div class="col-md-4 mb-2">
    
                        <strong>Openings</strong>
    
                        <p>{{ drive.number_of_openings }}</p>
    
                    </div>
    
                    <div class="col-md-4 mb-2">
    
                        <strong>Deadline</strong>
    
                        <p>{{ drive.application_deadline }}</p>
    
                    </div>
    
                    <div class="col-md-4 mb-2">
    
                        <strong>Drive Status</strong>
    
                        <p>
    
                            {{ drive.is_closed ? 'Closed' : 'Open' }}
    
                        </p>
    
                    </div>
    
                </div>
    
                <div
                v-if="drive.status === 'rejected'"
                class="alert alert-danger"
                >

                <strong>Rejection Reason:</strong>

                {{ drive.rejection_reason }}

                </div>
    
                <div class="mt-3">
    
                    <div v-if="drive.status === 'pending'">

                        <button
                            class="btn btn-success me-2"
                            @click="approveDrive(drive.id)"
                        >
                            Approve
                        </button>

                        <button
                            class="btn btn-danger"
                            @click="rejectDrive(drive.id)"
                        >
                            Reject
                        </button>

                    </div>
    
                </div>
    
            </div>
    
        </div>
    
    </div>
    
    </template>