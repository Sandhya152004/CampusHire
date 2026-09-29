<script setup>

import AdminNavbar from '../../components/AdminNavbar.vue'

import { ref,onMounted } from 'vue'

import api from '../../api'

const token = localStorage.getItem('token')

const report = ref({})

const fetchReport = async()=>{

    const response = await api.get(

        '/admin/reports',

        {

            headers:{

                Authorization:`Bearer ${token}`

            }

        }

    )

    report.value=response.data

}

onMounted(()=>{

    fetchReport()

})

</script>


<template>

    <AdminNavbar/>
    
    <div class="container mt-4">
    
    <h2>
    
    Placement Reports
    
    </h2>
    
    <p class="text-muted">
    
    Overall portal statistics.
    
    </p>
    
    <div class="row">
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.total_students }}</h3>
    
    <p>Total Students</p>
    
    </div>
    
    </div>
    
    </div>
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.total_companies }}</h3>
    
    <p>Total Companies</p>
    
    </div>
    
    </div>
    
    </div>
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.approved_companies }}</h3>
    
    <p>Approved Companies</p>
    
    </div>
    
    </div>
    
    </div>
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.pending_companies }}</h3>
    
    <p>Pending Companies</p>
    
    </div>
    
    </div>
    
    </div>
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.total_drives }}</h3>
    
    <p>Total Drives</p>
    
    </div>
    
    </div>
    
    </div>
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.active_drives }}</h3>
    
    <p>Active Drives</p>
    
    </div>
    
    </div>
    
    </div>
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.closed_drives }}</h3>
    
    <p>Closed Drives</p>
    
    </div>
    
    </div>
    
    </div>
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.total_applications }}</h3>
    
    <p>Total Applications</p>
    
    </div>
    
    </div>
    
    </div>
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.shortlisted }}</h3>
    
    <p>Shortlisted</p>
    
    </div>
    
    </div>
    
    </div>
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.interview }}</h3>
    
    <p>Interview Scheduled</p>
    
    </div>
    
    </div>
    
    </div>
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.offer }}</h3>
    
    <p>Offer</p>
    
    </div>
    
    </div>
    
    </div>
    
    <div class="col-md-3 mb-4">
    
    <div class="card shadow-sm">
    
    <div class="card-body text-center">
    
    <h3>{{ report.rejected }}</h3>
    
    <p>Rejected</p>
    
    </div>
    
    </div>
    
    </div>
    
    </div>
    
    </div>
    
    </template>