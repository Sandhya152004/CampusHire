<script setup>

import AdminNavbar from '../../components/AdminNavbar.vue'

import {ref,onMounted} from 'vue'

import api from '../../api'

const token = localStorage.getItem('token')

const applications = ref([])

const fetchApplications = async()=>{

    const response = await api.get(

        '/admin/applications',

        {

            headers:{

                Authorization:`Bearer ${token}`

            }

        }

    )

    applications.value=response.data

}

onMounted(()=>{

    fetchApplications()

})

</script>

<template>

    <AdminNavbar />
    
    <div class="container mt-4">
    
        <div class="d-flex justify-content-between align-items-center mb-4">
    
            <div>
    
                <h2>All Student Applications</h2>
    
                <p class="text-muted">
    
                    Monitor all placement applications submitted across the portal.
    
                </p>
    
            </div>
    
        </div>
    
        <div
            v-if="applications.length === 0"
            class="alert alert-info"
        >
            No applications found.
        </div>
    
        <div
            v-for="application in applications"
            :key="application.application_id"
            class="card shadow-sm mb-3"
        >
    
            <div class="card-body">
    
                <div class="row">
    
                    <div class="col-md-8">
    
                        <h5>
    
                            {{ application.student_name }}
    
                        </h5>
    
                        <p>
    
                            <strong>Company:</strong>
    
                            {{ application.company_name }}
    
                        </p>
    
                        <p>
    
                            <strong>Drive:</strong>
    
                            {{ application.job_title }}
    
                        </p>
    
                        <p>
    
                            <strong>Branch/Specialization:</strong>
    
                            {{ application.branch }}
    
                        </p>
    
                        <p>
    
                            <strong>CGPA:</strong>
    
                            {{ application.cgpa }}
    
                        </p>
    
                        <p>
    
                            <strong>Applied On:</strong>
    
                            {{ application.applied_at }}
    
                        </p>
    
                        <p v-if="application.interview_date">
    
                            <strong>Interview Date:</strong>
    
                            {{ application.interview_date }}
    
                        </p>
    
                    </div>
    
                    <div class="col-md-4 text-end">
    
                        <span
                            v-if="application.status === 'applied'"
                            class="badge bg-secondary"
                        >
                            Applied
                        </span>
    
                        <span
                            v-else-if="application.status === 'shortlisted'"
                            class="badge bg-warning text-dark"
                        >
                            Shortlisted
                        </span>
    
                        <span
                            v-else-if="application.status === 'interview'"
                            class="badge bg-info"
                        >
                            Interview
                        </span>
    
                        <span
                            v-else-if="application.status === 'offer'"
                            class="badge bg-success"
                        >
                            Offer
                        </span>
    
                        <span
                            v-else-if="application.status === 'rejected'"
                            class="badge bg-danger"
                        >
                            Rejected
                        </span>
    
                    </div>
    
                </div>
    
            </div>
    
        </div>
    
    </div>
    
    </template>