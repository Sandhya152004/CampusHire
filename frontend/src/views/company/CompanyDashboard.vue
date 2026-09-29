<script setup>
import CompanyNavbar from '../../components/CompanyNavbar.vue'
import { ref, onMounted } from 'vue'
import api from '../../api'
import { useRouter } from 'vue-router'

const router = useRouter()

const token = localStorage.getItem('token')

const dashboard = ref({})

const fetchDashboard = async () => {

  const response = await api.get(
    '/company/dashboard',
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  dashboard.value = response.data
}

const goToApplicant = (studentId) => {

    router.push(`/company/student/${studentId}`)

}

const goToDrive = (driveId) => {

    router.push(`/company/drives?edit=${driveId}`)

}

onMounted(() => {
  fetchDashboard()
})
</script>

<template>

<CompanyNavbar/>

<div class="container mt-4">

<h2>
Welcome,
{{ dashboard.company_name }}
</h2>

<div class="row mt-4">

<div class="col-md-3">
<div class="card shadow-sm p-3">
<h6>Active Drives</h6>
<h2>{{ dashboard.active_drives }}</h2>
</div>
</div>

<div class="col-md-3">
<div class="card shadow-sm p-3">
<h6>Applications</h6>
<h2>{{ dashboard.applications }}</h2>
</div>
</div>

<div class="col-md-3">
<div class="card shadow-sm p-3">
<h6>Shortlisted</h6>
<h2>{{ dashboard.shortlisted }}</h2>
</div>
</div>

<div class="col-md-3">
<div class="card shadow-sm p-3">
<h6>Offer</h6>
<h2>{{ dashboard.offer }}</h2>
</div>
</div>

</div>

<div class="row mt-4">

<div class="col-md-6">

<div class="card shadow-sm p-3">

<h4>Recent Drives</h4>

<div
v-for="drive in dashboard.recent_drives"
:key="drive.id"
class="card shadow-sm mb-3"
>

<div class="card-body">

    <div class="d-flex justify-content-between">

        <h5>{{ drive.job_title }}</h5>

        <span
            class="badge"

            :class="{

                'bg-success': drive.status==='approved',

                'bg-warning text-dark': drive.status==='pending',

                'bg-danger': drive.status==='rejected'

            }"

        >

            {{ drive.status }}

        </span>

    </div>

    <div class="row mt-3">

        <div class="col-md-6">

            <p>

                <strong>Applicants:</strong>

                {{ drive.applicants }}

            </p>

            <p>

                <strong>CGPA:</strong>

                {{ drive.cgpa_required }}

            </p>

        </div>

        <div class="col-md-6">

            <p>

                <strong>Deadline:</strong>

                {{ drive.deadline }}

            </p>

            <p>

                <strong>Location:</strong>

                {{ drive.location }}

            </p>

        </div>

    </div>

    <button

    class="btn btn-outline-primary"

    @click="goToDrive(drive.id)"

    >

    View Drive

    </button>

</div>

</div>

</div>

</div>

<div class="col-md-6">

<div class="card shadow-sm p-3">

<h4>Recent Applicants</h4>

<div
v-for="student in dashboard.recent_applicants"
:key="student.student_id"
class="card shadow-sm mb-3"
>

<div class="card-body">

    <div class="d-flex justify-content-between align-items-center">

        <h5>

            {{ student.student_name }}

        </h5>

        <span

            class="badge"

            :class="{

                'bg-secondary': student.status==='applied',

                'bg-primary': student.status==='shortlisted',

                'bg-warning text-dark': student.status==='interview_scheduled',

                'bg-success': student.status==='offer',

                'bg-dark': student.status==='placed',

                'bg-danger': student.status==='rejected'

            }"

        >

            {{ student.status }}

        </span>

    </div>

    <hr>

    <p>

        <strong>Applied For:</strong>

        {{ student.job_title }}

    </p>

    <p>

        <strong>Degree:</strong>

        {{ student.degree }}

    </p>

    <p>

        <strong>CGPA:</strong>

        {{ student.cgpa }}

    </p>

    <button

    class="btn btn-outline-success"

    @click="goToApplicant(student.student_id)"

    >

    View Student

    </button>

</div>

</div>

</div>

</div>

</div>

</div>

</template>